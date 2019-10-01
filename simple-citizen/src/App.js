import React, {Component} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
//import Upload from "./upload/Upload"
import SimpleFormUpload from "./upload/SimpleFormUpload"

class App extends Component {
  render() {
    return (
      <div>
        <SimpleFormUpload />
      </div>
    )
  }

}

export default App;
