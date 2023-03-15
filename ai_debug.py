import os

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

first_line="Explain why the error message is occurring in the code given, what line it is occurring at, " \
           "and give a potential simple modification to the existing code that could fix it. Only explain the error in the " \
           "code that led to the Error, and ignore any other errors you might see in the code"

def generate_code_prompt(error, code, lang):
    return """#### {f}
    
    ### Language
    {l}
    
    ### Error
    {e}

    ### Code
    {c}

    ### Explanation of error""".format(f=first_line, l=lang, e=error, c=code)

def write_code(error, code, lang):
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=generate_code_prompt(error, code, lang),
        temperature=0.0,
        max_tokens=350,
        stop=[first_line, '```\n']
    )
    # print(response)
    with open('test.txt', 'w') as out:
        out.write(response['choices'][0]['text'])
        print("\n AI insight:\n", response['choices'][0]['text'])


def debug(error, code, lang):
    # error="""
    # test.c:1:7: error: expected declaration specifiers or ‘...’ before string constant
    # 1 | print("hello world");
    #   |       ^~~~~~~~~~~~~
    # make: *** [makefile:26: Test] Error 1
    # """
    #
    # code = 'print("hello world");'
        # openai.api_key = KEY
        # openai.api_key = os.environ.get("OPENAI_API_KEY")
    write_code(error, code, lang)
