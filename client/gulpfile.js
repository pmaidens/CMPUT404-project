/* eslint-disable no-undef, no-console */
var gulp = require("gulp");
var sourcemaps = require("gulp-sourcemaps");
var source = require("vinyl-source-stream");
var buffer = require("vinyl-buffer");
var browserify = require("browserify");
var watchify = require("watchify");
var babelify = require("babelify");
var connect = require("gulp-connect");
var sass = require("gulp-sass");
var less = require("gulp-less");
var merge = require("merge-stream");
var concat = require("gulp-concat");
var fs = require("fs");
/* eslint-enable no-undef */

var paths = {
    bootstrapLess: "./bower_components/bootstrap/less/bootstrap.less",
    mainFile: "./index.js",
    buildLoc: "./build",
    buildFile: "bundle.js",
    sassSrc: "sass/**/*.scss",
    styleLoc: "css/"
}

function compile(watch) {
    var bundler = watchify(browserify(paths.mainFile, { debug: true }).transform(babelify, {presets: ["es2015", "react"]}));

    function rebundle() {
        console.log("[INFO]  Compiling and Bundling Javascript.");
        bundler.bundle()
        .on("error", function(err) { console.error(err); this.emit("end"); })
        .pipe(source(paths.buildFile))
        .pipe(buffer())
        .pipe(sourcemaps.init({ loadMaps: true }))
        .pipe(sourcemaps.write("./"))
        .pipe(gulp.dest(paths.buildLoc));
    }

    if (watch) {
        bundler.on("update", function() {
            rebundle();
        });
    }

    rebundle();
}

function styles(watch) {
    function recompile() {
        console.log("[INFO]  Compiling Stylesheets.");
        var sassStream = gulp.src(paths.sassSrc)
            .pipe(sass().on("error", sass.logError))
            .pipe(concat("scss-files.scss"));
        var bootstrapStream = gulp.src(paths.bootstrapLess)
            .pipe(less())
            .pipe(concat("less-files.less"));
        merge(sassStream, bootstrapStream)
            .pipe(concat("main.css"))
            .pipe(gulp.dest(paths.styleLoc))
    }

    if (watch) {
        gulp.watch(paths.sassSrc, function() { return recompile();});
    }

    recompile();
}

function watch() {
    styles(true);
    return compile(true);
}

gulp.task("build", function() { return compile(); });
gulp.task("watch", function() { return watch(); });
gulp.task("connect", function() {connect.server(); });
gulp.task("styles", function() { return styles(); });

gulp.task("default", ["watch", "connect"]);
