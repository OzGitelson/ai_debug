import sys
import stderr_reader

if len(sys.argv) < 3:
    print("Invalid command args")
    exit(1)

command = sys.argv[1]
lang = sys.argv[2]

lang_dic = {
    'python': ".py",
    'C': ".c",
    'C++': '.cpp'
}

if lang not in lang_dic:
    print("Invalid language")
    exit(1)

stderr_reader.run_program(command, lang, lang_dic[lang])