import datetime
from flask import Flask,url_for,render_template, jsonify, request, redirect
from flask.globals import session
from flask.helpers import send_file, send_from_directory
from werkzeug.utils import  secure_filename
import json ,os
import pprint
import requests
import zipfile
import hashlib
import session_utils
from dotenv import load_dotenv

load_dotenv()

from flask_bcrypt import Bcrypt

from pymongo import MongoClient


bcrypt = Bcrypt()


app=Flask(__name__)


app.secret_key = 'smite$me$oh$mighty$smiter'

SESSION_ID_KEY  = "sid"


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CHECKSUM_FOLDER'] = 'static/uploads'


def get_mongo_uri():
    
    mongo_uri = os.environ['MONGO_URI']
    # print(mongo_uri)

    return mongo_uri

F12R_MONGO_URI = get_mongo_uri()

# creating a MongoClient object  
client = MongoClient(F12R_MONGO_URI)  

# accessing the database  
DB_NAME = 'cner_dev'
database = client[DB_NAME]

c12_annotators = database['c12_annotators']
c12_batches = database['c12_batches']
c12_clusters = database['c12_clusters']
c12_files = database['c12_files']
c12_pages = database['c12_pages']
c12_annotations = database['c12_annotations']



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_annotator_id():

    return session["annotator_id"]

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

        print(file.filename)
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
        path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        f = open(path , "r")
        # words = f.read()
        file_list = f.read().split(delimiter)
    
        app.config[request.remote_addr] = file_list
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

    # pprint.pprint(res_list)
    for ner in keys_data:
        # print(keys_data[ner])
        for select in keys_data[ner]:

            prev = False
            prev_value = None
            token_start = None
            token_end = None
            selected_words = select.split()
            # print(select,selected_words)
            hit = None


            for word in selected_words:
                # print(word,keys_data[ner][select] )
                # print("word", select)
                for word2 in res_list:
                    # print(word2["start"],"--",word2["text"],"==", word, len(word2["text"]), len(word))
                    # print(res_list)

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

    # pprint.pprint(hit_list)



    ## overlap fix

    tokens = res_list
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

    res_list = new_tokens


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
    print(folder_path)
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        pass
    with open(os.path.join(folder_path, filename), 'a') as outfile:
        for entry in [one_page_data]:
            json.dump(entry, outfile)
            outfile.write('\n')
    
    with open(os.path.join(folder_path, pattern_filename), 'a') as outfile:
        for entry in pattern_data:
            # print(pattern_data)
            json.dump(entry, outfile)
            outfile.write('\n')
    
    

    return True

@app.route('/exp', methods=['GET'])
def export_files():
    filename =app.config[request.remote_addr+"-file_name"].replace(".txt",".jsonl")
    folder_path = filename.replace(".jsonl","")
    zip_name = filename.replace(".jsonl",".zip")
    print("hey",zip_name)
    # return zip_name
    with open(os.path.join(folder_path, filename),'r') as file_to_check:
                # read contents of the file
                json_l = list(file_to_check)
               
                data = (file_to_check.read()).encode('utf-8') 
                # pipe contents of the file through
                md5_returned = hashlib.md5(data).hexdigest()
                # print(file_to_check)
                # checksum_dict = {
                #         md5_returned : json_l
                # }
                # print("checksum_dicts",checksum_dict)
                with open( "checksum.json", "r+") as outfile:
                    file_data = json.load(outfile)
                    # print(checksum_dict)
                    file_data[md5_returned] = json_l
                    outfile.seek(0)
                    json.dump(file_data, outfile, indent=4)
                # app.config[md5_returned] = list(file_to_check)
                # print("md_checksum:",type(data))
                # return str(list(file_to_check))
    zipfolder = zipfile.ZipFile(zip_name,'w', compression = zipfile.ZIP_STORED) # Compression type 

    # zip all the files which are inside in the folder
    for root,dirs, files in os.walk(folder_path):
        for file in files:
            print("file:",file)
            zipfolder.write(folder_path+"/"+file)
    zipfolder.close()
    # return str(True)
    return_file = send_file(zip_name,
            mimetype = 'zip',
            attachment_filename= zip_name,
            as_attachment = True)
    os.remove(zip_name)

    return return_file

@app.route('/converter')
def converter_page():
    # files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('converter.html', files="none")

@app.route('/to_json', methods=['POST'])
def upload_files():
    file = request.files['file']
    filename = secure_filename(file.filename)

    if file :
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as json_file:
        json_list = list(json_file)

    json_dict={}
    json_count = 1

    for json_str in json_list:
        result = json.loads(json_str)
        # result = f"{result}"
        json_dict["line_"+str(json_count)] = result
        json_count+=1

    # pprint.pprint(json_dict)

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



    if file :
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename),)
    
 
    data = json.load(f)

   

    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename.replace(".json",".jsonl")), 'a') as outfile:
        for entry in data:
            # print(pattern_data)
            json.dump(data[entry], outfile)
            outfile.write('\n')

    # pprint.pprint(json_dict)

   
    return_file = send_from_directory(app.config['UPLOAD_FOLDER'],filename.replace(".json",".jsonl") , as_attachment=True)
    
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename.replace(".json",".jsonl")))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return return_file

def get_page_data_for_annotator(annotator_id):

    annotator_aggregated_data = c12_annotators.aggregate([
                                                { "$match": { "annotator_id": annotator_id } },
                                                {
                                                    "$lookup": {
                                                        "from": "c12_clusters",
                                                        "localField": "cluster_id",
                                                        "foreignField": "cluster_id",
                                                        "as": "cluster_data"
                                                    }
                                                },
                                                { "$unwind": "$cluster_data" }
                                                ])

    annotator_aggregated_data  = list(annotator_aggregated_data)[0]

    del annotator_aggregated_data['_id']

    del annotator_aggregated_data['cluster_data']['_id']

    batch_id = annotator_aggregated_data['cluster_data']['batch_id']

    batches_aggregated_data = c12_batches.find_one({ "batch_id": batch_id })

    all_files_in_batch = batches_aggregated_data['file_id']

    all_files_data = list(c12_files.find({ "file_id": { "$in": all_files_in_batch }}))

    for single_file in all_files_data:

        del single_file['_id']

        if single_file['assigned_status'] != 'completed':

            required_file_id = single_file['file_id']

            break

    all_pages_data = list(c12_pages.find({ "file_id": required_file_id}))

    for single_page in all_pages_data:

        del single_page['_id']

        if not single_page['page_status']:

            required_page_id = single_page['page_id']

            required_page_data = single_page['page_data']

            break     

    result = {
        "page_id"   : required_page_id,
        "page_data" : required_page_data
    }

    return result


## cluster stuff ###



def match_password(db_password, password):

    return bcrypt.check_password_hash(db_password, password)






@app.route('/login', methods=['GET'])
def login_page():
    
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def page_login_post():

    username = request.values.get('username')
    password = request.values.get('password')

    print(username,password)
    ###############

    collection_name = 'c12_annotators'
    new_collection = database[collection_name]

    user = new_collection.find_one({"annotator_name" : username})

    if not user:
        return "NO USER FOUND"

    if not match_password(user["password"],password):
        return "WRONG PASSWORD"

    sid = session_utils.created_sessionid(user["annotator_id"])
    session[SESSION_ID_KEY]      = sid
    session["annotator_id"]      = user["annotator_id"]
    return redirect("/dashboard")

@app.route('/dashboard', methods=['GET'])
def dash_page():
    
    return render_template("dash.html")


@app.route('/get_next_page', methods=['GET'])
def get_next_page():
    
    next_text_data = get_page_data_for_annotator(get_annotator_id())


    URL = "http://backend-service:5555/tokenize"
    
    

    # print(next_text_data)
   
    PARAMS = {'text':next_text_data["page_data"]}
    

    r = requests.post(url = URL, json = PARAMS)
    
    # extracting data in json format
    data = r.json()

    # print(data)
    return {"result" : data, "page_id" : next_text_data["page_id"] }

def get_last_annotation_id():
    last_annotation_id = c12_annotations.find().sort([('annotation_id', -1)]).limit(1)
    try:
        last_annotation_id = last_annotation_id[0]['annotation_id']
    except Exception as err:
        print("error while getting last annotation_id : ", err)
        last_annotation_id = 0

    return last_annotation_id


@app.route('/save_annotations', methods=['POST'])
def save_annotations_db():
    if request.method == "POST":
        val = request.get_json()
        print(val)
        tokenized_data = val["initial-data"]["tokens"]
        keys_data = val["selected-data"]
        page_id = val["page_id"]
        words = val["orig_text"]
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

        # pprint.pprint(res_list)
        for ner in keys_data:
            # print(keys_data[ner])
            for select in keys_data[ner]:

                prev = False
                prev_value = None
                token_start = None
                token_end = None
                selected_words = select.split()
                # print(select,selected_words)
                hit = None


                for word in selected_words:
                    # print(word,keys_data[ner][select] )
                    # print("word", select)
                    for word2 in res_list:
                        # print(word2["start"],"--",word2["text"],"==", word, len(word2["text"]), len(word))
                        # print(res_list)

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

        # pprint.pprint(hit_list)



        ## overlap fix

        tokens = res_list
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

        res_list = new_tokens


        one_page_data = {
            "text"      : words,
            "meta"      : {"section":"tech_keys"},
            "_input_hash": 1922477360,
            "_task_hash": 508078126,
            "tokens"    : res_list,
            "spans"     : hit_list,
            "answer"    : "accept"
            }
        
        annotation_data = {
            "annotation_id" : get_last_annotation_id() + 1,
            "annotator_id"  : get_annotator_id(),
            "annotation_data" : one_page_data,
            "page_id"       : page_id,
            "created_at"    : datetime.datetime.now(),
            "updated_at"    : datetime.datetime.now()
        }

        c12_annotations.insert_one(annotation_data)

        return "True"




@app.route('/annotator', methods=['GET'])
def annotator_new():

    # page_data = get_page_data_for_annotator(int(session["annotator_id"]))
    
    # tokenized_data = 
    return render_template("annotator_new.html")

@app.route('/tester', methods=['GET','POST'])
def tester():

    result = {
        "ping" : get_page_data_for_annotator(annotator_id = 3)
    }
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



