
from tracemalloc import start
import requests
from werkzeug.utils import  secure_filename
from flask import Flask, request, send_file, redirect
from flask_cors import cross_origin
import os
import json
import random

app = Flask(__name__)


@app.route('/',methods=['GET'])
def ping():
    return  {
        'message'   :   'ping received'
    }


@app.route('/predict',methods=['POST'])
@cross_origin()
def train():

    text    =   request.json['text']
    result  =  {
        "content"   :   text,
        "keys"      :   []
    }
    text      =   text.lower()
    with open('./common/words.json') as jsonfile:
        data = json.load(jsonfile)

        words    =   data['words']
        print(words)

        for  word in words:
            word    =   word.lower()
            print(f"word {word} index {text.find(word)}")
            try:
                if(text.index(word)):
                    start           =   text.index(word)
                    random_color    =    ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0]
                    result['keys'].append(
                        {

                        
                            'tech':{
                                word     :   [start,start+len(word)],
                                "color"  :    random_color
                            }
                        }
                    )
            except  ValueError as e:
                print(e) 
        res_json    =   json.dumps(result)

        with open("./common/data.json", "w") as out_file:
            out_file.write(res_json)   
        
        return {
            'status'    :   'success'
        }

   

    # '''
    # '''


    # result  =   {
    #         'status'    :   'success'
    # }

    # res_dict    =   {
    #     'text'          :   text,
    # }

    # res_json    =   json.dumps(res_dict)

    # with open("./common/data.json", "w") as out_file:
    #     out_file.write(res_json)
    # return res_dict


@app.route('/get/annotation',methods=['GET','POST'])
@cross_origin()
def get_annotation():
    
    with open('./common/data.json') as jsonfile:
        data = json.load(jsonfile)
        print("data",data)
        result  =   {
            'status'    :   'success',
            'content'      :   data['content'],
            'keys'  :   data['keys']
        }
        return result
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5050, debug=True)

