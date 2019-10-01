import React from 'react'
import axios from 'axios';

class SimpleFormUpload extends React.Component {

    UPLOAD_ENDPOINT = 'http://127.0.0.1:40086/api/v1/ayi/garbage_image';
    constructor(props) {
        super(props);
        this.state ={
          file:null,
          result:"",
        }
        this.onSubmit = this.onSubmit.bind(this)
        this.onChange = this.onChange.bind(this)
        this.uploadFile = this.uploadFile.bind(this)
    }

    checkMimeType=(event)=>{
        //getting file object
        let files = event.target.files 
        //define message container
        let err = ''
        // list allow mime type
       const types = ['image/png', 'image/jpeg', 'image/gif']
        // loop access array
        for(var x = 0; x<files.length; x++) {
         // compare file type find doesn't matach
             if (types.every(type => files[x].type !== type)) {
             // create error message and assign to container   
             err += files[x].type+' is not a supported format\n';
           }
         };
      
       if (err !== '') { // if message not same old that mean has error 
            event.target.value = null // discard selected file
            console.log(err)
             return false; 
        }
       return true;
      
    }

    checkFileSize=(event)=>{
        let files = event.target.files
        let size = 10485760 
        let err = ""; 
        for(var x = 0; x<files.length; x++) {
            if (files[x].size > size) {
                err += files[x].type+'is too large, please pick a smaller file\n';
            }    
        };
        if (err !== '') {
            event.target.value = null
            console.log(err)
            return false
        }
    
        return true;
    }

    async onSubmit(e){
        e.preventDefault() 
        let res = await this.uploadFile(this.state.file);
        console.log(res.data);
        this.setState({result: res.data.comment})
    }

    onChange(e) {
        let file = e.target.files[0]
        if(this.checkMimeType(e) && this.checkFileSize(e)){
            this.setState({file:file})
        }   
    }
        
    async uploadFile(file){

        const formData = new FormData();
        
        formData.append('image_file',file)
        
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
        <form onSubmit={ this.onSubmit }>
          <h1>Upload Image</h1>
          <input type="file" onChange={ this.onChange } />
          <button type="submit">Upload File</button>
          <div>{this.state.result.length === 0 ? (<div></div>
            ) : (
                <div>{this.state.result}</div>
            )}
          </div>
        </form>
     )
    }
        
}

export default SimpleFormUpload;