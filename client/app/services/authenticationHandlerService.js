"use strict";

angular.module("myApp.services.authenticationHandler", [])
.service("authenticationHandler", function($q,$http) {
    this.loginWatchers = [];

    this.login = function (username, password) {
        // Make a request to see if the login credentials are valid
        // If they are, set them as default headers
    //     return $q(function(resolve/*, reject*/) {
    //         setTimeout(function () {
    //             // $httpProvider.defaults.headers.common.Authorization = "Basic " + result.token;
    //             this.loginWatchers.forEach(function(f) {
    //                 f(true);
    //             });
    //             resolve();
    //         }.bind(this), 1000);
    //     }.bind(this));
     
	var url = 'localhost:8000/rest-auth/login/'
	return $http.post(url).then(function(result){

	    //$scope.authToken = result.data.key;
	    $httpProvider.defaults.headers.common.Authorization = "Basic " + result.data.key;

	},function(err){


	    console.log(err);
	});
    
    
    };

    this.logout = function() {
        //Keep this wrapped in 'q' just to keep everything consistent.
        return $q(function(resolve/*, reject*/) {
            // $httpProvider.defaults.headers.common.Authorization = undefined;
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
