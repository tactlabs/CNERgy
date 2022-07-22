from flask import Flask,url_for,render_template, jsonify, request, redirect
from flask.helpers import send_file, send_from_directory
from werkzeug.utils import  secure_filename
from time import sleep

app=Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return redirect('/gettag')



@app.route('/get/data', methods=['GET'])
def get_paragraph():
    return render_template('dummy.html')


@app.route('/view/tag/data', methods=['GET'])
def get_taggged_data():
    return render_template('dummy.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060, debug=True)





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