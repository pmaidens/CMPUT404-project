"use strict";

angular.module("myApp.navbar", ["myApp.services.authenticationHandler"])


.controller("NavbarController", function($scope, $location, authenticationHandler) {
    $scope.valid = false;

    $scope.logout = function() {
        authenticationHandler.logout();
        $location.url("/login");
    };
    authenticationHandler.watchLogin(function(loggedin) {
        $scope.valid = loggedin;
    }.bind(this));

    $scope.login = function() {
        authenticationHandler.login($scope.username, $scope.password).then(function() {
            console.log("sup?");
            $location.url("/stream");
        },function(err){
            console.log(err);
        });
    };
});