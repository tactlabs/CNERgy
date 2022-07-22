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
    with open('./words/words.json') as jsonfile:
        data = json.load(jsonfile)

        words    =   data['words']
        print(words)

        for idx in range(len(words)):
            word    =   words[idx]
            word    =   word.lower()
            print(word)
            if(word in text):
                text    =   text.replace(word,f'<mark>{word}</mark>')


    # file    =   open('./collection.txt')
    # # lines=[]
    # # for line in file:
    # #     lines.append(line.strip())
    # file_list   =   file.read().split('-----------------------------------------------------------------------')
    # print(file_list)

    # print(lines)
    # highlight_words =   []

    # for line in file_list:
    # line    =   text.split(',')
    # for idx in range(len(line)):
    #     word    =   line[idx]
    #     # print(word)
    #     if(word in tagged_words):
    #         word    =   f'<mark class="mark">{word}</mark>'
    #         line[idx] = word
    #         print(word)

    # for idx in range(len(file_list)):
    #     line    =   text[idx]
    #     for word in line.split(' '):
    #         if(word in words):
    #         # highlight_words.append(word)
    #             word    =   f'<mark id="mark {idx}"></mark>'

      
  

    '''
    '''


    result  =   {

        'text'              :   text
    }

    return result


@app.route('/annotation',methods=['GET','POST'])
def get_annotation():
    
    
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5050, debug=True)

