/**
 * Practice Session Service
 * @ngInject
 */
angular.module('flocs.practice')
.factory('practiceService', function ($state, $timeout, $q, practiceDao, taskEnvironmentService) {

  var attemptReport = null;
  var taskStartTimestamp = null;
  var taskFinishedDeferred = null;
  var taskInstance = null;
  var attemptEvaluation = {
    'earned-credits': null
  };

  // === public API ===
  return {
    settingTaskById: settingTaskById,
    settingNextTask: settingNextTask,
    practicingTask: practicingTask,
    taskCompleted: taskCompleted,
    giveUpTask: giveUpTask,
    attemptEvaluation: attemptEvaluation,
  };

  function settingNextTask() {
    return practiceDao.gettingNextTask().then(function(newTaskInstance) {
      taskInstance = newTaskInstance;
      var newTaskId = taskInstance.task['task-id'];
      $state.go('practice-task', {'taskId': newTaskId});
    });
  }

  function settingTaskById(taskId) {
    if (taskInstance === null || taskInstance.task['task-id'] != taskId) {
      return practiceDao.gettingTaskById(taskId).then(function (newTaskInstance) {
        taskInstance = newTaskInstance;
        startCurrentTask();
        return taskInstance;
      }, function() {
        $state.go('404', null, {'location': false});
      });
    } else {
      return $timeout(function() {
        startCurrentTask();
        return taskInstance;
      });
    }
  }

  function startCurrentTask() {
    attemptReport = null;
    var newTask = taskInstance['task'];
    newAttemptReport(newTask);
    taskStartTimestamp = Date.now();
    var instructionsText = taskInstance['instructions'];
    taskEnvironmentService.setTask(newTask, attemptFinished,
          instructionsText);
  }

  function giveUpTask() {
    attemptReport['given-up'] = true;
    attemptReport['time'] = calculateSolvingTime();
    practiceDao.sendingAttemptReport(attemptReport);
    attemptReport = null;
    taskFinishedDeferred.reject();
  }

  /*
   * Start practicing task.
   * The promise is finished only after resolving task.
   */
  function practicingTask() {
    taskFinishedDeferred = $q.defer();
    return taskFinishedDeferred.promise;
  }

  /*
   * Send final report about task resolving including flow report.
   */
  function taskCompleted(taskReport) {
    var flowReport = {
      'task-instance-id': attemptReport['task-instance-id'],
      'given-up': attemptReport['task-instance-id'],
      'flow-report': taskReport['flow']
    };
    practiceDao.sendingFlowReport(flowReport).then(function(result) {
      // reset attempt object
      attemptReport = null;
      // resolve taskFinnished promise
      taskFinishedDeferred.resolve(result);
    });
  }

  function attemptFinished(result) {
    if (attemptReport === null) {
      return;
    }
    // ignore additional attempts after the first successful one
    if (!attemptReport.solved) {
      attemptReport.time = calculateSolvingTime();
      attemptReport.attempt += 1;
      attemptReport.solved = result.solved;
      practiceDao.sendingAttemptReport(attemptReport).then(function(response) {
        attemptEvaluation.earnedCredits = response['earned-credits'];
        //result.evaluation = evaluation;
        taskFinishedDeferred.notify(result);
      });
    }
  }

  /*
   * Return time the user spent solving the task as a number of seconds.
   */
  function calculateSolvingTime() {
    var taskFinishedTimestamp = Date.now();
    var milisecondsSpent = taskFinishedTimestamp - taskStartTimestamp;
    var secondsSpent = Math.ceil(milisecondsSpent / 1000);
    return secondsSpent;
  }


  /*
   * Create new report for new attempt
   */
  function newAttemptReport(task) {
    attemptReport = {
      'task-instance-id': taskInstance['task-instance-id'],
      'attempt': 0,
      'time': 0,
      'solved': false,
      'given-up': false,
      'flow-report': 0
    };
  }

});
