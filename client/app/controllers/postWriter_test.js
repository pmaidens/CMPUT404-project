/*eslint-env node, qunit, mocha */
"use strict";

describe("myApp.postWriter module", function() {

    beforeEach(module("myApp.postWriter"));

    describe("postWriter controller", function(){
        var scope, postWriter;

        beforeEach(inject(function ($rootScope, $controller) {
            scope = $rootScope.$new();
            postWriter = $controller("PostWriterController", {$scope: scope});
        }));

        it("should ....", inject(function() {
            //spec body
            expect(postWriter).toBeDefined();
        }));

    });
});
