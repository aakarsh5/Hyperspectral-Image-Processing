import React, { useState } from "react";
import axios from "axios";
import "./UploadFolder.css";

const UploadFolder = () => {
  const [files, setFiles] = useState([]);

  const handleChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
  };

  const handleSubmit = async () => {
    // if (files.length() === 0) {
    //   alert("Please select a folder");
    //   return;
    // }
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      alert("Uploaded Sucessfully");
    } catch (error) {
      console.error("Error occured", error);
      alert("Folder upload failed");
    }
  };

  return (
    <div className="input">
      <input
        type="file"
        webkitdirectory="true"
        directory=""
        multiple
        onChange={handleChange}
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default UploadFolder;
