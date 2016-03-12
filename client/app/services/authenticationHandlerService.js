"use strict";

angular.module("myApp.services.authenticationHandler", ["myApp.services.urlHandler"])
.service("authenticationHandler", function($q,$http, urlHandler) {
    this.loginWatchers = [];
    this.user = {};
    this.token = "";

    this.login = function (username, password) {
        var url = urlHandler.serviceURL() + "rest-auth/login/";
        return $http.post(url,{"username":username, "password":password}).then(function(result){
            this.determineUser(username).then(function () {
                this.updateWatchers(true);
            }.bind(this));
            $http.defaults.headers.common.Authorization = "Token " + result.data.key;
            this.token = "Token " + result.data.key;

        }.bind(this),function(err){
            console.log(err);
        });
    };

    this.logout = function() {
        //Keep this wrapped in 'q' just to keep everything consistent.
        return $q(function(resolve/*, reject*/) {
            $http.defaults.headers.common.Authorization = undefined;
            this.token = "";
            this.updateWatchers(false);
            resolve();
        }.bind(this));
    };

    this.register = function (userInfo) {
        $http.post(urlHandler.serviceURL()+"rest-auth/registration", userInfo).then(function () {
            this.determineUser(userInfo.displayname).then(function () {
                this.updateWatchers(true);
            }.bind(this));
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
