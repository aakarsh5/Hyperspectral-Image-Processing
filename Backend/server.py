from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from model.PrepareData import prepare  # Importing the function directly

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "files" not in request.files:
            return jsonify({"error": "No files found"}), 400

        files = request.files.getlist("files")
        if not files:
            return jsonify({"error": "No files uploaded"}), 400

        # Extract folder name from the first file (without extension)
        first_file_name = secure_filename(files[0].filename)
        folder_name, _ = os.path.splitext(first_file_name)  # Extract name without extension
        folder_path = os.path.join(app.config["UPLOAD_FOLDER"], folder_name)
        os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists

        count = 0
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(folder_path, filename)
            file.save(file_path)
            count += 1

        print(f"✅ {count} files uploaded to {folder_path}")

        # Fix the path issue before passing to prepare()
        relative_folder_path = os.path.relpath(folder_path, start=os.getcwd())  # Get relative path

        # Call the function with the corrected path
        result = prepare( folder_name)

        return jsonify({
            "message": f"Successfully uploaded {count} files",
            "folder_name": folder_name,
            "features": result["features"],
            "binary_mask_path": result["binary_mask_path"]
        }), 200

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
