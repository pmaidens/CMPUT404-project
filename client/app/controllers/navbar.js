"use strict";

angular.module("myApp.navbar", ["myApp.services.authenticationHandler"])

.controller("NavbarController", function($scope, authenticationHandler) {
    $scope.valid = false;
    $scope.logout = function() {
        authenticationHandler.logout();
    };
    authenticationHandler.watchLogin(function(loggedin) {
        $scope.valid = loggedin;
    }.bind(this));
});