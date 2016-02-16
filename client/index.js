import * as React from "react";
import { render } from "react-dom";
import App from "./js/app";
import { Router, Route, browserHistory } from "react-router";
import { createStore } from "redux";
import AppReducer from "./js/reducers/AppReducer";

const store = createStore( AppReducer ); //eslint-disable-line no-unused-vars

render((
    <Router history={browserHistory}>
        <Route path="/" component = {App} />
    </Router>
), document.getElementById("mount-point"));

store.subscribe(render);
