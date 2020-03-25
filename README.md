# Elf wrapper

[![Build Status](https://travis-ci.org/sgnes/elf_dwarf_wrapper.svg?branch=master)](https://travis-ci.org/sgnes/elf_dwarf_wrapper)
[![Coverage Status](https://coveralls.io/repos/github/sgnes/elf_dwarf_wrapper/badge.svg?branch=master)](https://coveralls.io/github/sgnes/elf_dwarf_wrapper?branch=master)

This tool use the [pyelftools](https://github.com/eliben/pyelftools) to parse the elf file, and provide a interface
for user to get the global variable address informations.



### Installation


Install use pip.

```sh
$ pip install python_elf_wrapper
```


 

### How to use it

```python 
from elf_addr_dict import ElfAddrObj
elf = ElfAddrObj(r"example/test.elf")
var_addr = elf.get_var_addrs('TestStructVar1')
print(var_addr)
enum_info = self.get_enum_info('TestEnumAType')
```

### Supported variable types
- structure 
- structure array
- structure array filed 
- array


### Todos

 - to add support for bit filed members
 - 
 
 

License
----

MIT


