/*
 * Practice Session Service
 */
angular.module('flocs.services')
.factory('practiceSessionService', ['$http', '$timeout', 'taskEnvironmentService',
    function ($http, $timeout, taskEnvironmentService) {

    var attemptReport = null;

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
    nextTask();
  }

  function attemptFinished(result) {
    // we don't count additional attempts after the first successful one
    if (attemptReport !== null) {
      // TODO: add time information to the report
      attemptReport.attempt += 1;
      attemptReport.result = result;
      reportAttempt(attemptReport);
    }

    if (result.solved) {
      console.log('Task solved!');
      attemptReport = null;
      $timeout(nextTaskDialog, 400);
    } else {
      console.log('Unsuccessful attempt.');
    }
  }

  function nextTask() {
    taskEnvironmentService.settingNextTask(attemptFinished)
      .then(function(task) {
        newAttemptReport(task);
      });
  }

  function nextTaskDialog() {
    // TODO: show modal ("Continue to next task?")
    alert('Solved. Next task?');
    nextTask();
  }

  function newAttemptReport(task) {
    // TODO: measure time
    attemptReport = {
      'task-id': task.id,
      'attempt': 0,
      'result': null
    };
  }

  /**
   * Send results of last attempt to server
   */
  function reportAttempt(report) {
    $http.post('api/practice/attempt-report', report);
  }
}]);
