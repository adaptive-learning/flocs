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
  grunt.loadNpmTasks('grunt-wiredep');

  /**
   * Paths configuration.
   */
  var pathConfig = {
    // where to store compiled files during development
    development_build_dir: 'development-build',
    development_static_dir: 'development-build/static',

    // where to store compiled files ready for production
    production_build_dir: 'production-build',

    // source codes of our application
    app_files: {
      js: ['src/**/*.js', '!src/**/*.spec.js', '!src/assets/**/*.js'],
      atpl: ['src/app/**/*.tpl.html'],
      ctpl: ['src/common/**/*.tpl.html'],
      css: ['src/css/styles.css'],
      index: 'src/index.html',
    },

    // vendor files
    vendor_files: {
      js: [
        'vendor/angular/angular.js',
        'vendor/angular-route/angular-route.js',
        'vendor/blockly/blockly_compressed.js',
        'vendor/blockly/javascript_compressed.js',
        'vendor/blockly/python_compressed.js',
        'vendor/blockly/blocks_compressed.js',
        'vendor/blockly/msg/js/en.js',
        'vendor/JS-Interpreter/acorn_interpreter.js'
      ],
      css: [
      ],
      assets: [
      ]
    }
  };


  /**
   * Tasks configuration.
   */
  var taskConfig = {
    /**
     * Load package information
     */
    pkg: grunt.file.readJSON("package.json"),

    /**
     * The directories to delete when `grunt clean` is executed.
     */
    clean: [
      '<%= development_build_dir %>',
      '<%= production_build_dir %>'
    ],

    /**
     * Copy project assets (images, fonts, etc.) and javascripts into
     * `development_build_dir` and `production_build_dir`.
     */
    copy: {
      app_assets: {
        files: [
          {
            expand: true,
            cwd: 'src/assets',
            src: [ '**' ],
            dest: '<%= development_static_dir %>/assets/'
          }
       ]
      },
      vendor_assets: {
        files: [
          {
            src: [ '<%= vendor_files.assets %>' ],
            dest: '<%= development_static_dir %>/assets/',
            cwd: '.',
            expand: true,
            flatten: true
          }
       ]
      },
      app_scripts: {
        files: [
          {
            src: [ '<%= app_files.js %>' ],
            dest: '<%= development_static_dir %>/scripts/',
            cwd: '.',
            expand: true
          }
        ]
      },
      vendor_scripts: {
        files: [
          {
            src: [ '<%= vendor_files.js %>' ],
            dest: '<%= development_static_dir %>/scripts/',
            cwd: '.',
            expand: true
          }
        ]
      },
    },

    /**
     * `grunt concat` concatenates multiple source files into a single file.
     */
    concat: {
      /**
       * Concatenates compiled CSS and vendor CSS together.
       */
      all_css: {
        src: [
          '<%= vendor_files.css %>',
          '<%= app_files.css %>'
        ],
        dest: '<%= development_static_dir %>/css/all.css'
      },
    },

    /**
     * Take all of template files and place them into AngularJS's template
     * cache so that all templates are loaded at once.
     */
    html2js: {
      app: {
        options: {
          base: 'src/app'
        },
        src: [ '<%= app_files.atpl %>' ],
        dest: '<%= development_static_dir %>/scripts/templates-app.js'
      },

      common: {
        options: {
          base: 'src/common'
        },
        src: [ '<%= app_files.ctpl %>' ],
        dest: '<%= development_static_dir %>/scripts/templates-common.js'
      }
    },

    /**
     * Include imports of js and css source files into index.html.
     */
    includeSource: {
      options: {
        basePath: '<%= development_build_dir %>/',
        baseUrl: '',
      },
      development: {
        files: {
          '<%= development_build_dir %>/index.html': '<%= app_files.index %>'
        }
      },
    },


    /**
     * Injecting vendor (bower) packages into index.html.
     */
    /*wiredep: {

      development: {
        src: '<%= development_build_dir %>/index.html',

        options: {
        }
      }
    }
    */

    /**
     * And for rapid development, we have a watch set up that checks to see if
     * any of the files listed below change, and then to execute the listed
     * tasks when they do.
     */
    delta: {
      /**
       * By default, we want the Live Reload to work for all tasks; this is
       * overridden in some tasks (like this file) where browser resources are
       * unaffected. It runs by default on port 35729, which your browser
       * plugin should auto-detect.
       */
      options: {
        livereload: true
      },

      /**
       * When our JavaScript source files change, we want to run lint them and
       * run our unit tests.
       */
      jssrc: {
        files: [
          '<%= app_files.js %>'
        ],
        tasks: [ 'copy:app_scripts' ]
      },

      /**
       * When assets are changed, copy them. Note that this will *not* copy new
       * files, so this is probably not very useful.
       */
      assets: {
        files: [
          'src/assets/**/*'
        ],
        tasks: [ 'copy:app_assets', 'copy:vendor_assets' ]
      },

      /**
       * When index.html changes, we need to compile it.
       */
      html: {
        files: [ '<%= app_files.index %>' ],
        tasks: [ 'includeSource:development' ]
      },

      /**
       * When our templates change, we only rewrite the template cache.
       */
      tpls: {
        files: [
          '<%= app_files.atpl %>',
          '<%= app_files.ctpl %>'
        ],
        tasks: [ 'html2js' ]
      },

      /**
       * When the CSS files change, we need to concat them to the build folder.
       */
      css: {
        files: [ '<%= app_files.css %>' ],
        tasks: [ 'concat:all_css' ]
      },

    }


  };

  /**
   * In order to make it safe to just compile or copy *only* what was changed,
   * we need to ensure we are starting from a clean, fresh build. So we rename
   * the `watch` task to `delta` (that's why the configuration var above is
   * `delta`) and then add a new task called `watch` that does a clean build
   * before watching for changes.
   */
  grunt.renameTask( 'watch', 'delta' );
  grunt.registerTask( 'watch', [ 'development-build', 'delta' ] );

  grunt.initConfig(grunt.util._.extend(taskConfig, pathConfig));

  /**
   * The default task is to do the development build.
   */
  grunt.registerTask( 'default', ['development-build'] );

  /**
   * Development build task.
   */
  grunt.registerTask( 'development-build', [
    'clean',
    'html2js',
    'copy:app_assets',
    'copy:vendor_assets',
    'copy:app_scripts',
    'copy:vendor_scripts',
    'concat:all_css',
    'includeSource:development',
  ]);

  /**
   * Production build task (gets the application ready for deployment.
   */
  grunt.registerTask( 'production-build', [
      // TODO
  ]);

};
