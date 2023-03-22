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
    messages=[{"role": "system", 'content':'You are an advanced AI coding assistant that follows all instructions '
                                           'they receive. Your job is to help the user debug their code by '
                                           'explaining the error they give you in the context of the code provided. '
                                           'Then, offer the simplest potential modification to the existing code that could fix '
                                           'it while changing as little as possible. If you see other problems or '
                                           'errors in the code, explain and offer a fix for those, too. Users will '
                                           'input in the following format:\n '
                                           '### Language\n<language they are coding in>\n\n'
                                           '### Error\n<error message they have received>\n\n'
                                           '### Code\nCode snippet tht generated the error\n\n\n'
                                           'You should respond in the following format:\n'
                                           '### Explanation of error\n<an explanation of why the error occurred\n\n'
                                           '### Potential modification\n<the modification you recommend>'},
              {'role':'user', 'content':"""### Language
              {l}
              
              ### Error
              {e}
              
              ### Code
              {c}""".format(l=lang, e=error, c=code)}]

    # return """#### {f}
    #
    # ### Language
    # {l}
    #
    # ### Error
    # {e}
    #
    # ### Code
    # {c}
    #
    # ### Explanation of error""".format(f=first_line, l=lang, e=error, c=code)
    return messages


def write_code(error, code, lang):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=generate_code_prompt(error, code, lang),
        temperature=0.0,
        max_tokens=350,
        stop=[first_line, '<Done>']
    )
    # print(response)
    with open('test.txt', 'w') as out:
        out.write(str(response['choices']))
        print("\n AI insight:\n", response['choices'][0]['message']['content'])


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
