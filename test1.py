from elf_addr_dict import ElfAddrObj
import os

elf = ElfAddrObj(os.path.join(os.getcwd(), r"example/test.elf"))

vars = ["TestStructVar1", 'TestStructVar1.level1_1.level2_1.levle3_1.level4_1.level5_1', 'TestStructVar1.level1_2.level2_2.levle3_2.level4_2.level5_2']
for var in vars:
    print(hex(elf.get_var_addrs(var)))