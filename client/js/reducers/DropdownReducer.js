// I am not using this anymore, but I am going to leave it here as an example

const DropdownReducer = (state = [], action) => {
    switch (action.type) {
        case "TOGGLE_DROPDOWN":
            return state.map(d => dropdown(d, action));
        case "ADD_DROPDOWN":
            return [
                ...state,
                dropdown(undefined, action)
            ];
        default:
            return state;
    }
};

const dropdown = (state, action) => {
    switch(action.type) {
        case "ADD_DROPDOWN":
            return {
                id: action.id,
                visible: false
            };
        case "TOGGLE_DROPDOWN":
            if (state.id === action.id) {
                return state;
            }
            return {
                ...state,
                visible: !state.visible
            };
        default:
            return state;
    }
};

export default DropdownReducer;
