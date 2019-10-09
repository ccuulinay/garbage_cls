import React, {Component} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
//import Upload from "./upload/Upload"
import SimpleFormUpload from "./upload/SimpleFormUpload"
import CameraUpload from "./upload/CameraUpload"
import H5CameraUpload from "./upload/H5CameraUpload"

class App extends Component {
  render() {
    return (
      <div>
        
        <H5CameraUpload />
      </div>
    )
  }

}

export default App;
