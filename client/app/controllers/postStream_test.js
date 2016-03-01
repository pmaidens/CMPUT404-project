/*eslint-env node, qunit, mocha */

"use strict";

describe("myApp.postStream module", function() {

    beforeEach(module("myApp.postStream"));

    describe("PostStream controller", function(){

        it("should ....", inject(function($controller) {
            //spec body
            var postStreamController = $controller("PostStreamController");
            expect(postStreamController).toBeDefined();
        }));

    });
});
