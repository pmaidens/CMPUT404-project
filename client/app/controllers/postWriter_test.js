/*eslint-env node, qunit, mocha */
"use strict";

describe("myApp.postWriter module", function() {

    beforeEach(module("myApp.postWriter"));

    describe("postWriter controller", function(){

        it("should ....", inject(function($controller) {
            //spec body
            var postWriter = $controller("postWriter");
            expect(postWriter).toBeDefined();
        }));

    });
});
