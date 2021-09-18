from flask import Flask,url_for,render_template, jsonify
import json
from pprint import pprint

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    data = read_json()
    return render_template('index.html' , data = data)

# @app.route('/json',methods=['GET','POST'])
def read_json():
    f = open("data.txt" , "r")
    words = f.read().split()

    i=0
    data = []
    for word in words:
        temp = {}
        temp["text"] = word + " "
        temp["start"] = i
        for letter in word:
            i+=1
        temp["end"] = i
        i+=1
        data.append(temp)
    pprint(data)
    return data
        

    # return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)