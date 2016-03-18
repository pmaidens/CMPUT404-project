"use strict";

angular.module("myApp.commentController", [
    "myApp.services.postHandler",
    "myApp.services.authenticationHandler"
])

.controller("CommentController", function($scope, postHandler, authenticationHandler){


 $scope.AddComment = function () {
 		postHandler.commentPost({
            author: authenticationHandler.user.id,
            source:"someSource",
            origin:"anOrigin",
            title: $scope.title || "",
            description: $scope.description || "",
            contentType: $scope.contentType,
            categories: separateCategories($scope.categories || ""),
            visibility: $scope.visibility,
            content: $scope.content || "",
            comment: $scope.txtcomment !== "" ? $scope.comment.push($scope.txtcomment) : $scope.comment,
 		});
        $scope.txtcomment = "";
    };
})
