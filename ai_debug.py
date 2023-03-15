import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

first_line = "You are a helpful AI coding assistant that follows all instructions they receive exactly." \
             "Explain why the specific error message supplied in Error is occurring in the code given" \
             " and give a potential modification to the existing code that could fix it while changing as little as " \
             "possible. Ignore all code expect for the lines that produced the supplied error message. The error " \
             "message in Error will give the line number that the error is occurring at. before moving " \
             "on to subsequent errors, print '<Done>'. Here is an example of what a response should look like for an " \
             "error message at line n:\n" \
             "### Explanation of error\n" \
             "*explain error at line n*\n\n" \
             "### Modification\n" \
             "*give modification*\n" \
             "<Done>"


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
        stop=[first_line, '<Done>']
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
