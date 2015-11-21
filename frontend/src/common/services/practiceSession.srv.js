/*
 * Practice Session Service
 */
angular.module('flocs.services')
.factory('practiceSessionService', ['$http', '$timeout', 'practiceDao', 'taskEnvironmentService',
    function ($http, $timeout, practiceDao, taskEnvironmentService) {

    var attemptReport = null;
    var taskInstanceId = null;

  // === public API ===
  return {
    startPracticeSession: startPracticeSession
  };

  // === private implementation ===

  /**
   * Start a new practice session
   */
  function startPracticeSession() {
    // start first task
    settingNextTask();
  }

  function attemptFinished(result) {
    // we don't count additional attempts after the first successful one
    if (attemptReport !== null) {
      // TODO: add time information to the report
      attemptReport.attempt += 1;
      attemptReport.solved = result.solved;
      practiceDao.sendingAttemptReport(attemptReport);
    }

    if (result.solved) {
      console.log('Task solved!');
      attemptReport = null;
      $timeout(nextTaskDialog, 400);
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
        taskEnvironmentService.setTask(newTask, attemptFinished);
        return newTask;
      });
    return taskPromise;
  }

  function nextTaskDialog() {
    // TODO: show modal ("Continue to next task?")
    alert('Solved. Next task?');
    settingNextTask();
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
      'solved': false
    };
  }
}]);
