import React, { Component } from 'react';
import Camera, { FACING_MODES, IMAGE_TYPES } from 'react-html5-camera-photo';
import axios from 'axios';
import 'react-html5-camera-photo/build/css/index.css';
 
class H5CameraUpload extends Component {
    //UPLOAD_ENDPOINT = 'http://127.0.0.1:40086/api/v1/ayi/camera_capture';
    UPLOAD_ENDPOINT = '/api/v1/ayi/camera_capture';
    constructor(props) {
        super(props);
        this.state ={
          screenshot:"",
          result:"",
          tab: 0,
        }
        this.onSubmit = this.onSubmit.bind(this)
        this.handleRetake = this.handleRetake.bind(this)
        this.uploadFile = this.uploadFile.bind(this)
    }

    handleRetake() {
        this.setState({ screenshot: "", result: "" });
    }

    async onSubmit(e){
        e.preventDefault() 
        //console.log(this.state.screenshot)
        let res = await this.uploadFile(this.state.screenshot);
        //console.log(res.data);
        this.setState({result: res.data.comment})
    }

    async uploadFile(file){
        //let i = file.indexOf('base64,');
        let base64Image = file.split(';base64,').pop();

        const formData = new FormData();
        
        formData.append('image_string', base64Image)
        
        return  await axios.post(this.UPLOAD_ENDPOINT, formData,{
            headers: {
                'content-type': 'multipart/form-data'
            }
        })
        /*.then(response => {
            console.log(response.data)
            this.setState({result: response.data})
        })*/.catch((error) => {
            console.log(error)
        });
    }

    onTakePhoto (dataUri) {
        // Do stuff with the photo...
        console.log('takePhoto');
        //console.log(dataUri)
        this.setState({ screenshot: dataUri });
    }
 
    onCameraError (error) {
        console.error('onCameraError', error);
    }
 
    onCameraStart (stream) {
        console.log('onCameraStart');
    }
 
    onCameraStop () {
        console.log('onCameraStop');
    }
 
    render () {
        return (
        <div className="App">
            <div>
            {this.state.screenshot ? (<div></div>) : (
                <Camera
                onTakePhoto = { (dataUri) => { this.onTakePhoto(dataUri); } }
                onCameraError = { (error) => { this.onCameraError(error); } }
                idealFacingMode = {FACING_MODES.ENVIRONMENT}
                //idealResolution = {{width: 640, height: 480}}
                imageType = {IMAGE_TYPES.JPG}
                imageCompression = {0.97}
                isMaxResolution = {false}
                isImageMirror = {false}
                //isSilentMode = {true}
                //isDisplayStartCameraError = {true}
                //isFullscreen = {true}
                //sizeFactor = {1}
                onCameraStart = { (stream) => { this.onCameraStart(stream); } }
                onCameraStop = { () => { this.onCameraStop(); } }
                />)}
            </div>
            <div>
            {this.state.screenshot ? (
            <div>
              <div className='screenshots'>
                <div className='controls'>
                  <button onClick={this.handleRetake}>retake</button>
                </div>
        {this.state.screenshot ? (<div><img src={this.state.screenshot} /></div>) : (<div></div>)}
              </div>
              <div><div>
              <h2>Are you ready to upload</h2>
              <form onSubmit={ this.onSubmit }>
                <button type="submit">Upload File</button>
                <div>{this.state.result.length === 0 ? (<div></div>
                    ) : (
                        <div>{this.state.result}</div>
                    )}
                </div>
                
              </form></div> 
              </div></div>)
              : (null)}
            </div>
        </div>
        
        );
    }
}
 
export default H5CameraUpload;