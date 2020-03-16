# -*- coding: utf-8 -*-

import unittest
import os

from elf_addr_dict import ElfAddrObj


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        elf = ElfAddrObj(os.path.join(os.getcwd(), r"example/Test.elf"))
        self.assertEqual(0xd0012154, elf.get_var_addrs("TestStructVar1"))
        self.assertEqual(0xd00121cd, elf.get_var_addrs("TestStructVar1.level1_2.level2_2.levle3_2.level4_2.level5_2"))
        self.assertEqual(0xd00032b9, elf.get_var_addrs("TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_1.level2_1.levle3_1.level4_1.level5_2[1]"))
        self.assertEqual(0xd0012154, elf.get_var_addrs("TestStructVar1.level1_1.level2_1.levle3_1.level4_1.level5_1"))
        self.assertEqual(0xd00117d4, elf.get_var_addrs("TestStructVar2.union1"))
        self.assertEqual(0xd00117ef, elf.get_var_addrs("TestStructVar2.unionStructl1.level2_1.levle3_2.level4_2.level5_4"))
        self.assertEqual(0xd000e774, elf.get_var_addrs("TestVarArray3d[5][5][5]"))
        self.assertEqual(0xd001158c, elf.get_var_addrs("TestVarArray2d[5][5]"))
        self.assertEqual(0xd001171c, elf.get_var_addrs("TestVarArray1d[5]"))
        self.assertEqual(0xd0009fee, elf.get_var_addrs("TestVarArrayUint163d[5][5][5]"))
        #self.assertEqual(0xd00, elf.get_var_addrs(""))



def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestApp)
    )

    return suite


if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=2).run(suite())