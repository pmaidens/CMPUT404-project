"use strict";

angular.module("myApp.commentController", ["myApp.services.postHandler"])

.controller("CommentController", function($scope, postHandler){


 $scope.AddComment = function () {
 		 postHandler.commentPost({
 		 	author: "7a0465c9-b89e-4f3b-a6e7-4e35de32bd64",
			source:"someSource",
			origin:"anOrigin",
            title: $scope.title || "",
            description: $scope.description || "",
            contentType: $scope.contentType,
            categories: separateCategories($scope.categories || ""),
            visibility: $scope.visibility,
            content: $scope.content || ""
            if($scope.txtcomment !=''){
                    comment: $scope.comment.push($scope.txtcomment);
                    $scope.txtcomment = "";
                    }
                }
 		 });

 };
})

