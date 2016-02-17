module.exports = function (grunt) {

  /**
   * Load required Grunt tasks.
   */
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-html2js');
  grunt.loadNpmTasks('grunt-include-source');
  grunt.loadNpmTasks('grunt-karma');
  grunt.loadNpmTasks('grunt-ng-annotate');

  /**
   * Paths configuration.
   */
  var pathConfig = {
    // where to store compiled files during development
    development_build_dir:  'development-build',
    development_static_dir: 'development-build/static',

    // where to store compiled files ready for production
    production_build_dir:  'production-build',
    production_static_dir: 'production-build/static',

    app_dirs: {
      assets: 'src/assets/'
    },
    app_files: {
      assets: 'src/assets/**/*',
      js: ['src/common/**/*.mdl.js', 'src/app/**/*.mdl.js',
           'src/common/**/*.js', 'src/app/**/*.js',
           '!src/**/*.spec.js'],
      jsunit: ['src/**/*.spec.js'],
      app_tpl: ['src/app/**/*.tpl.html'],
      common_tpl: ['src/common/**/*.tpl.html'],
      css: ['src/css/styles.css', 'src/**/*.css'],
      index: 'src/index.html',
    },

    test_files: {
      js : [
        'node_modules/angular-mocks/angular-mocks.js'
      ]
    },

    vendor_files: {
      js: [
        'vendor/jquery/dist/jquery.js',
        'vendor/angular/angular.js',
        'vendor/angular-ui-router/release/angular-ui-router.js',
        'vendor/angular-animate/angular-animate.min.js',
        'vendor/blockly/blockly_compressed.js',
        'vendor/blockly/javascript_compressed.js',
        'vendor/blockly/python_compressed.js',
        'vendor/blockly/blocks_compressed.js',
        'vendor/JS-Interpreter/acorn_interpreter.js',
        'vendor/ngDialog/js/ngDialog.js',
        'vendor/angular-bootstrap/ui-bootstrap-tpls.js',
        'vendor/angular-spinkit/build/angular-spinkit.min.js',
        'vendor/angular-translate/angular-translate.js',
        'vendor/messageformat/messageformat.js',
        'vendor/messageformat/locale/cs.js',
        'vendor/messageformat/locale/en.js',
        'vendor/angular-translate-interpolation-messageformat/angular-translate-interpolation-messageformat.min.js',
      ],
      css: [
        'vendor/bootstrap/dist/css/bootstrap.min.css',
        'vendor/ngDialog/css/ngDialog.css',
        'vendor/ngDialog/css/ngDialog-theme-plain.css',
        'vendor/ngDialog/css/ngDialog-theme-default.css',
        'vendor/angular-spinkit/build/angular-spinkit.min.css'
      ],
      assets: [
        //'vendor/bootstrap/dist/fonts/glyphicons-halflings-regular.svg'
      ]
    },

    // directory for temporary files (for semi-results of the building process)
    temp: '.tmp',
  };


  /**
   * Tasks configuration.
   */
  var taskConfig = {
    // package information
    pkg: grunt.file.readJSON("package.json"),

    clean: {
      temp: ['<%= temp %>'],
      build: ['<%= development_build_dir %>', '<%= production_build_dir %>']
    },

    copy: {
      // copy from temporary to development directory
      development: {
        files: [
          {
            expand: true,
            cwd: '<%= temp %>',
            src: [
              'assets/**',
              'css/**',
              'js/**',
            ],
            dest: '<%= development_static_dir %>'
          },
          /*{
            expand: true,
            cwd: '<%= temp %>',
            src: ['index.html'],
            dest: '<%= development_build_dir %>'
          }*/
        ]
      },
      // copy from temporary to production directory
      production: {
        files: [
          {
            expand: true,
            cwd: '<%= temp %>',
            src: [
              'assets/**',
              'css/vendor.css',
              'css/app.css',
              'js/vendor.min.js',
              'js/app.min.js',
            ],
            dest: '<%= production_static_dir %>'
          },
          /*{
            expand: true,
            cwd: '<%= temp %>',
            src: ['index.html'],
            dest: '<%= production_build_dir %>'
          }*/
        ]
      },
      // copy both app and vendor assets to temporary directory for assets
      assets: {
        files: [
          {
            expand: true,
            cwd: '<%= app_dirs.assets %>',
            src: ['**'],
            dest: '<%= temp %>/assets/'
          },
          {
            expand: true,
            cwd: '.',
            src: ['<%= vendor_files.assets %>'],
            dest: '<%= temp %>/assets/',
            flatten: true
          }
       ]
      },
      // copy app scripts to temporary directory for scripts
      app_js: {
        files: [
          {
            expand: true,
            cwd: '.',
            src: ['<%= app_files.js %>'],
            dest: '<%= temp %>/js/'
          }
        ]
      }
    },

    ngAnnotate: {
      all: {
        files: [{
          expand: true,
          src: ['<%= temp %>/js/**/*.js'],
        }]
      }
    },

    // Concatenation of js and css files
    concat: {
      app_css: {
        src: '<%= app_files.css %>',
        dest: '<%= temp %>/css/app.css'
      },
      vendor_css: {
        src: '<%= vendor_files.css %>',
        dest: '<%= temp %>/css/vendor.css'
      },
      app_js: {
        src: [
          '<%= app_files.js %>',
          '<%= html2js.app.dest %>',
          '<%= html2js.common.dest %>'
        ],
        dest: '<%= temp %>/js/app.js',
      },
      vendor_js: {
        src: '<%= vendor_files.js %>',
        dest: '<%= temp %>/js/vendor.js',
      },
    },

    // Create a js files containing html templates
    html2js: {
      options: {
        singleModule: true
      },
      app: {
        options: {base: 'src/app'},
        src: ['<%= app_files.app_tpl %>'],
        dest: '<%= temp %>/js/templates-app.js'
      },
      common: {
        options: {base: 'src/common'},
        src: ['<%= app_files.common_tpl %>'],
        dest: '<%= temp %>/js/templates-common.js'
      }
    },

    // Include imports of js and css source files into index.html
    includeSource: {
      options: {
        baseUrl: '/static/'
      },
      development: {
        options: {
          basePath: '<%= development_static_dir %>'
        },
        files: {
          '<%= development_build_dir %>/index.html': '<%= app_files.index %>'
        }
      },
      production: {
        options: {
          basePath: '<%= production_static_dir %>'
        },
        files: {
          '<%= production_build_dir %>/index.html': '<%= app_files.index %>'
        }
      }
    },

    // Linting js files (including this Gruntfile.js and unit tests).
    jshint: {
      options: {
        jshintrc: true
      },
      gruntfile: ['Gruntfile.js'],
      src: ['<%= app_files.js %>'],
      test: ['<%= app_files.jsunit %>'],
    },

    // Minification of source codes
    uglify: {
      js: {
        files: {
          '<%= temp %>/js/vendor.min.js': '<%= temp %>/js/vendor.js',
          '<%= temp %>/js/app.min.js': '<%= temp %>/js/app.js'
        }
      }
    },

    // Watch for changes
    watch: {
      // Live reload runs by default on port 35729, which should by
      // auto-detected by browser.
      options: {
        livereload: true
      },

      // When the Gruntfile changes, we just want to lint it.
      gruntfile: {
        files: 'Gruntfile.js',
        tasks: ['jshint:gruntfile'],
        options: {livereload: false}
      },

      // When js source files change, lint them and copy to development dir.
      // Note that it only works for change of already existing assets - if
      // you add a new asset, you need to run `grunt development-build` (or
      // restart `grunt work`).
      jssrc: {
        files: [
          '<%= app_files.js %>'
        ],
        tasks: [
          'jshint:src',
          'clean:temp',
          'copy:app_js',
          'ngAnnotate:all',
          'copy:development'
        ]
      },

      // When a js unit tests change, we only want to lint them
      jsunit: {
        files: [
          '<%= app_files.jsunit %>'
        ],
        tasks: ['jshint:test'],
        options: {livereload: false}
      },

      // When assets are changed, copy them. Note that it only works for change
      // of already existing assets - if you add a new asset, you need to run
      // `grunt development-build` (or restart `grunt work`).
      assets: {
        files: [
          '<%= vendor_files.assets %>',
          '<%= app_files.assets %>'
        ],
        tasks: ['clean:temp', 'copy:assets', 'copy:development']
      },

      // When index.html changes, compile it (and move to dev dir).
      index: {
        files: ['<%= app_files.index %>'],
        tasks: ['compileIndex:development']
      },

      // When templates change, rewrite the template cache.
      tpls: {
        files: [
          '<%= app_files.app_tpl %>',
          '<%= app_files.common_tpl %>'
        ],
        tasks: ['clean:temp', 'compileTemplates', 'copy:development']
      },

      // When the CSS files change, concat them to the dev dir.
      css: {
        files: ['<%= app_files.css %>'],
        tasks: ['clean:temp', 'concat:app_css', 'copy:development']
      },

    },

    // Tests configuration.
    karma: {
      // unit testing
      unit: {
        browsers: ['Chrome'],
        frameworks: ['jasmine'],
        basePath: '',
        plugins: [ 'karma-jasmine', 'karma-chrome-launcher'],
        files: [
          // libs
          {  src :
              pathConfig.vendor_files.js.concat(
                  pathConfig.test_files.js).concat(
                  pathConfig.app_files.js).concat(
                  pathConfig.app_files.jsunit)
          }
        ],
        reporters: ['dots'],
        port: 9019,
        runnerPort : 9100,
        urlRoot : '/',
        colors: true,
        logLevel: 'INFO',
        autoWatch: false,
        singleRun: true
      }
    }
  };

  // TODO: the following is deprecated, find another way
  grunt.initConfig(grunt.util._.extend(taskConfig, pathConfig));

  // Lingint task
  grunt.registerTask('lint', ['jshint']);

  // Create js with all html templates
  grunt.registerTask('compileTemplates', ['html2js:common', 'html2js:app']);

  // Compile index to include css and js imports
  grunt.registerTask('compileIndex', 'Compile index.html', function (target) {
    grunt.task.run('includeSource:' + target);
  });

  // Development build task.
  grunt.registerTask('development-build', [
    'clean',
    'lint',
    'compileTemplates',
    'copy:app_js',
    'ngAnnotate:all',
    'concat:vendor_js',
    'concat:app_css',
    'concat:vendor_css',
    'copy:assets',
    'copy:development',
    'compileIndex:development',
    'clean:temp'
  ]);

  // Production build task (gets the application ready for deployment).
  grunt.registerTask('production-build', [
    'clean',
    'lint',
    'compileTemplates',
    'concat:app_js',
    'ngAnnotate:all',
    'concat:vendor_js',
    'concat:app_css',
    'concat:vendor_css',
    'copy:assets',
    'uglify',
    'copy:production',
    'compileIndex:production',
    'clean:temp'
  ]);

  // For developing we want to run development-build and then watch for changes
  grunt.registerTask('work', ['development-build', 'watch']);

  // Default task (when `grunt` without additional arguments is run)
  grunt.registerTask('default', ['work']);


};
