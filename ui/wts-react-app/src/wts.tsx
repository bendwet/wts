/* eslint-disable no-use-before-define */
/* eslint-disable react/button-has-type */
/* eslint-disable no-console */
import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function ChooseFile() {
  // image passed into API
  const [imageFile, setImage] = useState<any>(null);
  // image to be displayed to user
  const [imageUrl, setImageUrl] = useState<any>(null);
  const [imagePrediction, setImagePrediction] = useState<any>(null);

  const changeHandler = (event: any) => {
    const predictImage = event.target.files[0];
    setImage(predictImage);
    setImageUrl(URL.createObjectURL(predictImage));
  };

  const uploadFile = () => {
    URL.revokeObjectURL(imageUrl);

    const predictData = new FormData();
    predictData.set('file', imageFile);

    // Post image to api
    axios.post('http://localhost:5000/predict', predictData)
    // Log returned result
      .then((res) => {
        console.log(res.data);
        setImagePrediction(res.data);
      })
    // Otherwise log error
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div className="App-upload">
      <div className="App-display">
        <img src={imageUrl} alt="not found" width="300" height="300" />
      </div>
      <div className="App-prediction">
        <b>{imagePrediction}</b>
      </div>
      <input className="Choose-file" type="file" name="file" onChange={changeHandler} />
      <button className="Upload-file" onClick={uploadFile}>Upload File</button>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <header className="App-header">Write to Screen</header>
      <ChooseFile />
    </div>
  );
}

export default App;
