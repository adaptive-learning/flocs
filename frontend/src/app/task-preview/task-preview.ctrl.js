/**
 * Task preview controller
 * @ngInject
 */
angular.module('flocs.taskPreview')
.controller('taskPreviewCtrl', function($scope, $state, $stateParams,
      taskEnvironmentService, taskDao) {

  function taskIdSelected() {
    $state.go('task-preview-set', {taskId: $scope.tasks.selected});
  }

  function attemptFinished(result) {
    if (result.solved) {
      console.log('Solved! Code:');
      console.log(result.code);
      window.prompt("Solved! Code:", result.code);
    }
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
        taskEnvironmentService.settingTaskByIdWithToolbox(
            $scope.tasks.selected,
            attemptFinished);
      }
    });

  $scope.onTaskIdSelected = taskIdSelected;

});
