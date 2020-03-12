# -*- coding: utf-8 -*-

import unittest

from elf_addr_dict import ElfAddrObj


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        elf = ElfAddrObj(r'.\example\test.elf')
        self.assertEqual(elf.get_var_addrs("TestStructVar1"), 0xb00034dc)



def suite():
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestApp)
    )

    return suite


if __name__ == '__main__':

    unittest.TextTestRunner(verbosity=2).run(suite())