"use strict";

import * as React from "react";
import "react-bootstrap";
import HeaderBar from "./headerBar";

class App extends React.Component {
    render() {
        return (
            <div>
                <HeaderBar />
                {this.props.children}
            </div>
        );
    }
}

export default App;
