import React from 'react';

export default class LanguageModel extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            startString: '',
            generatedText:''
        };
        this.handleChange = this.handleChange.bind(this)
        this.onSendRequest = this.onSendRequest.bind(this)
    }
    
    handleChange(e){
        this.setState(()=>({startString: e.target.value}))
        console.log(this.state.startString)
    }

    onSendRequest(e){
        e.preventDefault();
        fetch("http://0.0.0.0:80/app/", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
         },
        body: JSON.stringify({"start-string": this.state.startString}),
        })
        .then(response => response.json())
        .then(data => {
            this.setState(()=>({generatedText:data.msg}))
            const dispElement = document.getElementById("disp");
            dispElement.innerHTML = this.state.generatedText

        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    render(){
        return (
            <div className="">
                <form method="GET" onSubmit={this.onSendRequest}>
                    <input type="text" name="start-string" placeholder="supply a start string" value={this.state.startString} onChange={this.handleChange}/>
                    <input type="submit" value="submit"/>
                </form>
                <h3>Generated Text</h3>
                <p id="disp">
    
                </p>
            </div>
        );
    }   
}