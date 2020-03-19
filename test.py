# -*- coding: utf-8 -*-

import unittest
import os

from elf_addr_dict import ElfAddrObj


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        elf = ElfAddrObj(os.path.join(os.getcwd(), r"example/Test.elf"))
        self.assertEqual(0xd0012564, elf.get_var_addrs("TestStructVar1"))
        self.assertEqual(0xd00125dd, elf.get_var_addrs("TestStructVar1.level1_2.level2_2.levle3_2.level4_2.level5_2"))
        self.assertEqual(0xd00036c9, elf.get_var_addrs("TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_1.level2_1.levle3_1.level4_1.level5_2[1]"))
        self.assertEqual(0xd0012564, elf.get_var_addrs("TestStructVar1.level1_1.level2_1.levle3_1.level4_1.level5_1"))
        self.assertEqual(0xd0011be4, elf.get_var_addrs("TestStructVar2.union1"))
        self.assertEqual(0xd0011bff, elf.get_var_addrs("TestStructVar2.unionStructl1.level2_1.levle3_2.level4_2.level5_4"))
        self.assertEqual(0xd000eb84, elf.get_var_addrs("TestVarArray3d[5][5][5]"))
        self.assertEqual(0xd001199c, elf.get_var_addrs("TestVarArray2d[5][5]"))
        self.assertEqual(0xd0011b2c, elf.get_var_addrs("TestVarArray1d[5]"))
        self.assertEqual(0xd000a3fe, elf.get_var_addrs("TestVarArrayUint163d[5][5][5]"))
        self.assertEqual(0x800004e8, elf.get_var_addrs("Can_kTxHwObjectConfig_0[11].MsgObjId"))
        self.assertEqual(0x80000498, elf.get_var_addrs("Can_kTxHwObjectConfig_0[1].MsgObjId"))



def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestApp)
    )

    return suite


if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=2).run(suite())