import React from "react";
import Webcam from "react-webcam";
import axios from 'axios';

class CameraUpload extends React.Component {
    UPLOAD_ENDPOINT = '/api/v1/ayi/camera_capture';
    constructor(props) {
        super(props);
        this.state ={
          screenshot:null,
          result:"",
          tab: 0,
        }
        this.onSubmit = this.onSubmit.bind(this)
        //this.onChange = this.onChange.bind(this)
        this.uploadFile = this.uploadFile.bind(this)
    }

    handleCapture = () => {
        const screenshot = this.webcam.getScreenshot();
        this.setState({ screenshot });
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
        //console.log(file.slice(i + 7))
        //console.log(base64Image)
        //let some_image = window.atob(base64Image)
        //let buffer = Buffer.from(file.slice(i + 7), 'base64');
        //let buffer = Buffer.from(some_image)
        //let image_file = new File(buffer, "garbage.jpeg",{type: "image/jpeg"});
        //console.log(image_file)
        //let image_file = new File(file, "garbage.jpg", {type: "image/jpeg"})
        //let image_file = base64Img.img(file, '', 'garbage.jpg');

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

    render() {
        return (
          <div>
            <h1>Take a photo of garbage</h1>
            <Webcam
              audio={false}
              screenshotFormat="image/jpeg"
              ref={node => this.webcam = node}
            />
            
            <div>
              
              <div className='screenshots'>
                <div className='controls'>
                  <button onClick={this.handleCapture}>capture</button>
                </div>
        {this.state.screenshot ? (<div><img src={this.state.screenshot} /></div>) : (<div></div>)}
              </div>
              <div>{this.state.screenshot ? (<div>
              <h2>Are you ready to upload</h2>
              <form onSubmit={ this.onSubmit }>
                <button type="submit">Upload File</button>
                <div>{this.state.result.length === 0 ? (<div></div>
                    ) : (
                        <div>{this.state.result}</div>
                    )}
                </div>
                
              </form></div>) : (null)
              }</div>
              
            </div>
          </div>
        );
      }
}

export default CameraUpload;