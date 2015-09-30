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
        'vendor/blockly/blockly_compressed.js',
        'vendor/blockly/javascript_compressed.js',
        'vendor/blockly/python_compressed.js',
        'vendor/blockly/blocks_compressed.js',
        'vendor/blockly/msg/js/en.js',
        'vendor/acorn_interpreter.js'
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


  };

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
    'copy:app_assets', 'copy:vendor_assets',
    'copy:app_scripts', 'copy:vendor_scripts',
    'concat:all_css',
    'includeSource:development'
  ]);

  /**
   * Production build task (gets the application ready for deployment.
   */
  grunt.registerTask( 'production-build', [
      // TODO
  ]);

};
