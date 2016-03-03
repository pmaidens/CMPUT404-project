/*eslint-env node*/

module.exports = {
    "rules": {
        "indent": [
            2,
            4,
            {"SwitchCase": 1}
        ],
        "quotes": [
            2,
            "double"
        ],
        "linebreak-style": [
            2,
            "unix"
        ],
        "semi": [
            2,
            "always"
        ],
        "no-console": [
            0
        ]
    },
    "env": {
        "es6": true,
        "browser": true
    },
    "extends": "eslint:recommended",
    "ecmaFeatures": {
        "jsx": true,
        "experimentalObjectRestSpread": true,
        "modules": true
    },
    "globals": {
        "angular": true,
        "inject": true,
        "browser": true,
        "element": true,
        "by": true
    }
};
