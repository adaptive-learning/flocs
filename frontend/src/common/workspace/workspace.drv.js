/*
 * Workspace Directive
 */
angular.module('flocs.workspace')
.directive('flocsWorkspace', function($window, workspaceService) {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: 'workspace/workspace.tpl.html',
    /*controller: function($scope){
    },*/
    link: function(scope, element, attrs) {

      var blocklyArea = document.getElementById('blocklyArea');
      var blocklyDiv = document.getElementById('blocklyDiv');

      function resize(e) {
        // The official manual for blockly resizing is over-complicated, see:
        // https://developers.google.com/blockly/installation/injecting-resizable
        blocklyDiv.style.left = '0px';
        blocklyDiv.style.top = '0px';
        blocklyDiv.style.width = '100%';
        blocklyDiv.style.height = '100%';
      }
      angular.element($window).bind('resize', resize);
      resize();
      //workspaceService.setBlocklyDiv(blocklyDiv);
    }
  };
});


/*angular.module('flocs.workspace')
.directive('fillSpace', ['$window', function($window) {
  return function(scope, element, attrs) {

    function resize() {
      //var w = angular.element($window);
      var innerHeight = $window.innerHeight;
      var innerWidth = $window.innerWidth;
      console.log('window.inner..', innerHeight, innerWidth);
      console.log('parent..', element.prop('offsetWidth'));
      var width = 100;
      var height = 100;
      element.css('width',  width + 'px');
      element.css('height', height + 'px');
      console.log('resize to', width, height);
    }

    angular.element($window).bind('resize', resize);
    resize();

  };
}]);*/
