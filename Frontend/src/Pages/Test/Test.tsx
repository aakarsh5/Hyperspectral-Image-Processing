import React from "react";
import "./Test.css";
import UploadFolder from "../../Components/UploadFolder/UploadFolder";

const Test = () => {
  return (
    <div>
      <div className="header">
        <h3>Give Sample File Which Satisfy the requirements</h3>
        <UploadFolder />
        {/* <p>{data || "loading"}</p> */}
      </div>
    </div>
  );
};

export default Test;
