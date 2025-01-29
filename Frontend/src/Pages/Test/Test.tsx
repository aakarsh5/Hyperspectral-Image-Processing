import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Test.css";
import UploadFolder from "../../Components/UploadFolder/UploadFolder";

const Test = () => {
  const [data, setdata] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/hello")
      .then((response) => {
        setdata(response.data.message);
      })
      .catch((error) => {
        console.error("the error is", error);
      });
  });

  return (
    <div>
      <div className="header">
        <h1>Give Sample File Which Satisfy the requirements</h1>
        <UploadFolder />
        <p>{data || "loading"}</p>
      </div>
    </div>
  );
};

export default Test;
