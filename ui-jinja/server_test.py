from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer
from flask import Flask,url_for,render_template, jsonify, request, redirect
from flask.helpers import send_file, send_from_directory
from werkzeug.utils import  secure_filename
import json ,os
import shutil
import nltk

app=Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CHECKSUM_FOLDER'] = 'static/uploads'
app.config['SAVED_ANNOTATIONS'] = []



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/tokenize", methods=["POST"])
def tokenize():
    print("This is from tokenize func")
    print(request.json)
    text = request.json["text"]
    try:
        spans = list(TreebankWordTokenizer().span_tokenize(text))
    except LookupError:
        nltk.download('punkt')
        spans = list(TreebankWordTokenizer().span_tokenize(text))
    return {"tokens": [(s[0], s[1], text[s[0]:s[1]]) for s in spans]}


@app.route("/detokenize", methods=["POST"])
def detokenize():
    tokens = request.json["tokens"]
    return {"text": TreebankWordDetokenizer().detokenize(tokens)}


@app.route('/',methods=['GET','POST'])
def base():
    return render_template('home_new.html')

@app.route('/view',methods=['GET'])
def home():
    data = app.config[request.remote_addr]
    
    return render_template('index.html' , data = data)


@app.route('/api/save/data', methods=['POST'])
def save():
    if request.method == "POST":
        val = request.get_json()

        filename =app.config[request.remote_addr+"-file_name"].replace(".txt",".jsonl")
        print(filename)
        save_file(val["initial-data"]["tokens"],val["selected-data"], val["orig_text"], filename)

        return jsonify(val)


def save_file(tokenized_data, keys_data , words, filename):

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
    pattern_data = []

    for ner in keys_data:
        for select in keys_data[ner]:

            prev = False
            prev_value = None
            token_start = None
            token_end = None
            selected_words = select.split()
            hit = None
            for word in selected_words:
                for word2 in res_list:
                    if (word2["start"] == keys_data[ner][select] and prev == False) or (word in word2["text"] and prev == True and word2 == ( res_list[res_list.index(prev_value)+1])):
                        print("yes",word2)
                        hit = word2
                        if prev == False:
                            token_start = word2["id"]
                            pattern_data.append({"label": ner ,"pattern":[{"lower": select.lower()}]})
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

    print(f'hit list in save file : {hit_list}')
    one_page_data = {
        "text" : words,
        "meta" : {"section":"tech_keys"},
        "_input_hash":1922477360,
        "_task_hash":508078126,
        "tokens" : res_list,
        "spans" : hit_list,
        "answer":"accept"
        }
    pattern_filename = filename.replace(".jsonl","_pattern.jsonl")
    folder_path = filename.replace(".jsonl","")
    if 'ui-jinja' not in os.getcwd():
        folder_path = os.path.join('ui-jinja', folder_path)
    print(f'this is from save files : ', folder_path)
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        pass
    # saving a tokenized uploade file 
    with open(os.path.join(folder_path, filename), 'a') as outfile:
        print('this is inside the save file func')
        print(outfile)
        print(one_page_data)
        for entry in [one_page_data]:
            json.dump(entry, outfile)
            outfile.write('\n')
    # saving a pattern for tokenization
    with open(os.path.join(folder_path, pattern_filename), 'a') as outfile:
        for entry in pattern_data:
            json.dump(entry, outfile)
            outfile.write('\n')
    
    return True


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print("File Upload")
        # check if the post request has the file part
        if 'file' not in request.files:
            
            return redirect(request.url)
        file = request.files['file']
        delimiter = request.values.get('delimiter')

        print('this is from upload files : ', file.filename)
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            curr_working_dir = os.getcwd() 
            save_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if 'ui-jinja' not in curr_working_dir:
                save_file_path = os.path.join('ui-jinja', save_file_path)
            
            print(curr_working_dir)
            print(f"full file path from uploads : {save_file_path}")
            file.save(save_file_path)
    
        path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        if 'ui-jinja' not in os.getcwd():
                path = os.path.join('ui-jinja', path)
        print(f'printing the path of the filename : {path}')
        f = open(path , "r")
        file_list = f.read().split(delimiter)
        app.config[request.remote_addr] = file_list
        print(f'file list/remote addr {app.config[request.remote_addr]} | also the type is : {type(file_list)} | delimiter : {delimiter}')
        app.config[request.remote_addr+"-file_name"] = filename

        return redirect(url_for('home',file_name = filename))


@app.route('/export', methods=['GET'])
def export_files():
    print('''
*****************************************************************************************8

               we are here in export files 
   
*****************************************************************************************8
''')
    filename =app.config[request.remote_addr+"-file_name"].replace(".txt",".jsonl")
    folder_path = filename.replace(".jsonl","")
    if 'ui-jinja' not in os.getcwd():
        folder_path = os.path.join('ui-jinja', folder_path)
    zip_name = filename.replace(".jsonl",".zip")
    print("hey",zip_name)   
    print('hey', folder_path)
    print('hey', filename)

    shutil.make_archive(folder_path, 'zip', folder_path)
    return_file = send_file(zip_name,
            mimetype = 'zip',
            attachment_filename= zip_name,
            as_attachment = True)

    try:
        os.remove(os.path.join('ui-jinja', zip_name))
        shutil.rmtree(folder_path)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], app.config[request.remote_addr+"-file_name"]))
    except Exception as err:
        print(err)
    
    print(return_file)
    return return_file 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060, debug=True)