/*eslint-env node, qunit, mocha */
"use strict";

describe("myApp.profile module", function() {

    beforeEach(module("myApp.profile"));

    describe("profile controller", function(){
        var scope, profile;

        beforeEach(inject(function ($rootScope, $controller) {
            scope = $rootScope.$new();
            profile = $controller("Profile", {$scope: scope});
        }));

        it("should ....", inject(function() {
            //spec body
            expect(profile).toBeDefined();
        }));

    });
});
