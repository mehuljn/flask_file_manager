#!/usr/local/bin/python
# Based on the Example provided in Flask Documentation

import os
import hashlib

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = '/Users/mehuljani/ProjectsData/flask_file_manager/upload_data/'
TEMP_UPLOAD_FOLDER = '/Users/mehuljani/ProjectsData/flask_file_manager/temp_upload_data/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


#Dictionary for keeping track of files and their MD5 hashes to help with duplicate detection
file_list ={}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = TEMP_UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# To keep md5 hashes of already present files in upload folder
def create_list():
    for file in os.listdir(UPLOAD_FOLDER):
        md5sum=md5(os.path.join(UPLOAD_FOLDER, file))
        file_list[md5sum]=file 

@app.route('/list')
def list():
    uploaded_files=os.listdir(UPLOAD_FOLDER)
    return render_template( 'list.html',uploaded_items=uploaded_files)
        
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

@app.route('/uploads/<filename>')
def uploaded_file_complete(filename):
    return render_template( 'upload_complete.html',filename=filename)

@app.route('/already_uploads/<filename>')
def already_uploaded_file(filename):
    return render_template( 'already_upload_complete.html',filename=filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            md5sum=md5(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            print md5sum
            if md5sum in file_list.keys():
                  os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                  return redirect(url_for('already_uploaded_file',filename=file_list[md5sum]))
            else:
                  os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename),os.path.join(UPLOAD_FOLDER, filename))
                  print "file saved"
                  file_list[md5sum]=filename
                  return redirect(url_for('uploaded_file_complete',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <table>
    <tr><td><a href=/list>List Uploaded files</a></td></tr>
    </table>
    '''


if __name__ == '__main__':
    create_list()
    app.run()
# Just the run the application as python app.py
