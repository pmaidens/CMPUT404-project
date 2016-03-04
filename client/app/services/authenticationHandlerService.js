"use strict";

angular.module("myApp.services.authenticationHandler", [])
.service("authenticationHandler", function($q) {
    this.login = function (username, password) {
        // Make a request to see if the login credentials are valid
        // If they are, set them as default headers
        return $q(function(resolve/*, reject*/) {
            setTimeout(function () {
                // $httpProvider.defaults.headers.common.Authorization = "Basic " + result.token;
                resolve();
            }.bind(this), 1000);
        }.bind(this));
    };

    this.logout = function() {
        //Keep this wrapped in 'q' just to keep everything consistent.
        return $q(function(resolve/*, reject*/) {
            // $httpProvider.defaults.headers.common.Authorization = undefined;
            resolve();
        });
    };
});