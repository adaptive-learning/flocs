/*
 * Workspace Directive
 */
angular.module('flocs.workspace')
.directive('flocsWorkspace', ['workspaceService', function(workspaceService) {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: 'workspace/workspace.tpl.html',
    /*controller: function($scope){
    },*/
    link: function(scope, element, attrs) {

      // inject blockly into the workspace
      var blocklyDiv = Blockly.inject('blocklyDiv', {
        // TODO: create special service for initial settings
        toolbox: '<xml></xml>'
      });

      workspaceService.setBlocklyDiv(blocklyDiv);
    }
  };
}]);

