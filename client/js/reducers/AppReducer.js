import { combineReducers } from "redux";
import DropdownReducer from "./DropdownReducer";

const AppReducer = combineReducers({
    dropdowns: DropdownReducer
});

export default AppReducer;
