"use strict";

angular.module("myApp.directives.postStream", [])
.directive("postStream", function () {
    return {
        restrict: "E",
        templateUrl: "partials/postStream.html"
    };
});
