/*eslint-env node, qunit, mocha */

"use strict";

describe("myApp.postStream module", function() {

    beforeEach(module("myApp.postStream"));

    describe("PostStream controller", function(){

        var scope, postStream;

        beforeEach(inject(function ($rootScope, $controller) {
            scope = $rootScope.$new();
            postStream = $controller("PostStreamController", {$scope: scope});
        }));

        it("should ....", inject(function() {
            //spec body
            expect(postStream).toBeDefined();
        }));

    });
});
