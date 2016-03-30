"use strict";

angular.module("myApp.services.authorHandler", [
    "myApp.services.urlHandler",
    "myApp.services.authenticationHandler"
])
.service("authorHandler", function($q, $http, urlHandler, authenticationHandler) {
    var nodes = [{'url':'http://floating-sands-69681.herokuapp.com/api/','username':'c404','password':'asdf'},{'url':'http://cmput404team4b.herokuapp.com/api/' , 'username': 'team6', 'password':'team6' }];
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
                "url": authenticationHandler.user.url
            },
            friend: friend
        };

       var node1 = [{'url':'http://cmput404-team-4b.herokuapp.com/api/' , 'username': 'team6', 'password':'team6' }];
   // console.log(requestObject);
	//console.log(authenticationHandler.user.id === friend.id);
	if(friend.host != urlHandler.serviceURL()){
	    var encoded = '';
	    nodes.forEach(function(node){

		if (friend.host == node.host){

			encoded = window.btoa(node.username + ':' + node.password);
	
		}

	    });
	  //  console.log("i am HERE "+ friend.host+'/friendRequest/'+friend.displayName,requestObject);
      //  console.log(friend);
        //HARDCODED FOR GROUP 8 WILL HAVE TO CHANGE THIS.
        var node1 = [{'url':'http://cmput404-team-4b.herokuapp.com/api/' , 'username': 'team6', 'password':'team6' }];
        var username = 'team6';
        var password = 'team6'
        encoded = window.btoa('team6:team6');
	    $http.defaults.headers.common.Authorization =  'Basic ' + encoded;
	    return $http.post(urlHandler.remoteURL(friend.host)+'api/friendrequest/',requestObject);

	}else{
            $http.defaults.headers.common.Authorization = authenticationHandler.token;
            return $http.post(urlHandler.serviceURL() + "api/friendrequest/", requestObject);
	    }
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
	$http.defaults.headers.common.Authorization = authenticationHandler.token;
	return $http.post(urlHandler.serviceURL() + 'api/friends/removefriend/' , {friend:friend.author_id});

    };

    this.unfollow = function(following){
	//stop following
	$http.defaults.headers.common.Authorization = authenticationHandler.token;
	return $http.post( urlHandler.serviceURL()+'api/friends/unfollow/',{friend:following.author_id});	

    };

    this.acceptFriend = function(follower){
	$http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.post(urlHandler.serviceURL() + "api/friends/acceptfriend/", {friend:follower.author_id});
    };

});
