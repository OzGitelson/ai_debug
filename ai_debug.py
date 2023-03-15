import os

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

first_line="#### Explain why the error message is occuring in the code given, what line it is occuring at, and give a potential modification to the existing code that could fix it"

def generate_code_prompt(error, code):
    return """{f}

    ### Error
    {e}

    ### Code
    {c}

    ### Explanation of error""".format(f=first_line, e=error, c=code)

def write_code(error, code):
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=generate_code_prompt(error, code),
        temperature=0.0,
        max_tokens=350,
        stop=first_line
    )
    # print(response)
    with open('test.txt', 'w') as out:
        out.write(response['choices'][0]['text'])
        print("\n AI insight:\n", response['choices'][0]['text'])


def debug(error, code):
    with open('stderr_reader.py', 'r') as infile:
        code = '\n'.join(infile.readlines())
        # openai.api_key = KEY
        # openai.api_key = os.environ.get("OPENAI_API_KEY")
        write_code(error, code)
