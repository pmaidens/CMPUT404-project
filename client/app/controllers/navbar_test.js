/*eslint-env node, qunit, mocha */

"use strict";

describe("myApp.navbar module", function() {

    beforeEach(module("myApp.navbar"));

    describe("Navbar controller", function(){

        var scope, navbar;

        beforeEach(inject(function ($rootScope, $controller) {
            scope = $rootScope.$new();
            navbar = $controller("NavbarController", {$scope: scope});
        }));

        it("should ....", inject(function() {
            //spec body
            expect(navbar).toBeDefined();
        }));

    });
});