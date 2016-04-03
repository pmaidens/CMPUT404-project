"use strict";

angular.module("myApp.friendsFeed", [
    "ngRoute",
    "myApp.services.authenticationHandler",
    "myApp.services.urlHandler",
    "myApp.services.authorHandler"
])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/friendsFeed", {
        templateUrl: "partials/friendsFeed.html",
        controller: "FriendsFeedController"
    });
}])

.controller("FriendsFeedController", function($scope, $http, $location, $q, $route, authenticationHandler, urlHandler, authorHandler) {
    $scope.localAuthors = [];
    $scope.user = authenticationHandler.user;
    $scope.isFollowing = false;
    $scope.hasFollowers = false;
    $scope.request = false;
    $scope.friends = $scope.user.friends;
    var friends = $scope.friends;
    console.log($scope.user);
    authenticationHandler.determineUser($scope.user.displayName);
    $scope.nodeAuthors = [];
    authorHandler.getAllAuthors().then(function (results) {
        results.data.forEach(function (author) {
            var pushAuthorTrue = true;
            if(~urlHandler.apiURL().indexOf(author.host)) {
                for (var i = 0; i < friends.length; i++){
                   if(friends[i].id == author.id){
                        pushAuthorTrue = false;

                    }
               }
               if(pushAuthorTrue){

                    $scope.localAuthors.push(author);


               }
            } else {
                $scope.nodeAuthors.push(author);
            }
        });
           console.log($scope.localAuthors);
    });

    // authorHandler.getAllAuthors().then(function(result) {
    //     $scope.localAuthors = result.data;
    //     var followers = $scope.getfollowers();
    //
    //     $q.all([followers||$scope.followers2, getRefresh($scope.user)]).then(function(){
    //         filteredStuff($scope.localAuthors,$scope.followers,$scope.user,$scope.user.friends);
    //     });
    //
    //     //STEP 1
    //     //STEP 2
    //     //console.log($scope.nodeAuthors);
    // });



     $scope.getfollowers2 = function(){
         authorHandler.getFollowers($scope.user.id).then(function(result){
            $scope.followers2 = result.data[0].friendrequests;
            if($scope.followers2.length){

                $scope.hasFollowers = true;    
            }
            
         });
     };
     $scope.getfollowers2();

    // $scope.getfollowers = function(){
    //     // return authorHandler.getFollowers($scope.user.id).then(function(result){
    //     // 	//console.log($scope.followers);
    //     //     $scope.followers = result.data[0].friendrequests;
    //     // 	if($scope.followers.length){
    //     // 	    $scope.hasFollowers = true;
    //     // 	}
    //     //Step 3
    //     //FILTER HERE
    //     //filteredStuff($scope.allAuthors, $scope.followers, authentication.user,authentication.user.friends)
    //     // });
    //     return $q(function(resolve, reject) { //eslint-disable-line no-unused-vars
    //         authorHandler.getFollowers($scope.user.id).then(function(result){
    //             // console.log($scope.followers);
    //             $scope.followers = result.data[0].friendrequests;
    //             if($scope.followers.length){
    //                 $scope.hasFollowers = true;
    //             }
    //             resolve(result);
    //         });
    //     });
    // };

     var getRefresh = function(user){
         return authorHandler.getAuthor(user.id).then(function(result){
             $scope.followers = result.data.friendrequests;
             $scope.friends = result.data.friends;
         });
     };

    // var filteredStuff = function(localAuthors, followers, user, friends){
    //     $scope.filteredlocalAuthors = localAuthors.filter(function(filteredlocalAuthors){
    //         return (!followers.some(function(follower){
    //             return filteredlocalAuthors.id === follower.author_id;
    //         })
    //         && !friends.some(function(friend){
    //             return filteredlocalAuthors.id === friend.author_id;
    //         })&& filteredlocalAuthors.id !== user.id);
    //     });
    // };

    authorHandler.getFollowing($scope.user.id).then(function(result){
        $scope.friendsSOON = result.data[0].following;
        if($scope.friendsSOON.length){
            $scope.isFollowing = true;
        }
    });

    $scope.makeFriendReq = function(author){
        var friend = {
            "id": author.id,
            "host":author.host,
            "displayName": author.displayName,
            "url": author.url || author.host
        };
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

        authorHandler.postFriendRequest(friend).then(function() {
            $http.defaults.headers.common.Authorization = authenticationHandler.token;
                      alert("Friend Request Sent");
                      console.log(urlHandler.serviceURL());
                      console.log(author.host);
            if(urlHandler.apiURL().indexOf(author.host) == -1){
                $http.post(urlHandler.serviceURL() + "api/addfollower/",requestObject).then(function(){
                    $route.reload();
            });
            }
        }, function() {
            alert("uh-oh, something went wrong");
        });
               $route.reload();

    };
    $scope.unfriend = function(friend){
        authorHandler.unfriend(friend).then(function(){
            alert("unfriended!");
            authenticationHandler.determineUser($scope.user.displayName);
            $route.reload();
        });
    };

    $scope.unfollow = function(following){
        authorHandler.unfollow(following).then(function(){
            alert("unfollowed!");

            authenticationHandler.determineUser($scope.user.displayName);
            $route.reload();
        });
    };

    $scope.acceptFriend = function(follower){
          $route.reload();
        authorHandler.acceptFriend(follower).then(function(){
    
            alert("friend accepted!");
       
            authenticationHandler.determineUser($scope.user.displayName);
        
        });
                   $route.reload();
    };


    $scope.showFollowTag = function(friend){
	var show = false;
	$scope.friendsSOON.forEach(function(following){
	    if (friend.host == following.host){
		if(friend.id == following.author_id){
		    show = true;
		    return;
		}

	    }

	});

	return show;
    };

});
