"use strict";

angular.module("myApp.services.urlHandler", [])
.service("urlHandler", function() {
    this.serviceURL = function () {//eslint-disable-line no-unused-vars
        return "http://localhost:8080/";
    };
});
