/*
 * Main practice controller
 */
angular.module('flocs.practice')
.controller('practiceCtrl', ['$scope', 'taskEnvironmentService',
    function($scope, taskEnvironemntService) {

  function nextTask() {
    taskEnvironemntService.settingNextTask();
    //console.log('next task');
    //taskService.taskFinished().then(function() {
    /*taskService.gettingNextTask().then(function() {
      mazeService.set(taskService.getMazeSettings());
      workspaceService.set(taskService.getWorkspaceSettings());
    });*/
  }

  // set first task
  nextTask();

}]);

