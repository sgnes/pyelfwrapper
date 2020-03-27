# -*- coding: utf-8 -*-

import unittest
import os

from elfwrapper.elf_wrapper import ElfAddrObj 


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        elf = ElfAddrObj(os.path.join(os.getcwd(), r"example/Test.elf"))
        self.assertEqual(0xd0013bcc, elf.get_var_addrs("TestStructVar1"))
        self.assertEqual(0xd0013c45, elf.get_var_addrs("TestStructVar1.level1_2.level2_2.levle3_2.level4_2.level5_2"))
        self.assertEqual(0xd0003ef1, elf.get_var_addrs("TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_1.level2_1.levle3_1.level4_1.level5_2[1]"))
        self.assertEqual(0xd0013bcc, elf.get_var_addrs("TestStructVar1.level1_1.level2_1.levle3_1.level4_1.level5_1"))
        self.assertEqual(0xd001318c, elf.get_var_addrs("TestStructVar2.union1"))
        self.assertEqual(0xd00131a7, elf.get_var_addrs("TestStructVar2.unionStructl1.level2_1.levle3_2.level4_2.level5_4"))
        self.assertEqual(0xd001012c, elf.get_var_addrs("TestVarArray3d[5][5][5]"))
        self.assertEqual(0xd0012f44, elf.get_var_addrs("TestVarArray2d[5][5]"))
        self.assertEqual(0xd00130d4, elf.get_var_addrs("TestVarArray1d[5]"))
        self.assertEqual(0xd000b9a6, elf.get_var_addrs("TestVarArrayUint163d[5][5][5]"))
        self.assertEqual(0x80000510, elf.get_var_addrs("Can_kTxHwObjectConfig_0[11].MsgObjId"))
        self.assertEqual(0x800004c0, elf.get_var_addrs("Can_kTxHwObjectConfig_0[1].MsgObjId"))
        self.assertEqual(0xd0013584, elf.get_var_addrs('TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.FiledEnum'))
        self.assertEqual(0xd0013587, elf.get_var_addrs("TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.FiledEnumAray[2]"))
        self.assertEqual(0xd00000b2, elf.get_var_addrs("TestEnumTest1"))
        self.assertEqual(0xd000004d, elf.get_var_addrs("L9301_CHxDIAG[4][5].U"))
        self.assertEqual(0xd00000aa, elf.get_var_addrs("TestEnumTest11[2]"))
        self.assertEqual(elf.get_enum_info("TestEnumATypeaaabbb"), {'TestEnumType11': '0', 'TestEnumType21': '1', 'TestEnumType31': '2', 'TestEnumType41': '3', 'TestEnumType51': '4', 'TestEnumType61': '5'})
        self.assertEqual(elf.get_enum_info("TestEnumATypeaaa"), {'TestEnumType11': '0', 'TestEnumType21': '1', 'TestEnumType31': '2', 'TestEnumType41': '3', 'TestEnumType51': '4', 'TestEnumType61': '5'})
        self.assertEqual(elf.get_enum_info("TestEnumTypeA"), {'TestEnumType11': '0', 'TestEnumType21': '1', 'TestEnumType31': '2', 'TestEnumType41': '3', 'TestEnumType51': '4', 'TestEnumType61': '5'})



def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestApp)
    )

    return suite


if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=2).run(suite())