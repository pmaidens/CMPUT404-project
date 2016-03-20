"use strict";

angular.module("myApp.services.authorHandler", [
    "myApp.services.urlHandler",
    "myApp.services.authenticationHandler"
])
.service("authorHandler", function($q, $http, urlHandler, authenticationHandler) {
    this.getAllAuthors = function(){
        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.get(urlHandler.serviceURL() + "api/author/");
    }
    this.getAuthor = function (authorId) {
        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.get(urlHandler.serviceURL() + "api/author/" + (authorId || authenticationHandler.user.id) + "/");
    };


    this.submitAuthor = function (author) {
        var putParameters = {
            github: author.github,
            first_name: author.first_name,
            last_name: author.last_name,
            email: author.email,
            bio: author.bio
        };

        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.put(urlHandler.serviceURL() + "api/author/" + author.id + "/", putParameters).then(function() {
            authenticationHandler.updateUser(author);
        });
    };

    var STUBgetAuthorId = {
        "id":"de305d54-75b4-431b-adb2-eb6b9e546013",
        "host":"http://127.0.0.1:5454/",
        "displayName":"laracroft",
        "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "friends": [],
        "github": "http://github.com/laracroft",
        "first_name": "Lara",
        "last_name": "Croft",
        "email": "lara@croft.com",
        "bio": "An amazing person!"
    };

    this.postFriendRequest = function(friend){
    	/*
        	we're going to post to our service and tell it to follow the user
            then our backend makes the real request to the friend we want 
    	*/
        var requestObject = {
            query: "friendrequest",
            author:  {
                "id": authenticationHandler.user.id,
                "host": authenticationHandler.user.host,
                "displayName": authenticationHandler.user.displayname,
            },
            friend: friend
        };

        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.post(urlHandler.serviceURL() + "api/friendrequest/", requestObject);
    };


    this.getFollowers = function(authorId){
	
	//get followers
	return $http.get(urlHandler.serviceURL() + "api/author/" + (authorId|| authenticationHandler.user.id) + "/friendrequests/");

    };
    this.getFollowing = function(authorId){
	
	//get ppl who the author is following
	return $http.get(urlHandler.serviceURL() + "api/author/" + (authorId || authenticationHandler.user.id) + "/following/");


    };

    this.unfriend = function(friend){

	//delete friend
	//return $http.post();

    };

    this.unfollow = function(following){
	//stop following

    };

    this.acceptFriend = function(follower){
    
	//accept friend request
    };

});
