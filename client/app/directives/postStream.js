"use strict";

angular.module("myApp.directives.postStream", ["myApp.services.postHandler"])
.directive("postStream", function () {
    return {
        restrict: "E",
        templateUrl: "partials/postStream.html"
    };
});
