import * as React from "react";
import { render } from "react-dom";
import { Router, Route, browserHistory } from "react-router";
import { createStore } from "redux";
import AppReducer from "./js/reducers/AppReducer";
import App from "./js/app";
import Writer from "./js/writer";

const store = createStore( AppReducer ); //eslint-disable-line no-unused-vars

render((
    <Router history={browserHistory}>
        <Route path="/" component={App}>
            <Route path="/write" component={Writer} />
        </Route>
    </Router>
), document.getElementById("mount-point"));

store.subscribe(render);
