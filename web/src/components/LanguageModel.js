import React from 'react';
import Header from './Header';
import Body from './Body';

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
                <Body />
            </div>
        );
    }

}