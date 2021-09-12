import sys, os
sys.path.append(os.getcwd())
from elfwrapper.elf_wrapper import ElfAddrObj 
import datetime
print("Test time Before Init", datetime.datetime.now())
elf = ElfAddrObj(r"V:\github\pyelfwrapper\example\STM32CubeIDE.elf")
print("Test time After Init", datetime.datetime.now())

vars = [
    'TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.FiledEnum',
    "L9301_CHxDIAG[4][5].U",
    "L9301_CHxDIAG[4][5].I",
    'TestEnumTest11[2]',
    'TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_1.level2_2.levle3_1.level4_1.level5_777',
    'TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_1.level2_1.levle3_1.level4_1.level5_2[1]',
    'TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.FiledEnumAray[2]',
    'TestEnumTest1',
    'Can_kTxHwObjectConfig_0[1].MsgObjId',
    'testU8xxxx[1][2][3]',
    'testU8xxxxyyy[1][2][3]',
    'TestVarArray1d[5]',
    'TestVarArrayUint163d[5][5][5] ',
    'TestVarArray3d[5][5][5]',
    'TestVarArray2d[5][5]',
    'TestStructVar2.union1',
    'TestStructVar2.unionStructl1.level2_1.levle3_2.level4_2.level5_4',
    'TestStructVar1.level1_2.level2_2.levle3_2.level4_2.level5_2',
    'TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_2.level2_2.levle3_2.level4_1.level5_2[1]',
    "TestStructVar1",
    'TestStructVar1.level1_1.level2_1.levle3_1.level4_1.level5_1',
    'Can_kTxHwObjectConfig_0[11].MsgObjId',
    'Can_kTxHwObjectConfig_0[1].MsgObjId']
for var in vars:
    print(var, hex(elf.get_var_addrs(var)))


enums = [ 'TestEnumATypeaaabbb', 'TestEnumATypeaaa','TestEnumAType', 'TestEnumType', 'TestEnumTypeA']
for i in enums:
    print(i, elf.get_enum_info(i))
