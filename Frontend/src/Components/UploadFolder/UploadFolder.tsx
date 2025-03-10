import React, { useState } from "react";
import axios from "axios";
import "./UploadFolder.css";

const UploadFolder = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [folderName, setFolderName] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files as FileList);

    if (selectedFiles.length > 0) {
      const firstFilePath = selectedFiles[0].webkitRelativePath;
      const folder = firstFilePath.split("/")[0]; // Extract folder name
      setFolderName(folder);
    }

    setFiles(selectedFiles);
  };

  const handleSubmit = async () => {
    if (files.length === 0) {
      alert("Please select a folder first!");
      return;
    }

    const formData = new FormData();
    formData.append("folderName", folderName); // Include folder name
    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      console.log(response.data);
      alert(`Folder "${folderName}" uploaded successfully!`);
    } catch (error) {
      console.error("Error uploading folder:", error);
      alert("Upload failed.");
    }
  };

  return (
    <div className="input">
      <input
        type="file"
        ref={(input) => input && (input.webkitdirectory = true)}
        multiple
        onChange={handleChange}
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default UploadFolder;
