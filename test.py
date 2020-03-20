# -*- coding: utf-8 -*-

import unittest
import os

from elf_addr_dict import ElfAddrObj


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        elf = ElfAddrObj(os.path.join(os.getcwd(), r"example/Test.elf"))
        self.assertEqual(0xd00133f0, elf.get_var_addrs("TestStructVar1"))
        self.assertEqual(0xd0013469, elf.get_var_addrs("TestStructVar1.level1_2.level2_2.levle3_2.level4_2.level5_2"))
        self.assertEqual(0xd0003bd5, elf.get_var_addrs("TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_1.level2_1.levle3_1.level4_1.level5_2[1]"))
        self.assertEqual(0xd00133f0, elf.get_var_addrs("TestStructVar1.level1_1.level2_1.levle3_1.level4_1.level5_1"))
        self.assertEqual(0xd00129f0, elf.get_var_addrs("TestStructVar2.union1"))
        self.assertEqual(0xd0012a0b, elf.get_var_addrs("TestStructVar2.unionStructl1.level2_1.levle3_2.level4_2.level5_4"))
        self.assertEqual(0xd000f990, elf.get_var_addrs("TestVarArray3d[5][5][5]"))
        self.assertEqual(0xd00127a8, elf.get_var_addrs("TestVarArray2d[5][5]"))
        self.assertEqual(0xd0012938, elf.get_var_addrs("TestVarArray1d[5]"))
        self.assertEqual(0xd000b20a, elf.get_var_addrs("TestVarArrayUint163d[5][5][5]"))
        self.assertEqual(0x80000500, elf.get_var_addrs("Can_kTxHwObjectConfig_0[11].MsgObjId"))
        self.assertEqual(0x800004b0, elf.get_var_addrs("Can_kTxHwObjectConfig_0[1].MsgObjId"))
        self.assertEqual(0xD0012db8, elf.get_var_addrs('TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.FiledEnum'))
        self.assertEqual(0xD0012dbb, elf.get_var_addrs("TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.FiledEnumAray[2]"))
        self.assertEqual(0xd0000018, elf.get_var_addrs("TestEnumTest1"))
        #self.assertEqual(, elf.get_var_addrs(""))



def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestApp)
    )

    return suite


if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=2).run(suite())