import React from 'react';

export default (props) => {
    return (
        <div className="header">
            <div className="container">
                <h1 className="header__title">{props.title}</h1>
                <nav>
                    {props.modelName&&<h2 className="header__modelName">{props.modelName}</h2>}
                </nav>
            </div>
        </div>
    );
}

