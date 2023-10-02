# Elf wrapper

[![Build Status](https://travis-ci.org/sgnes/elf_dwarf_wrapper.svg?branch=master)](https://travis-ci.org/sgnes/elf_dwarf_wrapper)
[![Coverage Status](https://coveralls.io/repos/github/sgnes/elf_dwarf_wrapper/badge.svg?branch=master)](https://coveralls.io/github/sgnes/elf_dwarf_wrapper?branch=master)

This tool use the [pyelftools](https://github.com/eliben/pyelftools) to parse the elf file, and provide an interface
for user to get the global variable address information.

This was intended to update the address information in the A2L file for CCP/XCP calibration, 
which use widely used in automotive industry.


### Installation


Install use pip.

```sh
$ pip install pyelfwrapper
```


 

### How to use it

#### Step 1:
Write An example c source code with global variables.
```c 
#include <stdlib.h>

typedef unsigned char uint8;
typedef unsigned short uint16;
typedef unsigned int  uint32;


typedef struct TestStructFileds{

	uint32 filed1:5;
	uint32 filed2:6;
	uint32 filed3:5;
	uint32 filed4:8;

}TestStructFiledsType;


typedef struct TestStructArrayLevel5{
uint8 level5_1[16];
uint8 level5_2[16];
uint8 level5_3[16];
uint8 level5_4[16];
TestStructFiledsType Filed1;
}TestStructArrayLevel5Type;

typedef struct TestStructArrayLevel4{
TestStructArrayLevel5Type level4_1;
TestStructArrayLevel5Type level4_2;
}TestStructArrayLevel4Type;


typedef struct TestStructArrayLevel3{
TestStructArrayLevel4Type levle3_1;
TestStructArrayLevel4Type levle3_2;
}TestStructArrayLevel3Type;


typedef struct TestStructArrayLevel2{
TestStructArrayLevel3Type level2_1;
TestStructArrayLevel3Type level2_2;
}TestStructArrayLevel2Type;


typedef struct TestStructArrayLevel1{
TestStructArrayLevel2Type level1_1;
TestStructArrayLevel2Type level1_2;
}TestStructArrayLevel1Type;


typedef enum
{
    TestEnum1 = 0,
    TestEnum2
}TestEnumType;


typedef struct TestStructLevel5{
uint8 level5_1;
uint8 level5_2;
uint8 levezl5_3;
uint8 level5_4;
TestStructFiledsType Filed2;
}TestStructLevel5Type;

typedef struct TestStructLevel4{
TestStructLevel5Type level4_1;
TestStructLevel5Type level4_2;
}TestStructLevel4Type;


typedef struct TestStructLevel3{
TestStructLevel4Type levle3_1;
TestStructLevel4Type levle3_2;
}TestStructLevel3Type;


typedef struct TestStructLevel2{
TestStructLevel3Type level2_1;
TestStructLevel3Type level2_2;
}TestStructLevel2Type;


typedef struct TestStructLevel1{
TestStructLevel2Type level1_1;
TestStructLevel2Type level1_2;
}TestStructLevel1Type;



TestStructLevel1Type  TestStructVar1;
TestStructLevel1Type  TestStructVar1Array[10];
TestStructArrayLevel1Type TestStructArrayVar1;


typedef struct TestUnionStructLevel1
{
	TestStructLevel2Type level1_1;
	union
	{
		uint32 union1;
		TestStructLevel2Type unionStructl1;
	};

}TestUnionStructLevel1Type;



TestUnionStructLevel1Type TestStructVar2;

uint32 TestVaru32_1;
uint32 TestVaru32_2;
uint32 TestVaru32_3;

float TestVarFloat1;
float TestVarFloat2;
uint32 TestVarArrayUint32[10];
float TestVarArrayFloat32[10];

uint32 TestVarArray1d[10];
uint32 TestVarArray2d[10][20];
uint32 TestVarArray3d[10][20][30];
uint16 TestVarArrayUint163d[10][20][30];

struct TestStruct5
{
	uint8 TestStruct5uint8[200];
	uint32 TestStruct5uint32[40];
	float TestStruct5float[10];
	TestUnionStructLevel1Type TestUnionStructLevel1TypeMem[5];
	TestStructArrayLevel1Type TestUnionArrayLevel1TypeMem[7];
};

struct TestStruct5 TestStruct5Var[4];

TestEnumType TestEnumTest11[10];
TestEnumType TestEnumTest1;
uint8 testU8xxxx[3][4][5];
uint8 testU8xxxxyyy[3][4][5];

int main(void)
{

	TestStructVar1.level1_1.level2_1.levle3_1.level4_1.level5_1 = 55;
	TestStructVar2.union1 = 0x55;
	TestStructVar2.unionStructl1.level2_1.levle3_2.level4_2.level5_4= 1;
	TestVaru32_1 = 0x55;
	TestVaru32_2 = 0x55;
	TestVaru32_3 = 0x55;
	TestVarFloat1 = 0.4;
	TestVarFloat2 = 0.7;

	TestVarArrayUint32[1] = 66;
	TestVarArrayFloat32[4] = 0.5;
	TestStructArrayVar1.level1_1.level2_2.levle3_2.level4_2.level5_2[1] = 9;
	TestStructVar1Array[2].level1_1.level2_2.levle3_1.level4_1.level5_2 = 4;

	TestStruct5Var[1].TestStruct5uint32[2] = 10;
	TestStruct5Var[1].TestUnionStructLevel1TypeMem[3].level1_1.level2_2.levle3_1.level4_1.level5_2 = 5;
	TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_1.level2_2.levle3_1.level4_1.level5_2[1] = 7;
	
	TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.Filed1.filed2 = 1;
	TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.Filed1.filed1 = 1;
	TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.Filed1.filed3 = 3;
	TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.Filed1.filed4 = 2;

	TestVarArray1d[5] = 5;
	TestVarArray2d[5][5] = 5;
	TestVarArray3d[5][5][5] = 5;
	TestVarArrayUint163d[5][5][5] = 5;



	return EXIT_SUCCESS;
}

```
#### Step 2:
Compile it to an elf file.

```shell 
arm-none-eabi-gcc --specs=nosys.specs -g hello.c -o  hello_arm_none_eabi_gcc.elf
```

#### Step 3:
Use this tool to get global variable address.

```python 
from elfwrapper.elf_wrapper import ElfAddrObj
elf = ElfAddrObj(r"example/test.elf")
var_addr = elf.get_var_addrs('TestStructArrayVar1.level1_2.level2_1.levle3_2.level4_2.Filed1.filed3')
print(var_addr)
var_addr = elf.get_var_addrs('TestStruct5Var[1].TestUnionArrayLevel1TypeMem[3].level1_1.level2_2.levle3_1.level4_1.level5_2[1]')
print(var_addr)
enum_info = elf.get_enum_info('TestEnumAType')
```


### Supported variable types
- structure 
- structure array
- structure array filed 
- array


### Todos

 - 
 - 
 
 

License
----

MIT


