import * as React from "react";
import { Link } from "react-router";
import NavDropdown from "./navDropdown";

class HeaderBar extends React.Component {
    render() {
        return (
            <nav className="navbar navbar-default">
              <div className="container-fluid">
                <div className="navbar-header">
                  <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                    <span className="sr-only">Toggle navigation</span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                  </button>
                  <Link className="navbar-brand" to="/">Blog</Link>
                </div>

                <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                  <ul className="nav navbar-nav">
                    <li className="active"><Link to="/">Link <span className="sr-only">(current)</span></Link></li>
                    <li><Link to="/">Link</Link></li>
                    <NavDropdown className="dropdown">
                      <Link to="/" className="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span className="caret"></span></Link>
                      <ul className="dropdown-menu" style={{display: "block"}}>
                        <li><Link to="/">Action</Link></li>
                        <li><Link to="/">Another action</Link></li>
                        <li><Link to="/">Something else here</Link></li>
                        <li role="separator" className="divider"></li>
                        <li><Link to="/">Separated link</Link></li>
                        <li role="separator" className="divider"></li>
                        <li><Link to="/">One more separated link</Link></li>
                      </ul>
                    </NavDropdown>
                  </ul>
                </div>
              </div>
            </nav>
        );
    }
}

export default HeaderBar;
