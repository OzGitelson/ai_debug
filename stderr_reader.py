import sys
from subprocess import Popen, PIPE, STDOUT
import re
import ai_debug

FOV=5

if len(sys.argv)<3:
    print("Invalid command args")
    exit(1)

command=sys.argv[1]
lang=sys.argv[2]

lang_dic={
    'python':".py",
    'C':".c",
    'C++':'.cpp'

}

if lang not in lang_dic:
    print("Invalid language")
    exit(1)

# sub = Popen([r"C:\python projects\openai_api_test\ai_debug\venv\Scripts\python.exe", path_to_python], stdout=PIPE, stderr=PIPE)
sub = Popen(command.split(" "), stdout=PIPE, stderr=PIPE)

output, error_output = sub.communicate()

error_output=error_output.decode('utf_8')

line_reg=re.compile('([^\n"]+{ext})[^\n0-9]+([0-9]+)'.format(ext=lang_dic[lang]))

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
        ai_debug.debug(error_output, code_to_send, lang)
else:
    print("No errors detected!")



