import React, { Component } from 'react';
import Camera, { FACING_MODES, IMAGE_TYPES } from 'react-html5-camera-photo';
import axios from 'axios';
import 'react-html5-camera-photo/build/css/index.css';
import Dropdown from 'react-dropdown'
import 'react-dropdown/style.css'
import "./H5CameraUpload.css"

import sh_recyclable_logo from '../assets/上海_可回收物_sh.png'; 
import sh_residual_logo from '../assets/上海_干垃圾_sh.png'; 
import sh_hazardous_logo from "../assets/上海_有害垃圾_sh.png";
import sh_househood_food_logo from "../assets/上海_湿垃圾_sh.png";

import gen_recyclable_logo from "../assets/可回收.jpg";
import gen_residual_logo from '../assets/其他.jpg'; 
import gen_hazardous_logo from "../assets/有害.jpg";
import gen_food_logo from "../assets/厨余.jpg";
 
class H5CameraUpload extends Component {
    //UPLOAD_ENDPOINT = 'http://127.0.0.1:40086/api/v1/ayi/camera_capture';
    UPLOAD_ENDPOINT = '/api/v1/ayi/camera_capture';

    constructor(props) {
        super(props);
        this.state ={
          flag_takePhoto: 1,
          flag_previewPhoto: 0,
          flag_showResult: 0,
          screenshot:"",
          result:"",
          tab: 0,
          city: "sh",
          cities: ["sh", "gz"]
        }
        this.onSubmit = this.onSubmit.bind(this)
        this.handleRetake = this.handleRetake.bind(this)
        this.uploadFile = this.uploadFile.bind(this)
        this.handleResult = this.handleResult.bind(this)
        this._onCitySelect = this._onCitySelect.bind(this)
    }

    _onCitySelect(e) {
        //e.preventDefault();
        console.log(e.value);
        this.setState({
            city: e.value
        });
    }

    handleRetake() {
        this.setState({
             screenshot: "", result: "", flag_takePhoto:1,  flag_previewPhoto:0, flag_showResult:0
            });
    }

    handleResult() {
        let cur_city = this.state.city
        let cur_state = this.state.result
        if (cur_city === "sh"){
            if (cur_state === "可回收物") {
                return <img src={sh_recyclable_logo} alt="result"/>
            }else if (cur_state === "干垃圾" || cur_state === "其他垃圾"){
                return <img src={sh_residual_logo} alt="result"/>
            }else if (cur_state === "有害垃圾") {
                return <img src={sh_hazardous_logo} alt="result"/>
            }else if (cur_state === "湿垃圾" || cur_state === "厨余垃圾") {
                return <img src={sh_househood_food_logo} alt="result"/>
            }else if (cur_state === "人像") {
                return <p>你是什么垃圾？！</p>
            }
        }
        else {
            if (cur_state === "可回收物") {
                return <img src={gen_recyclable_logo} alt="result"/>
            }else if (cur_state === "其他垃圾") {
                return <img src={gen_residual_logo} alt="result"/>
            }else if (cur_state === "有害垃圾") {
                return <img src={gen_hazardous_logo} alt="result"/>
            }else if (cur_state === "厨余垃圾") {
                return <img src={gen_food_logo} alt="result"/>
            }else if (cur_state === "人像") {
                return <p>你是什么垃圾？！</p>
            }
        }
        
    }

    async onSubmit(e){
        e.preventDefault() 
        //console.log(this.state.screenshot)
        try {
            let res = await this.uploadFile(this.state.screenshot);
            //console.log(res.data);
            this.setState({
                result: res.data.comment, flag_takePhoto:0,  flag_previewPhoto:0, flag_showResult:1
            })
        } catch(err){
            console.log(err)
        }
        
    }

    async uploadFile(file){
        //let i = file.indexOf('base64,');
        let base64Image = file.split(';base64,').pop();

        const formData = new FormData();
        
        formData.append('image_string', base64Image)
        formData.append('city', this.state.city)
        return  await axios.post(this.UPLOAD_ENDPOINT, formData,{
            headers: {
                'content-type': 'multipart/form-data'
            }
        })
        /*.then(response => {
            console.log(response.data)
            this.setState({result: response.data})
        }).catch((error) => {
            console.log(error)
        });*/
    }

    onTakePhoto (dataUri) {
        // Do stuff with the photo...
        console.log('takePhoto');
        //console.log(dataUri)
        this.setState({ 
            screenshot: dataUri, flag_takePhoto:0,  flag_previewPhoto:1, flag_showResult:0
         });
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
            <div></div>
            <div className="camera-container">
            {this.state.flag_takePhoto ? (
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
            />
                ) : (<div></div>)}
            </div>
            <div className="result-container">
              <div>{this.state.result.length === 0 ? (<div></div>
                    ) : (
                        <div>
                        
                        <div>{this.handleResult()}</div>
                        <div className='controls'>
                            <button onClick={this.handleRetake}>retake</button>
                        </div>
                        </div>
                    )}
              </div>
            </div>
            <div className="preview-container">
            {this.state.flag_previewPhoto ? (
            <div>
              <div className='nav-control'>
                <div className="nav-control-tips">Please select city you are in: </div>
                <Dropdown options={this.state.cities} onChange={this._onCitySelect} value={this.state.cities[0]} placeholder="Select a city" />
              </div>
              <div className='screenshots'>
                {
                this.state.screenshot 
                ? (<div><img src={this.state.screenshot} alt="preview"/></div>) 
                : (<div></div>)
                }
              </div>
              <div className='controls'>
                  <button onClick={this.handleRetake}>retake</button>
                  <button onClick={this.onSubmit}>upload</button>
                  
              </div>
              <div><div>
              
              
              </div> 
              </div></div>)
              : (null)}
            </div>
            <div></div>
        </div>
        
        );
    }
}
 
export default H5CameraUpload;