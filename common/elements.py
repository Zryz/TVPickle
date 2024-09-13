

def result_text_render(input:dict):
    r = ''
    for key, val in input.items():
        if not isinstance(val, str):
            val = str(val)
        r += key + " : " + val + '\n'
    return r