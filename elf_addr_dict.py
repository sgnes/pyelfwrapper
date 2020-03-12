import re
from elftools.elf.sections import NoteSection, SymbolTableSection
from elftools.common.py3compat import (
        ifilter, byte2int, bytes2str, itervalues, str2bytes)
from elftools.elf.elffile import ELFFile
from elftools.dwarf.descriptions import (
    describe_reg_name, describe_attr_value, set_global_machine_arch,
    describe_CFI_instructions, describe_CFI_register_rule,
    describe_CFI_CFA_rule,
    )
from elftools.elf.gnuversions import (
    GNUVerSymSection, GNUVerDefSection,
    GNUVerNeedSection,
    )
from elftools.elf.dynamic import DynamicSection, DynamicSegment
import logging

class ElfAddrObj(ELFFile):
    """

    """
    def __init__(self, elf_file):
        self.struct_dict = {}
        self.offset_dict = {}
        self.member_dict = {}
        self.variables_dict = {}
        self.symbol_dict = {}
        self._versioninfo = None
        self._re_pattern = re.compile(r'\d+\s+[a-z]+\s+[a-z]+:\s+(\d+)\s+(\d+)\s+\(')
        self._elf_file_handler = open(r'd:\test.elf', 'rb')
        self.elffile = ELFFile(self._elf_file_handler)
        self.dwarfinfo = self.elffile.get_dwarf_info()
        self.section_offset = self.dwarfinfo.debug_info_sec.global_offset

        self._logger = logging.getLogger()
        self._parse_symbol_table()
        self._parse_debug_info()


    def _init_versioninfo(self):
        """ Search and initialize informations about version related sections
            and the kind of versioning used (GNU or Solaris).
        """
        if self._versioninfo is not None:
            return

        self._versioninfo = {'versym': None, 'verdef': None,
                             'verneed': None, 'type': None}

        for section in self.elffile.iter_sections():
            if isinstance(section, GNUVerSymSection):
                self._versioninfo['versym'] = section
            elif isinstance(section, GNUVerDefSection):
                self._versioninfo['verdef'] = section
            elif isinstance(section, GNUVerNeedSection):
                self._versioninfo['verneed'] = section
            elif isinstance(section, DynamicSection):
                for tag in section.iter_tags():
                    if tag['d_tag'] == 'DT_VERSYM':
                        self._versioninfo['type'] = 'GNU'
                        break

        if not self._versioninfo['type'] and (
                self._versioninfo['verneed'] or self._versioninfo['verdef']):
            self._versioninfo['type'] = 'Solaris'

    def _parse_symbol_table(self):
        """ Display the symbol tables contained in the file
        """
        self._init_versioninfo()

        symbol_tables = [s for s in self.elffile.iter_sections()
                         if isinstance(s, SymbolTableSection)]

        if not symbol_tables and self.elffile.num_sections() == 0:
            self._logger.warning('Dynamic symbol information is not available for displaying symbols.')
            return

        for section in symbol_tables:
            if not isinstance(section, SymbolTableSection):
                continue

            if section['sh_entsize'] == 0:
                self._logger.warning("\nSymbol table '%s' has a sh_entsize of zero!" % (
                    section.name))
                continue

            self._logger.info("\nSymbol table '%s' contains %s entries:" % (section.name, section.num_symbols()))

            for nsym, symbol in enumerate(section.iter_symbols()):
                self.symbol_dict[symbol.name] =  symbol['st_value']


    def _parse_debug_info(self):
        # Offset of the .debug_info section in the stream

        for cu in self.dwarfinfo.iter_CUs():
            die_depth = 0
            struct_name = None
            for die in cu.iter_DIEs():
                #print(' <%s><%x>: Abbrev Number: %s%s' % (die_depth,die.offset,die.abbrev_code,(' (%s)' % die.tag) if not die.is_null() else ''))
                if die.is_null():
                    die_depth -= 1
                    continue
                if die.tag == "DW_TAG_structure_type":
                    attrs = self._attr_to_dict(die)
                    if "DW_AT_name" in attrs:
                        struct_name = attrs["DW_AT_name"][2].strip()
                        self.struct_dict[struct_name] = {}
                    else:
                        pass
                        # Todo this maybe a union, will be handled later.
                    self.offset_dict[die.offset] = attrs

                if die.tag == "DW_TAG_member":
                    attrs = self._attr_to_dict(die)
                    if "DW_AT_name" in attrs and struct_name is not None:
                        self.member_dict["{}.{}".format(attrs["DW_AT_name"][2].strip(),struct_name)] = self.struct_dict[struct_name]
                        member_name = attrs['DW_AT_name'][2].strip()
                        self.struct_dict[struct_name][member_name] = attrs
                    else:
                        pass
                        #Todo this maybe a union, will be handled later.
                    if die.has_children:
                        die_depth += 1

                if die.tag == "DW_TAG_typedef":
                    attrs = self._attr_to_dict(die)
                    self.offset_dict[die.offset] = attrs

                if die.tag == "DW_TAG_variable":
                    attrs = self._attr_to_dict(die)
                    if "DW_AT_name" in attrs:
                        at_name = attrs["DW_AT_name"][2].strip()
                    else:
                        #Todo will be handled later
                        pass
                    attrs["abbrev_tag"] = die.tag
                    self.variables_dict[at_name] = attrs

    def _attr_to_dict(self, die):
        attrs = {attr[0]: attr for attr in
                 [(attr.name, attr.offset, describe_attr_value(attr, die, self.section_offset).strip()) for attr in
                  itervalues(die.attributes)]}
        if "DW_AT_type" in attrs:
            typestr = attrs["DW_AT_type"][2].strip()
            typeint = int(typestr[1:len(typestr) - 1], 16)
            attrs["DW_AT_type"] = (attrs["DW_AT_type"][0], attrs["DW_AT_type"][1], typeint)
        attrs["abbrev_tag"] = die.tag
        return attrs


    def get_var_addrs(self, var):
        addr = None
        if "." in var:
            names = var.split(".")
            full_offset = 0
            root, members = names[0], names[1:]
            root_type = self.offset_dict[self.variables_dict[root]['DW_AT_type'][2]]
            root_struct_name = self.offset_dict[root_type['DW_AT_type'][2]]['DW_AT_name'][2]
            root_struct = self.struct_dict[root_struct_name]
            for mem in members:
                offset_str = root_struct[mem]['DW_AT_data_member_location'][2]
                _, off = res = re.findall(self._re_pattern, offset_str)[0]
                full_offset += int(off, 16)
                self._logger.info("member name:{}, offset:{}".format(mem, off))
                root_type = self.offset_dict[root_struct[mem]['DW_AT_type'][2]]
                if root_type['DW_AT_type'][2] in self.offset_dict:
                    root_struct_name = self.offset_dict[root_type['DW_AT_type'][2]]['DW_AT_name'][2]
                    root_struct = self.struct_dict[root_struct_name]
            addr = self.symbol_dict[root] + full_offset
        else:
            if var in self.symbol_dict:
                addr = self.symbol_dict[var]
        return addr

