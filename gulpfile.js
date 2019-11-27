var gulp = require('gulp');
var sass = require('gulp-sass');
var concatCss = require('gulp-concat-css');

var sassGlob = require('gulp-sass-glob');

gulp.task('sass', function(){
    return gulp.src('static/styles/main.SCSS')
        .pipe(sass())
        // .pipe(sassGlob())
        .pipe(concatCss("styles.css"))
        .pipe(gulp.dest('static/styles'));
});

gulp.task('default', function(){
    console.log("Compiling...");
    sass();
    console.log("enjoy coding ;) starting watcher now...");
    gulp.watch('static/styles/sass/**/*.SCSS', gulp.series('sass'));

});