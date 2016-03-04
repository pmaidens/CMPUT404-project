/*eslint-env node*/

module.exports = function(config){
    config.set({

        basePath : "./",

        files : [
            "bower_components/angular/angular.js",
            "bower_components/angular-route/angular-route.js",
            "bower_components/angular-mocks/angular-mocks.js",
            "app/components/**/*.js",
            "app/view*/**/*.js",
            "app/controllers/*.js",
            "app/services/*.js",
            "app/directives/*.js"
        ],

        autoWatch : true,

        frameworks: ["jasmine"],

        browsers : ["Firefox"],

        plugins : [
            "karma-chrome-launcher",
            "karma-firefox-launcher",
            "karma-jasmine",
            "karma-junit-reporter"
        ],

        junitReporter : {
            outputFile: "test_out/unit.xml",
            suite: "unit"
        },

        single_run: true

    });
};
