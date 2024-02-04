import React, { useState } from 'react';
import{ render } from "react-dom";
import { HtmlHTMLAttributes } from 'react';

export default function FileUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isFilePicked, setIsFilePicked] = useState(false);

  const changeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsFilePicked(true);
  };

  const handleSubmission = () => {
    const formData = new FormData();

    formData.append('file', selectedFile);

    fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        console.log('Success:', result);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <div>
      <input type="file" name="file" onChange={changeHandler} />
      {isFilePicked ? (
        <div>
          <p>Filename: {selectedFile.name}</p>
          <p>Filetype: {selectedFile.type}</p>
          <p>Size in bytes: {selectedFile.size}</p>
          <p>
            lastModifiedDate:{' '}
            {selectedFile.lastModifiedDate.toLocaleDateString()}
          </p>
        </div>
      ) : (
        <p>Select a file to show details</p>
      )}
      {isFilePicked ? (
        <div>
          <button onClick={handleSubmission}>Submit</button>
        </div>
      ) : (
        ''
      )}
    </div>
  );
}

const appDiv = document.getElementById("app");
render(<FileUpload />, appDiv);
