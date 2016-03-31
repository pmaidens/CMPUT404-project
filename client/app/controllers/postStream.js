"use strict";

angular.module("myApp.postStream", [
    "ngRoute",
    "myApp.services.postHandler",
    "myApp.services.authenticationHandler",
    "myApp.services.urlHandler"
])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/stream", {
        templateUrl: "partials/postStream.html",
        controller: "PostStreamController"
    });
}])

.controller("PostStreamController", function($scope, $http, $location ,postHandler, authenticationHandler, urlHandler) {
    $scope.user = authenticationHandler.user;
    $scope.posts = [];
    $scope.allPost = [];

    postHandler.getPosts().then(function (results) {
        var targetAuthorId = $scope.postStream && $scope.postStream.authorId ? $scope.postStream.authorId : targetAuthorId = authenticationHandler.user.id;
        // If we are on the profile page, only show the user's posts
        if(~$location.url().indexOf("/profile")){
            results.data = results.data.filter(function(post){
                return post.author.id === targetAuthorId;
            });
        }

        results.data.forEach(function (post) {
            $scope.allPost.push(post);
        });

        loadGit();
    });

    // Make a http call to the github api to get all user information
    // associated with the git_username

    var loadGit = function () {
        //change $scope.git_username to the author"s github user name

        var gitHubURL = $scope.user.github;


        if(gitHubURL){
            $scope.git_username = gitHubURL.substring(gitHubURL.lastIndexOf("/")+1);
            $http({method: "GET", url:"https://api.github.com/users/"+$scope.git_username , headers:{"Authorization":undefined}}).success(function(gitdata){


                $scope.gitUserData = gitdata;
                loadEvents();


            });
        } else {

            $scope.posts.forEach(function(post){

                $scope.allPost.push(post);


            });

        }

    };
    // Http call for github repos (not too sure what Abram means by "activity")
    // ** May need to make additional calls

    var loadEvents = function () {
        $http({method:"GET", url: "https://api.github.com/users/"+$scope.git_username+"/events" , headers:{"Authorization":undefined}})
        .success(function(event_data){
            $scope.eventData = event_data;

            //$scope.allPost = $scope.posts.concat($scope.eventData);
            $scope.eventData.forEach(function(eventData){

                $scope.allPost.push(eventData);

            });

        });
    };

    $scope.deletePost = function(post) {
        post.disabled = true;
        postHandler.deletePost(post.id).then(function(result) { //eslint-disable-line no-unused-vars
            //postHandlerService should reload the page


        });
    };

    $scope.editPost = function (post) {
        post.editMode = true;
    };

    $scope.submitPost = function (post) {
        postHandler.updatePost(post);
        post.editMode = false;

    };


    //localhost/api/posts/{postid}/comments

    //POST : author id, comment, postid
    $scope.AddComment = function (post, comments) {
        var nodeURL;
        var postURL = post.author.host;

        if(postURL !== urlHandler.serviceURL() && !~postURL.indexOf("/api/")) {
            nodeURL = postURL + "api/";
        }

        postHandler.commentPost({
            author: authenticationHandler.user,
            comment: comments,
            contentType: "text/plain"
        },post.id, nodeURL).then(function () {
            postHandler.getPost(nodeURL, post.id).then(function (result) {
                post.comments = result.data.comments;
            });
        });
        //	var urlToComment = post.author.host + "api/posts/" + post.id + "/comments/";
        // var appendCheck = post.author.host.split("/");
        // var toAppend = "";
        // if(appendCheck[appendCheck.length-1]!="api"){
        //
        //     toAppend = "api";
        // }
        // console.log(post.id);
        // var urlToComment = post.author.host + toAppend + "/posts/" + post.id + "/comments/";
        // console.log(urlToComment);
        // var commentAuthor = authenticationHandler.user;
        // var DisplayName = commentAuthor.displayname;
        // commentAuthor["displayName"] = DisplayName;
        // postHandler.commentPost({
        //     author: commentAuthor,
        //     comment: comments,
        //     //we need to allow different contenttypes for comments
        //     contentType: "text/plain"//,
        //     // published: date,
        //     //id
        // },urlToComment).then(function(){
        //
        //     comments = "";
        //
        //     //TODO
        //
        //     $http.get(urlHandler.serviceURL()+"api/posts/"+post.id+"/").then(function(postData){
        //
        //
        //         post.comments = postData.data.comments;
        //
        //     });
        //
        // });
    };
});
