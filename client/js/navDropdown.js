import * as React from "react";

class NavDropdown extends React.Component {
    constructor(props) {
        super(props);
        this.state = {showDropdown: false};
        this.onClick = this.onClick.bind(this);
    }

    onClick () {
        this.setState({
            ...this.state,
            showDropdown: !this.state.showDropdown
        });
    }

    render() {
        return (
            <li onClick={this.onClick}>
                { this.state.showDropdown ? this.props.children : this.getNonDropdownChildren()}
            </li>
        );
    }

    getNonDropdownChildren() {
        return this.props.children.filter(function(element) {
            return element.props.className !== "dropdown-menu";
        });
    }
}

export default NavDropdown;
