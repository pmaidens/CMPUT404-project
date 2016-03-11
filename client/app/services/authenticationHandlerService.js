"use strict";

angular.module("myApp.services.authenticationHandler", ["myApp.services.urlHandler"])
.service("authenticationHandler", function($q,$http, urlHandler) {
    this.loginWatchers = [];
    this.user = {};

    this.login = function (username, password) {
        // Make a request to see if the login credentials are valid
        // If they are, set them as default headers
        //  return $q(function(resolve/*, reject*/) {
        //    setTimeout(function () {
        // $httpProvider.defaults.headers.common.Authorization = "Basic " + result.token;
        //         this.loginWatchers.forEach(function(f) {
        //             f(true);
        //         });
        //         resolve();
        //     }.bind(this), 1000);
        // }.bind(this));

        var url = urlHandler.serviceURL() + "rest-auth/login/";
        return $http.post(url,{"username":username, "password":password}).then(function(result){
            // console.log(result.data.key);
            this.determineUser(username).then(function () {
                this.updateWatchers(true);
            });
            // $http.get(urlHandler.serviceURL()+"api/author/").then(function (result) {
            //     result.data.some(function (author) {
            //         if(author.displayname === username) {
            //             this.user = author;
            //             this.loginWatchers.forEach(function(f){
            //                 f(true);
            //             });
            //             return true;
            //         }
            //     }.bind(this));
            // }.bind(this));

            $httpProvider.defaults.headers.common.Authorization = "Token " + result.data.key;

        },function(err){


            console.log(err);

        });

    };

    this.logout = function() {
        //Keep this wrapped in 'q' just to keep everything consistent.
        return $q(function(resolve/*, reject*/) {
            $httpProvider.defaults.headers.common.Authorization = undefined;
            this.updateWatchers(false);
            resolve();
        }.bind(this));
    };

    this.register = function (userInfo) {
        $http.post(urlHandler.serviceURL()+"rest-auth/registration", userInfo).then(function () {
            this.determineUser(userInfo.displayname).then(function () {
                this.updateWatchers(true);
            });
        }.bind(this));
    };

    this.determineUser = function (displayname) {
        return $http.get(urlHandler.serviceURL()+"api/author/").then(function (result) {
            result.data.some(function (author) {
                if(author.displayname === displayname) {
                    this.user = author;
                    return true;
                }
            }.bind(this));
        }.bind(this));
    };

    this.updateWatchers = function (loggedIn) {
        this.loginWatchers.forEach(function(f){
            f(loggedIn);
        });
    };

    this.watchLogin = function(callback) {
        this.loginWatchers.push(callback);
    };
});
