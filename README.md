# Elf wrapper

[![Build Status](https://travis-ci.org/sgnes/elf_addr_dict.png)](https://travis-ci.org/sgnes/elf_addr_dict)
[![Coverage Status](https://coveralls.io/repos/github/sgnes/elf_addr_dict/badge.svg?branch=master)](https://coveralls.io/github/sgnes/elf_addr_dict?branch=master)

This will use the [pyelftools](https://github.com/eliben/pyelftools) to parse the elf file, and provide a interface
for user to get the global variable address informations.



### Installation


Install the dependencies.

```sh
$ pip install pyelftools
```


### How to use it

```python 
from elf_addr_dict import ElfAddrObj
elf = ElfAddrObj(r"example/test.elf")
var_addr = elf.get_var_addrs('TestStructVar1')
print(var_addr)
```

### Supported variable types
- TestVaru32_2
- TestStruct5Var[1].TestStruct5uint32[2]
- TestStructVar1.level1_1.level2_1.levle3_1.level4_1.level5_1


### Todos

 - to add support of union;
 
 

License
----

MIT


