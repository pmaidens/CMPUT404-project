"use strict";

angular.module("myApp.services.urlHandler", [])
.service("urlHandler", function() {
    this.serviceURL = function () {//eslint-disable-line no-unused-vars
        return "http://project-c404.rhcloud.com/";
    };
    this.remoteURL = function(friendurl){

        console.log("friendurl "+friendurl);
        return friendurl;
    };
    this.apiURL = function () {
        return "http://project-c404.rhcloud.com/api/";
    };
});
