/*
 * Task preview controller
 */
angular.module('flocs.taskPreview')
.controller('taskPreviewCtrl', ['$scope', '$state', '$stateParams', 'taskService',
    function($scope, $state, $stateParams, taskService) {

  function taskIdSelected() {
    $state.go('task-preview-set', {taskId: $scope.tasks.selected});
  }

  $scope.tasks = {
    selected: null,
    options: []
  };

  // if task id is specified by the url, set this task id
  if ($stateParams.taskId !== undefined) {
    $scope.tasks.selected = $stateParams.taskId;
    taskService.gettingTaskById($scope.tasks.selected);
  }

  taskService.gettingAllTaskIds()
    .then(function(taskIds) {
      $scope.tasks.options = taskIds;
    });

  $scope.onTaskIdSelected = taskIdSelected;

}]);
