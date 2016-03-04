/*eslint-env node, qunit, mocha */

"use strict";

describe("myApp.login module", function() {

    beforeEach(module("myApp.login"));

    describe("Login controller", function(){

        var scope, login;

        beforeEach(inject(function ($rootScope, $controller) {
            scope = $rootScope.$new();
            login = $controller("LoginController", {$scope: scope});
        }));

        it("should ....", inject(function() {
            //spec body
            expect(login).toBeDefined();
        }));

    });
});