import sys

if len(sys.argv) == 2:
    file_name = sys.argv[1]
else:
    file_name = r'var_real.txt'
with open(file_name) as var_file:
    cmm_file = open(file_name+'.cmm', 'w')
    cmm_file.write("open #1 {0}datafile.txt /Create \r\n".format(file_name))
    for line in var_file:
        cmm_file.write("write #1 \"{0}:\" Var.ADDRESS({0})\r\n".format(line.strip()))
    cmm_file.write("close #1 \r\n")
cmm_file.close()