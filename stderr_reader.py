import sys
from subprocess import Popen, PIPE, STDOUT
import re
import ai_debug

FOV=10

if len(sys.argv)<2:
    print("Invalid command args")
    exit(1)

path_to_python=sys.argv[1]

sub = Popen([r"C:\python projects\openai_api_test\openai-quickstart-python\venv\Scripts\python.exe", path_to_python], stdout=PIPE, stderr=PIPE)
output, error_output = sub.communicate()

error_output=error_output.decode('utf_8')

line_reg=re.compile(r'File "([^\n]+)", line ([0-9]+)')

first_error=line_reg.search(error_output)

if first_error is not None:
    print("Errors:\n", error_output)
    line=int(first_error[2])
    error_path=first_error[1]
    code_to_send=''
    with open(error_path, 'r') as read:
        for i, l in enumerate(read.readlines()):
            if line-FOV<=i<=line+FOV:
                code_to_send+=l

        # print(code_to_send)
        ai_debug.debug(error_output, code_to_send)
else:
    print("No errors detected!")



