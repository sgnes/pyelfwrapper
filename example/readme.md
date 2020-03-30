# How to generate the "test_var.txtdatafile.txt"
script 'var_to_cmm.py' will read content from test_var.txt and generate a cmm file, run this cmm script in [trace32](https://trace32.software.informer.com/), trace32 will generate the 'test_var.txtdatafile.txt' which has the variable name and address information, in test.py it will read and compare it.
# note:
trace32 can run in simulator mode, load the elf, run the generated cmm file
