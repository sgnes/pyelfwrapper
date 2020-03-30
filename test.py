# -*- coding: utf-8 -*-

import unittest
import os

from elfwrapper.elf_wrapper import ElfAddrObj 


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        elf = ElfAddrObj(os.path.join(os.getcwd(), r"example/Test.elf"))
        with open(r'example\test_var.txtdatafile.txt') as f:
            for line in f:
                var, _, add  = line.split(":")
                if elf.get_var_addrs(var) == int(add.strip(),16):
                    print()
        #self.assertEqual(, elf.get_var_addrs(""))



def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestApp)
    )

    return suite


if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=2).run(suite())