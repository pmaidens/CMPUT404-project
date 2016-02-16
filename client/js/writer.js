import * as React from "react";
import "react-bootstrap";
import HeaderBar from "./headerBar";

class Writer extends React.Component {
    onClick() {
        alert("Clicked!");
    }

    render() {
        return (
            <div>
                <textarea name="writeArea" autoComplete="on" autofocus="true" placeholder="Your blog post here" spellCheck="true"></textarea>
                <button onClick={this.onClick}>Submit</button>
            </div>
        );
    }
}

export default Writer;
