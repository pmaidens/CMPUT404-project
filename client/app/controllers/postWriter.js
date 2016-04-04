"use strict";

angular.module("myApp.postWriter", [
  "ngRoute",
  "myApp.services.postHandler",
  "myApp.services.authenticationHandler",
  "ngFileUpload",
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
        }).success(function(data, status, headers, config) {
          deferred.resolve(data);
        }).error(function(data, status, headers, config) {
          deferred.reject(data);
          console.log("Image upload failed");
        });
      }

      return deferred.promise;
    }

    $scope.SubmitPost = function() {
      // TODO: Change this object to whatever it needs to be
	console.log('am i hwere atleast????????');
      uploadImage().then(function(data) {
	  
	  console.log('DATA from uploadImage printing below!');
	  console.log(data.url);
          
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
              image: data.url
        });

        $location.url("/#/stream");
      }, function(err) {
        console.log("Error in promise");
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
