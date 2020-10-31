// Sass configuration
var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('sass', function (cb) {
  gulp
    .src('assets/illuminate/src/*.scss')
    .pipe(sass())
    .pipe(
      gulp.dest(function (f) {
        var parent_dir = f.base.substring(0, f.base.lastIndexOf('/'));
        return parent_dir + '/build';
      })
    );
  cb();
});

gulp.task(
  'default',
  gulp.series('sass', function (cb) {
    gulp.watch('assets/illuminate/src/*.scss', gulp.series('sass'));
    cb();
  })
);
