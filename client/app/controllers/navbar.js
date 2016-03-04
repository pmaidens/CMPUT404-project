"use strict";

angular.module("myApp.navbar", ["myApp.services.authenticationHandler"])

.controller("NavbarController", function($scope, authenticationHandler) {
    $scope.valid = false;
    $scope.login = function() {
        authenticationHandler.login("asdf", "asdf");
    };
    $scope.logout = function() {
        authenticationHandler.logout();
    };
    authenticationHandler.watchLogin(function(loggedin) {
        $scope.valid = loggedin;
    }.bind(this));
});