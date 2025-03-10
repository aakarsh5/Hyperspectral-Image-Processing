from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
from werkzeug.utils import secure_filename
from model.PrepareData import prepare

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    if "files" not in request.files:
        return jsonify({"error": "No files found from"}), 400

    folder_name = request.form.get("folderName", "1600")  # Get folder name from request
    folder_path = os.path.join(app.config["UPLOAD_FOLDER"], folder_name)
    print(folder_name)
    # prepare(folder_name)
    print(folder_path)
    os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists

    files = request.files.getlist("files")
    count = 0

    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(folder_path, filename)
        file.save(file_path)
        count += 1
        # print(count)

    # Call PrepareData.py with the folder name
    subprocess.run(["python", "model/PrepareData.py", folder_name])

    return jsonify({"message": f"Successfully uploaded {count} files to {folder_name}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
