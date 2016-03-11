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
            console.log(result.data.key);

            this.loginWatchers.forEach(function(f){

                f(true);
            });

            $httpProvider.defaults.headers.common.Authorization = "Token " + result.data.key;

        },function(err){


            console.log(err);

        });

    };

    this.logout = function() {
        //Keep this wrapped in 'q' just to keep everything consistent.
        return $q(function(resolve/*, reject*/) {
            $httpProvider.defaults.headers.common.Authorization = undefined;
            this.loginWatchers.forEach(function(f) {
                f(false);
            });
            resolve();
        }.bind(this));
    };

    this.watchLogin = function(callback) {
        this.loginWatchers.push(callback);
    };
});
