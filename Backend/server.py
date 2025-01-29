from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

#initialize app
app = Flask(__name__)
CORS(app)  #cors for cross origin request

#to upload files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok = True)

#route to upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error':'No file found'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'No file selected'})
    
    #save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    file.save(filepath)

    return jsonify({'message': 'File upload successfully','filepath':filepath})

@app.route('/hello',methods=['GET'])
def hello():
    return jsonify({'message':"Hello world"})

@app.route('/upload',methods=['POST'])
def upload():
    if "files" not in request.files:
        return jsonify({"error": "No files found"}),400
    
    files = request.files.getlist("files")
    
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER,file.filename)
        file.save(file_path)
    
    return jsonify({"message":"Folder Uploaded","file_count":len(files)})
    

if __name__ == '__main__':
    app.run(debug=True)