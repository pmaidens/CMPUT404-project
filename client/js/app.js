"use strict";

import * as React from "react";
import * as ReactDOM from "react-dom";
import * as Bootstrap from "react-bootstrap";

class App extends React.Component {
    render() {
        return (
            <div>
                Hello World!
            </div>
        );
    }
}

const render = () => {
    ReactDOM.render(
        <App/>,
        document.getElementById("mount-point")
    );
};

render();
