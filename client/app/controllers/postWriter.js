"use strict";

angular.module("myApp.postWriter", [
    "ngRoute",
    "myApp.services.postHandler",
    "myApp.services.authenticationHandler",
    "ngFileUpload"
])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/write", {
        templateUrl: "partials/postWriter.html",
        controller: "PostWriterController"
    });
}])

.controller("PostWriterController", ["$scope", "$q", "$location", "$http", "postHandler", "authenticationHandler", "urlHandler", "Upload",

function($scope, $q, $location, $http, postHandler, authenticationHandler, urlHandler, Upload) {

    function separateCategories(inputValue) {
        return inputValue.split(",").map(function(category) {
            return category.trim();
        }).filter(function(category) {
            return !!category;
        });
    }

    var uploadImage = function() {
        var deferred = $q.defer();
        if ($scope.file && !$scope.file.$error) {
            $scope.file.upload = Upload.upload({
                url: "https://api.cloudinary.com/v1_1/" + "dnczne3if" + "/upload",
                headers: {
                    "Authorization": undefined
                },
                data: {
                    upload_preset: "kqfm51gi",
                    file: $scope.file
                }
            }).success(function(data) {
                deferred.resolve(data);
            }).error(function(data) {
                deferred.reject(data);
                console.log("Image upload failed");
            });
        } else if (!$scope.file){
            deferred.resolve({});
        }

        return deferred.promise;
    };

    $scope.SubmitPost = function() {
        // TODO: Change this object to whatever it needs to be
        uploadImage().then(function(data) {
            postHandler.createPost({
                author: authenticationHandler.user.id,
                source: "someSource",
                origin: "anOrigin",
                title: $scope.title || "",
                description: $scope.description || "",
                contentType: $scope.contentType,
                categories: separateCategories($scope.categories || ""),
                visibility: $scope.visibility,
                content: $scope.content || "",
                image: data.url || ""
            }).then(function () {
                console.log("success");
            }, function (err) {
                console.log(err);
            });

            $location.url("/#/stream");
        }, function(err) {
            console.log("Error in promise" + err);
        });


        // $http({
        //     method: "POST",
        //     url: "base/server/url/authors/123/posts",
        //     data: {
        //         author: 123,
        //         title: $scope.title || "",
        //         description: $scope.description || "",
        //         contentType: $scope.contentType,
        //         categories: separateCategories($scope.categories || ""),
        //         visibility: $scope.visibility,
        //         content: $scope.content || ""
        //     }
        // });
    };

    $scope.visibility = $scope.visibility || "PUBLIC";
    $scope.contentType = $scope.contentType || "text/plain";
}
]);
