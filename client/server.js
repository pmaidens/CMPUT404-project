/*eslint-env node*/

var express = require("express");
var path = require("path");
var url = require("url");

var app = express();

app.use(express.static(__dirname));

app.get("*", function (req, res) {
    var resource = url.parse(req.url).pathname;
    if(~resource.indexOf("node_modules") || ~resource.indexOf("bower_components")) {
        res.sendFile(path.join(__dirname));
    } else {
        if(resource.slice(-1) !== "/") {
            res.sendFile(path.join(__dirname + "/app" + resource));
        } else {
            res.sendFile(path.join(__dirname + "/app" + resource, "index.html"));
        }

    }
});

var PORT = process.env.OPENSHIFT_NODEJS_PORT || process.env.PORT || 8080;
var server_ip_address = process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';
app.listen(PORT, server_ip_address, function() {
    console.log("Production Express server running at " + server_ip_address + ":" + PORT);
});
