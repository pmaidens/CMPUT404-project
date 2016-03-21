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

.controller("FriendsFeedController", function($scope, $http, $location, $q, authenticationHandler, urlHandler, authorHandler) {
	$scope.potentialFriends = [];
	$scope.user = authenticationHandler.user;
    $scope.isFollowing = false;
    $scope.hasFollowers = false;
    $scope.friends = $scope.user.friends;
    //console.log($scope.friends.length!=0);

    authorHandler.getAllAuthors().then(function(result) {

        $scope.potentialFriends = result.data;
        var followers = $scope.getfollowers();

        $q.all([followers||$scope.followers2, getRefresh($scope.user)]).then(function(){
            filteredStuff($scope.potentialFriends,$scope.followers,$scope.user,$scope.user.friends)
        })
        //var friends = getfriends($scope potentialFriends);
	//STEP 1 
	//STEP 2
	getAuthorsFromNodes(nodes);
	console.log($scope.nodeAuthors);
     
    });

    $scope.getfollowers2 = function(){

	 authorHandler.getFollowers($scope.user.id).then(function(result){

	     $scope.followers2 = result.data[0].friendrequests;
	     
	 });

    };
    $scope.getfollowers2();

    $scope.getfollowers = function(){
        // return authorHandler.getFollowers($scope.user.id).then(function(result){
        // 	//console.log($scope.followers);
        //     $scope.followers = result.data[0].friendrequests;
        // 	if($scope.followers.length){
        // 	    $scope.hasFollowers = true;
        // 	}
	//Step 3
	//FILTER HERE 
	//filteredStuff($scope.allAuthors, $scope.followers, authentication.user,authentication.user.friends)
        // });
        return $q(function(resolve, reject) {
            authorHandler.getFollowers($scope.user.id).then(function(result){
                // console.log($scope.followers);
                $scope.followers = result.data[0].friendrequests;
                if($scope.followers.length){
                    $scope.hasFollowers = true;
                }
                resolve(result);
            });
        });
    };  

    var getRefresh = function(user){
        return authorHandler.getAuthor(user.id).then(function(result){
            $scope.followers = result.data.friendrequests;
            $scope.friends = result.data.friends;
        });
    }; 
    
    var filteredStuff = function(potentialFriends, followers, user, friends){

        $scope.filteredPotentialFriends = potentialFriends.filter(function(filteredPotentialFriends){
            console.log(filteredPotentialFriends.id);
            return (!followers.some(function(follower){
                return filteredPotentialFriends.id === follower.author_id;
            })
            && !friends.some(function(friend){
                return filteredPotentialFriends.id === friend.author_id;
            })&& filteredPotentialFriends.id !== user.id);
        
        });
    };

    authorHandler.getFollowing($scope.user.id).then(function(result){
        $scope.friendsSOON = result.data[0].following;
	if($scope.friendsSOON.length){

	    $scope.isFollowing = true;
	}
	

    
    });



    $scope.makeFriendReq = function(author){
	console.log(author);
        var friend = {
            "id": author.id,
            "host":author.host,
            "displayName": author.displayname,
            "url": author.url
        };

        authorHandler.postFriendRequest(friend).then(function() {alert("Friend Request Sent")}, function() {alert("uh-oh, something went wrong")});
    };

   


    $scope.unfriend = function(friend){

	authorHandler.unfriend(friend).then(function(result){

	    //success!
	    alert('unfriended!');
	    $window.location.reload();


	});

    };
    
    $scope.unfollow = function(following){

	authorHandler.unfollow(following).then(function(result){

	    //success!
	    alert('unfollowed!');
	    $window.location.reload();
	});

    };

    $scope.acceptFriend = function(follower){
	
	authorHandler.acceptFriend(follower).then(function(result){

		
	    alert('friend accepted!');
	    $window.location.reload();
	

	});

    };

    var nodes = [{'url':'http://floating-sands-69681.herokuapp.com/api/','username':'c404','password':'asdf'},{'url':'http://cmput404team4b.herokuapp.com/api/' , 'username': 'team6', 'password':'team6' }];


    var getAuthorsFromNodes = function(nodes){

	var nodeAuthors = [];
	var encoded='';

	for (var i=0; i < nodes.length ; i++){
	    //console.log(nodes);
	    
	    //TODO CHANGE encoded SO THAT IT MATCHES WHAT EACH GROUP WANTS.
	    if (nodes[i].url =='http://cmput404teamb.herokuapp.com/api'){


		encoded = window.btoa('team6@' + nodes[i].username + ':' + nodes[i].password);

	    }
	    else{
		encoded = window.btoa('team6@'+ nodes[i].username + ':' + nodes[i].password);


	    }
	    $http.defaults.headers.common.Authorization = 'Basic ' + encoded; 
	    $http.defaults.useXDomain=true;
	    $http({

		method:'GET',
		url: nodes[i].url+'author/',
		headers:{
		    

		}
		

	    }).then(function(result){

		console.log(result.data);
		//TODO 
		$scope.nodeAuthors = result.data;
		//STEP2

	    });
	


	}
    }

    


});

