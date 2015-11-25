/*
 * Practice Session Service
 */
angular.module('flocs.services')
.factory('practiceSessionService', ['$http', '$timeout', '$q', 'practiceDao', 'taskEnvironmentService',
    function ($http, $timeout, $q, practiceDao, taskEnvironmentService) {

    var attemptReport = null;
    var taskInstanceId = null;
    var taskFinishedDeferred = null;


  // === public API ===
  return {
    practicingTask: practicingTask,
  };

  function practicingTask() {
    taskFinishedDeferred = $q.defer();
    settingNextTask();
    return taskFinishedDeferred.promise;
  }


  // === private implementation ===

  function attemptFinished(result) {
    // we don't count additional attempts after the first successful one
    if (attemptReport !== null) {
      // TODO: add time information to the report
      attemptReport.attempt += 1;
      attemptReport.solved = result.solved;
      /*if (result.solved) {
      //  attemptReport.flowReport = askForFlowReport();
      }*/
      practiceDao.sendingAttemptReport(attemptReport);
    }

    if (result.solved) {
      console.log('Task solved!');
      attemptReport = null;
        taskFinishedDeferred.resolve();
    } else {
      console.log('Unsuccessful attempt.');
    }
  }

  function settingNextTask() {
    // TODO: measure time
    var taskPromise = practiceDao.gettingNextTask()
      .then(function(newTaskInstance) {
        taskInstanceId = newTaskInstance['task-instance-id'];
        var newTask = newTaskInstance['task'];
        newAttemptReport(newTask);
        var instructionsText = newTaskInstance['instructions'];
        taskEnvironmentService.setTask(
                newTask, attemptFinished, instructionsText);
        return newTask;
      });
    return taskPromise;
  }

  /*
   * Create new report for new attempt
   */
  function newAttemptReport(task) {
    attemptReport = {
      'task-instance-id': taskInstanceId,
      //'task-id': task['task-id'],
      'attempt': 0,
      'time': 0,
      'solved': false,
      'flowReport': 0
    };
  }

}]);
