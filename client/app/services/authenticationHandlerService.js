"use strict";

angular.module("myApp.services.authenticationHandler", [
    "myApp.services.urlHandler",
    "ngStorage"
])
.service("authenticationHandler", function($q, $http, $localStorage, $rootScope, urlHandler) {
    this.loginWatchers = [];
    this.user = $localStorage.user || {};
    this.token = $localStorage.token || "";
    this.realToken ='';

    $rootScope.loggedIn = !!$localStorage.token;

    this.login = function (username, password) {
        var url = urlHandler.serviceURL() + "rest-auth/login/";
        return $q(function(resolve, reject) {
            $http.post(url,{"username":username, "password":password}).then(function(result){
		this.realToken = result.data.key;
                this.determineUser(username).then(function () {
                    this.updateWatchers(true);
                    resolve(result);
                }.bind(this));

                var token = "Token " + this.realToken;
                $http.defaults.headers.common.Authorization = token;
                this.token = token;
                $localStorage.token = this.token;
            }.bind(this),function(err){
                console.log(err);
                reject(err);
            });
        }.bind(this));
    };

    this.logout = function() {
        //Keep this wrapped in 'q' just to keep everything consistent.
        return $q(function(resolve) {
            $http.defaults.headers.common.Authorization = undefined;
            this.token = "";
            delete $localStorage.token;
            delete $localStorage.user;
            this.user = {};
            $rootScope.loggedIn = false;
            this.updateWatchers(false);
            resolve();
        }.bind(this));
    };

    this.register = function (userInfo) {
        $http.post(urlHandler.serviceURL()+"rest-auth/registration/", userInfo).then(function () {
            this.determineUser(userInfo.displayname).then(function () {
                this.updateWatchers(true);
            }.bind(this));
        }.bind(this));
    };

    this.determineUser = function (displayname) {
        return $http.get(urlHandler.serviceURL()+"api/author/").then(function (result) {
            result.data.some(function (author) {
                if(author.displayName === displayname) {
                    this.user = $localStorage.user = author;
                    $rootScope.loggedIn = true;
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

    this.updateUser = function(user) {
        this.user = $localStorage.user = user;
    };

    this.generateToken = function (username, password) {
        return "Basic " + window.btoa(username+":"+password);
    };
});
