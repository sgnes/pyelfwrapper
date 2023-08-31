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
from logging.config import fileConfig
from elfwrapper.elf_exception import ParseSequenceError,UnSupportedElfFormatError
from elfwrapper.utility import objdict


class ElfAddrObj(ELFFile):
    """

    """
    DW_AT_TYPE = 'DW_AT_type'
    DW_AT_TYPEDEF = 'DW_TAG_typedef'
    DW_AT_NAME = 'DW_AT_name'
    DW_AT_BASE_TYPE = 'DW_TAG_base_type'
    version = '0.0.5'

    def __init__(self, elf_file):
        self.struct_dict = objdict()
        self.offset_dict = objdict()
        self.member_dict = objdict()
        self.variables_dict = objdict()
        self.symbol_dict = objdict()
        self.union_dict = objdict()
        self.array_type_dict = objdict()
        self.array_dict = objdict()
        self.typedef_dict = objdict()
        self.enum_dict = objdict()
        self._versioninfo = None
        self._die_depth = 0
        self._re_pattern = re.compile(r'DW_OP_plus_uconst:\s+(\d+)')
        self.re_pattern_varname = re.compile(
            r'([a-zA-Z_][a-zA-Z0-9_]+)\s*\[(\d+)\]')
        self.re_pattern_array = re.compile(r"\[(\d+)\]")
        self._elf_file_handler = open(elf_file, 'rb')
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
            self._logger.warning(
                'Dynamic symbol information is not available for displaying symbols.')
            return

        for section in symbol_tables:
            if not isinstance(section, SymbolTableSection):
                continue

            if section['sh_entsize'] == 0:
                self._logger.warning("\nSymbol table '%s' has a sh_entsize of zero!" % (
                    section.name))
                continue

            self._logger.info("\nSymbol table '%s' contains %s entries:" % (
                section.name, section.num_symbols()))

            for nsym, symbol in enumerate(section.iter_symbols()):
                self.symbol_dict[symbol.name] = symbol['st_value']

    def _parse_debug_info(self):
        # Offset of the .debug_info section in the stream
        iter_cus = self.dwarfinfo.iter_CUs()
        for cu in iter_cus:
            self._die_depth = 0
            iter_dies = cu.iter_DIEs()
            for die in iter_dies:
                self._process_die(die, iter_dies)

    def _process_die(self, die, iter_dies):

        if die.tag == "DW_TAG_structure_type":
            self._process_structure_type(die, iter_dies)
        elif die.tag == "DW_TAG_member":
            raise ParseSequenceError
        elif die.tag == "DW_TAG_typedef":
            attrs = self._attr_to_dict(die)
            self.offset_dict[die.offset] = attrs
            self.typedef_dict[attrs.DW_AT_name] = attrs
        elif die.tag == "DW_TAG_variable":
            self._process_variable(die, iter_dies)
        elif die.tag == "DW_TAG_union_type":
            self._process_union(die, iter_dies)

        elif die.tag == 'DW_TAG_array_type':
            self._process_array(die, iter_dies)
        elif die.tag == self.DW_AT_BASE_TYPE:
            self._process_base_type(die)
        elif die.tag == 'DW_TAG_compile_unit':
            pass
        elif die.tag == "DW_TAG_const_type":
            self.offset_dict[die.offset] = self._attr_to_dict(die)
        elif die.tag == None:
            pass
        elif die.tag == "DW_TAG_volatile_type":
            self.offset_dict[die.offset] = self._attr_to_dict(die)
        elif die.tag == "DW_TAG_enumeration_type":
            self._process_enum(die, iter_dies)
        else:
            self._process_unneeded(die, iter_dies)

    def _process_enum(self, die, iter_dies):
        attrs = self._attr_to_dict(die)
        self.offset_dict[die.offset] = objdict()
        for key in attrs:
            self.offset_dict[die.offset][key] = attrs[key]
        if self.DW_AT_NAME not in attrs:
            attrs.DW_AT_name = die.offset
        enum_type_name = attrs.DW_AT_name
        self.enum_dict[enum_type_name] = attrs

        self.offset_dict[die.offset].DW_AT_type = die.offset
        self.offset_dict[die.offset].tag = die.tag
        next_die = next(iter_dies)
        while(next_die.tag == "DW_TAG_enumerator"):
            attrs = self._attr_to_dict(next_die)
            self.offset_dict[die.offset][attrs.DW_AT_name] = attrs
            next_die = next(iter_dies)
        self._process_die(next_die, iter_dies)

    def _process_unneeded(self, die, iter_dies):
        while(1):
            #attrs = self._attr_to_dict(die)
            if die.is_null():
                self._die_depth -= 1
            if die.has_children:
                self._die_depth += 1
            self._logger.info("Unhandled die: is_null:{0}, has_children:{1}, die_depth:{2}, info:{3}".format(
                die.is_null(), die.has_children, self._die_depth, die.attributes))

            if self._die_depth <= 0:
                break
            try:
                die = next(iter_dies)
            except StopIteration:
                pass

    def _process_union(self, die, iter_dies):
        attrs = self._attr_to_dict(die)
        self.union_dict[die.offset] = [attrs]
        self.offset_dict[die.offset] = attrs

        next_die = next(iter_dies)
        while (next_die.tag == 'DW_TAG_member'):
            attrs = self._attr_to_dict(next_die)
            if self.DW_AT_NAME in attrs:
                self.union_dict[die.offset].append(attrs)
            else:
                raise UnSupportedElfFormatError
            next_die = next(iter_dies)
        self._process_die(next_die, iter_dies)

    def _process_variable(self, die, iter_dies):
        attrs = self._attr_to_dict(die)
        if self.DW_AT_NAME in attrs:
            at_name = attrs.DW_AT_name
        else:
            at_name = die.offset
            self._logger.warning(
                "None named variable found with offset:{0}".format(die.offset))
            attrs.DW_AT_name = die.offset
        attrs.tag = die.tag
        self.variables_dict[at_name] = attrs

    def _process_structure_type(self, die, iter_dies):
        attrs = self._attr_to_dict(die)
        if self.DW_AT_NAME in attrs:
            struct_name = attrs.DW_AT_name
        else:
            struct_name = die.offset
            self._logger.warning(
                "None named structure found with offset:{0}".format(die.offset))
            attrs.DW_AT_name = die.offset
        self.struct_dict[struct_name] = objdict()
        self.offset_dict[die.offset] = attrs

        next_die = next(iter_dies)
        while(next_die.tag == 'DW_TAG_member'):
            attrs = self._attr_to_dict(next_die)
            if self.DW_AT_NAME in attrs:
                member_name = attrs.DW_AT_name
                self.struct_dict[struct_name][member_name] = attrs
            else:
                for i in self.union_dict[attrs.DW_AT_type][1:]:
                    i.DW_AT_data_member_location = attrs.DW_AT_data_member_location
                    member_name = i.DW_AT_name
                    self.struct_dict[struct_name][member_name] = i
            next_die = next(iter_dies)
        self._process_die(next_die, iter_dies)

    def _process_base_type(self, die):
        attrs = self._attr_to_dict(die)
        self.offset_dict[die.offset] = attrs

    def _process_array(self, die, iter_dies):
        attrs = self._attr_to_dict(die)
        self.offset_dict[die.offset] = attrs

        next_die = next(iter_dies)
        upper_bound_list = []
        while (next_die.tag == 'DW_TAG_subrange_type'):
            attrs1 = self._attr_to_dict(next_die)
            if 'DW_AT_upper_bound' in attrs1:
                bound = attrs1.DW_AT_upper_bound
                base = 10
                if bound.upper().startswith("0X"):
                    base = 16
                upper_bound_list.append(int(bound, base))
            else:
                #Todo this should be handled later.
                self._logger.warning("Unsupported AT type:{0}, offset:{1}, more info:{2}".format(
                    next_die.tag, next_die.offset, next_die.attributes))
            next_die = next(iter_dies)

        attrs.DW_AT_upper_bound = upper_bound_list
        self.array_type_dict[die.offset] = attrs
        self._process_die(next_die, iter_dies)

    def _attr_to_dict(self, die):
        attrs_raw = {attr[0]: attr for attr in
                     [(attr.name, attr.offset, describe_attr_value(attr, die, self.section_offset).strip()) for attr in
                      itervalues(die.attributes)]}

        attrs = objdict()
        attrs.tag = die.tag
        for i in attrs_raw:
            attrs[i] = attrs_raw[i][2].strip()
        if self.DW_AT_TYPE in attrs_raw:
            typestr = attrs_raw[self.DW_AT_TYPE][2].strip()
            typeint = int(typestr[1:len(typestr) - 1], 16)
            attrs.DW_AT_type = typeint
        if self.DW_AT_NAME in attrs and attrs.DW_AT_name.startswith("(indirect string, offset:"):
            attrs.DW_AT_name = attrs.DW_AT_name.split(":")[2].strip()
        attrs.raw_die = die
        attrs.offset = die.offset
        return attrs

    def _get_struct_info(self, root_full):
        baseoffset, root_base_name, root_type = 0, root_full, None
        if '[' in root_full:
            #root_full can be 'Can_kTxHwObjectConfig_0[1]'
            root_base_name, baseoffset, base_type = self._get_array_info(
                root_full)

            self._logger.info(
                "Array type found with name:{0}, baseoffset:{1}".format(root_full, baseoffset))
            if self.DW_AT_NAME in base_type:
                root_struct_name = base_type.DW_AT_name
            else:
                root_struct_name = None
        else:
            root_type = self.offset_dict[self.variables_dict[root_base_name].DW_AT_type]
        #if root_type.tag == 'DW_TAG_const_type':
            base_type = self.offset_dict[root_type.DW_AT_type]
            if self.DW_AT_NAME in base_type:
                root_struct_name = base_type.DW_AT_name
            else:
                root_struct_name = None
                self._logger.error("Not found structure :{}".format(root_type))
        return (root_struct_name, baseoffset, root_base_name, base_type)

    def _get_array_member_info(self, mem, root_struct):
        membaseoffset = 0
        mem_base, offset = re.findall(self.re_pattern_varname, mem)[0]
        res = re.findall(self._re_pattern, root_struct[mem_base].DW_AT_data_member_location)
        if res:
            off = res[0]
        else:
            try:
                off = int(root_struct[mem_base].DW_AT_data_member_location)
            except Exception as e:
                self._logger.error(e)
        membaseoffset += int(off)
        self._logger.info("Element :{0}, offset:{1}".format(mem_base, off))
        root_type = self.offset_dict[self.array_type_dict[root_struct[mem_base].DW_AT_type].DW_AT_type]
        mem_type = self.offset_dict[root_type.DW_AT_type]
        while(mem_type.tag == 'DW_TAG_typedef'):
            mem_type = self.offset_dict[mem_type.DW_AT_type]
        mem_size = int(mem_type.DW_AT_byte_size)
        membaseoffset += mem_size * int(offset)
        self._logger.info("Array type found with base member name:{0}, base size:{1}, membaseoffset:{2}".format(
            mem, mem_size, membaseoffset))
        return (membaseoffset, root_type)

    def _get_array_offset_type(self, array_name):
        array_base_type = self.offset_dict[
            self.offset_dict[self.variables_dict[array_name].DW_AT_type].DW_AT_type]

        while (array_base_type.tag not in ['DW_TAG_base_type', 'DW_TAG_enumeration_type', 'DW_TAG_union_type', 'DW_TAG_structure_type']):
            array_base_type = self.offset_dict[array_base_type.DW_AT_type]
        array_base_type_size = int(array_base_type.DW_AT_byte_size)
        variable_type = self.variables_dict[array_name].DW_AT_type
        while (variable_type not in self.array_type_dict):
            variable_type = self.offset_dict[variable_type].DW_AT_type
        array_type = self.array_type_dict[variable_type]
        if 'array_size_info' not in array_type:
            temp_array = array_type.DW_AT_upper_bound.copy()
            temp_array.reverse()
            array_size_level = []
            if len(temp_array) > 1:
                temp_value = (temp_array[0] + 1) * array_base_type_size
                array_size_level.append(temp_value)
                for i in temp_array[1:(len(temp_array) - 1)]:
                    temp_value = (i + 1) * temp_value
                    array_size_level.append(temp_value)
                array_size_level.reverse()
                array_size_level.append(array_base_type_size)
            else:
                array_size_level.append(array_base_type_size)
            array_type.array_size_info = array_size_level
        return (array_type.array_size_info, array_base_type)

    def _get_array_info(self, var):
        array_name = var[:var.find('[')]
        offset = 0
        if array_name in self.symbol_dict:
            res = [int(i) for i in re.findall(
                self.re_pattern_array, var[var.find('['):])]
            array_size_level, base_type = self._get_array_offset_type(
                array_name)
            for i in range(len(res)):
                offset += res[i] * array_size_level[i]
        return (array_name, offset, base_type)

    def get_var_addrs(self, var):
        addr = None
        var = var.replace(' ', '')
        self._logger.info("Start processing variable :{0}".format(var))
        if "." in var:
            names = var.split(".")
            root_full, members = names[0], names[1:]
            all_mem_offset = 0
            root_struct_name, baseoffset, root_base_name, base_type = self._get_struct_info(
                root_full)
            if base_type.tag == 'DW_TAG_union_type':
                pass
            elif base_type.tag == 'DW_TAG_structure_type':
                root_struct = self.struct_dict[root_struct_name]
                for mem in members:
                    # first to find the member offset
                    mem_base = mem
                    if '[' in mem:
                        membaseoffset, root_type = self._get_array_member_info(
                            mem, root_struct)
                    else:
                        # None array field
                        res = re.findall(self._re_pattern, root_struct[mem_base].DW_AT_data_member_location)
                        if res:
                            off = res[0]
                        else:
                            try:
                                off = int(root_struct[mem_base].DW_AT_data_member_location)
                            except Exception as e:
                                self._logger.error(e)
                        membaseoffset = int(off)
                        root_type = self.offset_dict[root_struct[mem_base].DW_AT_type]
                        self._logger.info(
                            "Normal name:{0}, with offset:{1}".format(mem, membaseoffset))

                    if root_type.tag == self.DW_AT_TYPEDEF and root_type.DW_AT_type in self.offset_dict:
                        mem_type = self.offset_dict[root_type.DW_AT_type]
                        if mem_type.tag == "DW_TAG_structure_type":
                            if self.DW_AT_NAME in mem_type:
                                root_struct = self.struct_dict[mem_type.DW_AT_name]
                            else:
                                self._logger.error(
                                    "Not found structure :{}".format(mem_type))
                        #elif mem_type.tag == 'DW_TAG_typedef':

                    all_mem_offset += membaseoffset
            else:
                raise UnSupportedElfFormatError
            addr = self.symbol_dict[root_base_name] + \
                baseoffset + all_mem_offset
            self._logger.info("End processing variable:{0}, base offset:{1}, member offset:{2}, addr:{3:#x}".format(
                var, baseoffset, all_mem_offset, addr))
        else:
            if '[' in var and ']' in var:
                # it's a array
                array_name, offset, base_type = self._get_array_info(var)
                base_addr = self.symbol_dict[array_name]
                self._logger.info("End processing variable:{0}, addr:{1:#x}".format(
                    var, base_addr + offset))
                addr = base_addr + offset

            elif var in self.symbol_dict:
                addr = self.symbol_dict[var]
                self._logger.info(
                    "End processing variable:{0}, addr:{1:#x}".format(var, addr))
            else:
                raise KeyError
        return addr

    def get_enum_info(self, name):
        enum_type = None
        res = None
        if name in self.enum_dict:
            enum_type = self.offset_dict[self.enum_dict[name].offset]
        elif name in self.typedef_dict:
            enum_type = self.offset_dict[self.typedef_dict[name].DW_AT_type]
            while enum_type.tag == self.DW_AT_TYPEDEF:
                enum_type = self.offset_dict[enum_type.DW_AT_type]
        if enum_type:
            res = {i: enum_type[i].DW_AT_const_value for i in enum_type if type(enum_type[i]) == objdict}
        return res

