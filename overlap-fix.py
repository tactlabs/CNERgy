# from typing import Dict
# import pandas as pd 
import json 


def get_tokens(text):
    tokens = text['tokens']
    leng = len(tokens)
    new_tokens = []
    for tok in range(leng):

        prev_token = tokens[tok - 1] if tok > 0 else {'start' : -1, 'end' : -1}
        curr_token = tokens[tok]
        if curr_token['start'] == prev_token['end']:
            prev_diff = prev_token['end'] - prev_token['start']
            curr_diff = curr_token['end'] - curr_token['start']
            if curr_diff > prev_diff:
                new_tokens.append(curr_token)
        else:
            new_tokens.append(curr_token)

    text['tokens'] = new_tokens
    return text


def startpy():
    with open('testingFile.json') as file:
        jobs = json.load(file)

    tokens = get_tokens(jobs)
    print(tokens)

    with open('testingFile2.json', 'w') as file:
        json.dump(tokens, file)


if __name__ == "__main__":
    startpy()