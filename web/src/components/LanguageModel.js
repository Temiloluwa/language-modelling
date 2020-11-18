import React from 'react';
import Header from './Header';

export default class LanguageModel extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        const modelParams = {
            title:"Language Model",
            modelName: "Many to One"
        }
        return (
            <div>
                <Header {...modelParams} />
            </div>
        );
    }

}