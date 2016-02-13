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

  // === public API ===
  return {
    settingTaskById: settingTaskById,
    settingNextTask: settingNextTask,
    practicingTask: practicingTask,
    taskCompleted: taskCompleted,
    giveUpTask: giveUpTask
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
  function taskCompleted(flowReport) {
    // add flow report and send it to server
    attemptReport['flow-report'] = flowReport;
    practiceDao.sendingAttemptReport(attemptReport).then(function(result) {
      console.log(result);
      // reset attempt object
      attemptReport = null;
      // resolve taskFinnished promise
      taskFinishedDeferred.resolve();
      });
  }

  function attemptFinished(result) {
    if (attemptReport === null) {
      return;
    }

    // we don't count additional attempts after the first successful one
    if (!attemptReport.solved) {
      attemptReport.time = calculateSolvingTime();
      attemptReport.attempt += 1;
      attemptReport.solved = result.solved;

      // If the task has just been solved, it's likely that we will soon
      // send another report with reported flow, but we still send this
      // not-complete report in case a student does not fill the report.
      practiceDao.sendingAttemptReport(attemptReport);
    }

    // Notify about the attempt - even if the task was already solved by a
    // previous attemp (this is necessary, as the user might have closed
    // the report dialog the first time he solved the task)
    taskFinishedDeferred.notify(result);
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
