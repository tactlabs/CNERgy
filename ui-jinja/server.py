from flask import Flask,url_for,render_template, jsonify, request, redirect
from werkzeug.utils import  secure_filename
import json ,os
import pprint
import requests


app=Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET','POST'])
def base():
    return render_template('home.html')

@app.route('/view',methods=['GET'])
def home():
    # data = read_json()
    data = app.config[request.remote_addr]
    
    return render_template('index.html' , data = data)


@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        print("File Upload")
        # check if the post request has the file part
        if 'file' not in request.files:
            
            return redirect(request.url)
        file = request.files['file']
        delimiter = request.values.get('delimiter')
        # print(delimiter)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        f = open(path , "r")
        # words = f.read()
        file_list = f.read().split(delimiter)

        app.config[request.remote_addr] = file_list

        return redirect(url_for('home',file_name = filename))



# @app.route('/json',methods=['GET','POST'])
def read_json():
    f = open("data.txt" , "r")
    words = f.read()
    # words = f.read().split()


    dictToSend = {'text':words}
    res = requests.post('http://127.0.0.1:5555/tokenize', json=dictToSend)

    dictFromServer = res.json()
    post_result = dictFromServer

    # i=0
    # id = 1000
    # data = []
    # for word in words:
    #     temp = {}
    #     temp["text"] = word + " "
    #     temp["start"] = i
    #     temp["id"] = id
    #     for letter in word:
    #         i+=1
    #     temp["end"] = i
    #     i+=1
    #     id+=1
    #     data.append(temp)
    # pprint(data)
    # pprint.pprint(post_result)
    return post_result
    # return jsonify(data)

@app.route('/api/save/data', methods=['POST'])
def save():
    if request.method == "POST":
        val = request.get_json()
        # for i in val['uniqueSelectedText']:
        #     i['text'] = i['text'].split('\n')

        pprint.pprint(val)
        # res = data.update_record(val)
        save_file(val["initial-data"]["tokens"],val["selected-data"])
        return jsonify(val)

def save_file(tokenized_data, keys_data ):


    f = open("data.txt" , "r")
    words = f.read()
    print(type(words))

    # keys_data = {
    #     "tech": {"execution and delivery":922,"Deep Learning":1643},
    #     "location" : {"Toronto":128}
    # }

    # res = {}

    # dictToSend = {'text':words}
    # res = requests.post('http://127.0.0.1:5555/tokenize', json=dictToSend)

    # dictFromServer = res.json()
    # post_result = dictFromServer
    # # print(dictFromServer)

    count = 0
    res_list = []
    hit_list = []
    for word in tokenized_data:

        data = {
            "text" : word[2],
            "start" : word[0],
            "end" : word[1],
            "id" : count
        }

        

        res_list.append(data)
        count+=1

    # pprint.pprint(res_list)
    for ner in keys_data:

        for select in keys_data[ner]:

            prev = False
            prev_value = None
            token_start = None
            token_end = None
            selected_words = select.split()
            hit = None

            for word in selected_words:
                # print(word,keys_data[ner][select] )
                for word2 in res_list:
                    # print(word2["start"],"--",word2["text"],"==", word, len(word2["text"]), len(word))
                    # print(res_list)

                    if (word2["start"] == keys_data[ner][select] and prev == False) or (word in word2["text"] and prev == True and word2 == ( res_list[res_list.index(prev_value)+1])):
                        print("yes",word2)
                        hit = word2
                        if prev == False:
                            token_start = word2["id"]
                        else:
                            token_end = word2["id"]
                        prev_value = word2
                        prev=True
                        break
            
            if not token_end:
                token_end = token_start

            data = {
                "start" : word2["start"],
                "end" : word2["end"],
                "token_start" : token_start,
                "token_end" : token_end,
                "label" : ner
                }
            
            hit_list.append(data)

    pprint.pprint(hit_list)

    one_page_data = {
        "text" : words,
        "meta" : {"section":"tech_keys"},
        "_input_hash":1922477360,
        "_task_hash":508078126,
        "tokens" : res_list,
        "spans" : hit_list,
        "answer":"accept"
        }
    # one_page_data = [json.dumps(one_page_data)]
    # dump_jsonl([one_page_data],"output.jsonl")
    print(type(one_page_data))
    with open('output.jsonl', 'w') as outfile:
        for entry in [one_page_data]:
            json.dump(entry, outfile)
            outfile.write('\n')


@app.route('/api/tokenize_data', methods=['POST'])
def tokenize_data():
    val = request.json['data']
    # for i in val['uniqueSelectedText']:
    #     i['text'] = i['text'].split('\n')

    print(val)
    # res = data.update_record(val)
    # save_file(val["initial-data"]["tokens"],val["selected-data"])
    return jsonify(val)

if __name__ == '__main__':
    app.run(debug=True)


