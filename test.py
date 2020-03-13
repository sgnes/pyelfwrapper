# -*- coding: utf-8 -*-

import unittest
import os

from elf_addr_dict import ElfAddrObj


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        elf = ElfAddrObj(os.path.join(os.getcwd(), r"example/Test.elf"))
        self.assertEqual(elf.get_var_addrs("TestStructVar1"), 0xd000005c)



def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestApp)
    )

    return suite


if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=2).run(suite())