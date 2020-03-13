# -*- coding: utf-8 -*-

import unittest
import os

from elf_addr_dict import ElfAddrObj


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        elf = ElfAddrObj(os.path.join(os.getcwd(), r"example/Test.elf"))
        self.assertEqual(elf.get_var_addrs("TestStructVar1"), 0xd000916c)
        self.assertEqual(elf.get_var_addrs("TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_1.level2_1.levle3_1.level4_1.level5_2[1]"), 0xd00032b9)
        self.assertEqual(elf.get_var_addrs("TestStructVar1.level1_1.level2_1.levle3_1.level4_1.level5_1"), 0xd000916c)



def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestApp)
    )

    return suite


if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=2).run(suite())