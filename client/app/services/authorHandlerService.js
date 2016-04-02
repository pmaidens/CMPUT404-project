"use strict";

angular.module("myApp.services.authorHandler", [
    "myApp.services.urlHandler",
    "myApp.services.authenticationHandler",
    "myApp.services.nodeHandler"
])
.service("authorHandler", function($q, $http, urlHandler, authenticationHandler, nodeHandler) {
    this.getAllAuthors = function(){
        return $q(function (resolve) {
            nodeHandler.sendToAll("get", "author/", undefined, {
                url: "https://mighty-cliffs-82717.herokuapp.com/api/",
                relativeURL: "authors/"
            }).then(function (results) {
                var returnValue = {
                    data:[]
                };
                results.forEach(function (result) {
                    if(result.data instanceof Array) {
                        returnValue.data = returnValue.data.concat(result.data);
                    } else {
                        returnValue.data = returnValue.data.concat(result.data.authors);
                    }
                });
                resolve(returnValue);
            });
        });
    };
    this.getAuthor = function (authorId) {
        return nodeHandler.sendTo(urlHandler.serviceURL(), "get", "author/" + (authorId || authenticationHandler.user.id) + "/");
    };


    this.submitAuthor = function (author) {
        var putParameters = {
            github: author.github,
            first_name: author.first_name,
            last_name: author.last_name,
            email: author.email,
            bio: author.bio
        };

        return nodeHandler.sendTo(urlHandler.serviceURL(), "put", "author/" + author.id + "/", putParameters).then(function() {
            authenticationHandler.updateUser(author);
        });
    };

    this.postFriendRequest = function(friend){
        /*
        we"re going to post to our service and tell it to follow the user
        then our backend makes the real request to the friend we want
        */
        var requestObject = {
            query: "friendrequest",
            author:  {
                "id": authenticationHandler.user.id,
                "host": authenticationHandler.user.host,
                "displayName": authenticationHandler.user.displayName,
                "url": authenticationHandler.user.url
            },
            friend: friend
        };

        return nodeHandler.sendTo(friend.host, "post", "friendrequest/", requestObject);
    };

    this.getFollowers = function(authorId){
        //get followers
        return nodeHandler.sendTo(urlHandler.serviceURL(), "get", "author/" + (authorId || authenticationHandler.user.id) + "/friendrequests/");
    };
    this.getFollowing = function(authorId){
        //get ppl who the author is following
        return nodeHandler.sendTo(urlHandler.serviceURL(), "get", "author/" + (authorId || authenticationHandler.user.id) + "/following/");
    };

    this.unfriend = function(friend){
        //delete friend
        return nodeHandler.sendTo(urlHandler.serviceURL(), "post", "friends/removefriend/",  {"friend":friend.id});
    };

    this.unfollow = function(following){
        //stop following
        return nodeHandler.sendTo(urlHandler.serviceURL(), "post", "friends/unfollow/", {"friend":following.author_id});
    };

    this.acceptFriend = function(follower){
        return nodeHandler.sendTo(urlHandler.serviceURL(), "post", "friends/acceptfriend/", {"friend":follower.author_id});
    };

});
