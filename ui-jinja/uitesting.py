from flask import Flask,url_for,render_template, jsonify, request, redirect
from flask.helpers import send_file, send_from_directory
from werkzeug.utils import  secure_filename
import json
import shutil


# with open( "checksum.json", "r+") as outfile:
#     print(outfile)
#     file_data = json.load(outfile)
#     print(f'this is checksom file data : {file_data}')
#     outfile.seek(0)
#     json.dump(file_data, outfile, indent=4)

dir_name = 'test'
output_filename = 'something'
shutil.make_archive(output_filename, 'zip', dir_name)