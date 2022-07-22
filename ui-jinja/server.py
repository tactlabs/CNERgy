from flask import Flask,url_for,render_template, jsonify, request, redirect
from flask.helpers import send_file, send_from_directory
from werkzeug.utils import  secure_filename
import json ,os
import zipfile
import shutil
from time import sleep

app=Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CHECKSUM_FOLDER'] = 'static/uploads'
app.config['SAVED_ANNOTATIONS'] = []



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET','POST'])
def base():
    return render_template('home_new.html')

@app.route('/view',methods=['GET'])
def home():
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

        print('this is from upload files : ', file.filename)
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
        path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        print(f'printing the path of the filename : {path}')
        f = open(path , "r")
        file_list = f.read().split(delimiter)
        app.config[request.remote_addr] = file_list
        print(f'file list/remote addr {app.config[request.remote_addr]}')
        app.config[request.remote_addr+"-file_name"] = filename

        return redirect(url_for('home',file_name = filename))



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
            print(entry)
            json.dump(entry, outfile)
            outfile.write('\n')
    
    return True

@app.route('/delExport', methods = ['GET'])
def deleteFile():
    sleep(3)
    base_path =  'static/uploads/'
    all_files = os.listdir(base_path)
    try:
        for file in all_files:
            os.remove(base_path + file)

        return jsonify({'success' : 200})
    except:
        return jsonify({'error' : 404})

@app.route('/exporto', methods=['GET'])
def export_files():
    
    filename = app.config[request.remote_addr+"-file_name"].replace(".txt",".jsonl")
    dirname = filename.replace(".jsonl","")
    base_path =  'static/uploads/'
    zip_name = filename.replace(".jsonl",".zip")
    

    zipfolder = zipfile.ZipFile(base_path + zip_name,'w', compression = zipfile.ZIP_STORED) # Compression type 

    for root,dirs, files in os.walk(dirname):
        for file in files:
            print("file:",file)
            zipfolder.write(dirname + "/" + file)
    zipfolder.close()

    try:
        shutil.rmtree( dirname )
        os.remove( base_path + app.config[request.remote_addr+ "-file_name"])
    except Exception as err:
        print(err)
    
    return jsonify({'success' : 200})



@app.route('/to_json', methods=['POST'])
def upload_files():
    file = request.files['file']
    filename = secure_filename(file.filename)

    if file :
            filename = secure_filename(file.filename)
            print("This is from upload files" , filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as json_file:
        json_list = list(json_file)
        print(json_list)
    json_dict={}
    json_count = 1

    for json_str in json_list:
        result = json.loads(json_str)
        json_dict["line_"+str(json_count)] = result
        json_count+=1

    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename.replace(".jsonl",".json")), "w") as outfile:
        json.dump(json_dict, outfile, indent=4)

    return_file = send_from_directory(app.config['UPLOAD_FOLDER'],filename.replace(".jsonl",".json") , as_attachment=True)

    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename.replace(".jsonl",".json")))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return return_file


@app.route('/to_jsonl', methods=['POST'])
def to_jsonl_file():
    file = request.files['json_file']
    filename = secure_filename(file.filename)

    print('herer in jsonl func')
    print(f'filenae : {filename}')
    print(f'file : {file}')

    if file :
            filename = secure_filename(file.filename)
            print('inside some to jsonl func ', filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename),)
    
 
    data = json.load(f)

    print(f'inside jsonl data : {data}')

    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename.replace(".json",".jsonl")), 'a') as outfile:
        for entry in data:
            json.dump(data[entry], outfile)
            outfile.write('\n')

    return_file = send_from_directory(app.config['UPLOAD_FOLDER'],filename.replace(".json",".jsonl") , as_attachment=True)
    
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename.replace(".json",".jsonl")))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return return_file


@app.route('/gettag', methods=['GET'])

def _():
    return render_template('dummy.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)





# ============================================== unused code =============================================


# @app.route('/converter')
# def converter_page():
#     return render_template('converter.html', files="none")

# with open(os.path.join(folder_path, filename),'r') as file_to_check:
    #             json_l = list(file_to_check)
    #             data = (file_to_check.read()).encode('utf-8') 
    #             md5_returned = hashlib.md5(data).hexdigest()
    #             with open("checksum.json", "r+") as outfile:
    #                 print(outfile)
    #                 print(json_l)
    #                 file_data = json.load(outfile)
    #                 file_data[md5_returned] = json_l[-1]
    #                 print(f'this is checksom file data : {file_data}')
    #                 outfile.seek(0)
    #                 json.dump(file_data, outfile, indent=4)

    # zipfolder = zipfile.ZipFile(zip_name,'w', compression = zipfile.ZIP_STORED) # Compression type 

    # zip all the files which are inside in the folder
    # for root,dirs, files in os.walk(folder_path):
    #     for file in files:
    #         print("file:",file)
    #         zipfolder.write(folder_path+"/"+file)
    # zipfolder.close()