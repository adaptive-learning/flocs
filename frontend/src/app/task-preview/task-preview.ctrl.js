/*
 * Task preview controller
 */
angular.module('flocs.taskPreview')
.controller('taskPreviewCtrl', ['$scope', '$state', '$stateParams', 'taskEnvironmentService', 'taskDao',
    function($scope, $state, $stateParams, taskEnvironmentService, taskDao) {

  function taskIdSelected() {
    $state.go('task-preview-set', {taskId: $scope.tasks.selected});
  }

  $scope.tasks = {
    selected: null,
    options: []
  };


  taskDao.gettingAllTaskIds()
    .then(function(taskIds) {
      $scope.tasks.options = taskIds;

      // if task id is specified by the url, select this task id
      if ($stateParams.taskId !== undefined &&
          $scope.tasks.options.indexOf($stateParams.taskId) !== -1) {
        $scope.tasks.selected = $stateParams.taskId;
        taskEnvironmentService.settingTaskById($scope.tasks.selected);
      }
    });

  $scope.onTaskIdSelected = taskIdSelected;

}]);
