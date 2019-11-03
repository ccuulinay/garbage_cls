import React, {Component} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
//import Upload from "./upload/Upload"
//import SimpleFormUpload from "./upload/SimpleFormUpload"
//import CameraUpload from "./upload/CameraUpload"
import H5CameraUpload from "./upload/H5CameraUpload"
import Example from "./dev/ResponsiveView"

class App extends Component {
  render() {
    return (
      <div>
        
        <H5CameraUpload />
        {/*<Example>
        </Example>*/}
      </div>
    )
  }

}

export default App;
