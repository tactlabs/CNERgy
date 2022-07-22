from cgitb import text
from crypt import methods
from unittest import result

import requests
from werkzeug.utils import  secure_filename
from flask import Flask, request, send_file
from flask_cors import cross_origin
import os
import json


app = Flask(__name__)


@app.route('/',methods=['GET'])
def ping():
    return  {
        'message'   :   'ping received'
    }


@app.route('/train',methods=['POST'])
@cross_origin()
def train():

    # print(request.json)
    text    =   request.json['text']
    text    =   text.lower()
    # tagged_words   =   [
    #     'Machine Learning',
    #     'Stan',
    #     'Jags',
    #     'WinBugs',
    #     'federally',
    #     'companies'
    # ]
    with open('./common/words.json') as jsonfile:
        data = json.load(jsonfile)

        words    =   data['words']
        print(words)
        tagged_words    =   []

        for idx in range(len(words)):
            word    =   words[idx]
            word    =   word.lower()
            print(word)
            if(word in text):
                text    =   text.replace(word,f'<mark>{word}</mark>')
                tagged_words.append(word)


   

    '''
    '''


    result  =   {
            'status'    :   'success'
    }

    res_dict    =   {
        'text'          :   text,
        'tagged_words'  :   tagged_words
    }

    res_json    =   json.dumps(res_dict)

    with open("./common/data.json", "w") as out_file:
        out_file.write(res_json)
    return result


@app.route('/get/annotation',methods=['GET','POST'])
@cross_origin()
def get_annotation():
    
    with open('./common/data.json') as jsonfile:
        data = json.load(jsonfile)
        print(data)
        result  =   {
            'status'    :   'success',
            'text'      :   data['text'],
            'tagged_words'  :   data['tagged_words']
        }
        return result    
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5050, debug=True)

