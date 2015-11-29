/*
 * Practice Session Service
 */
angular.module('flocs.services')
  .factory('practiceSessionService', ['$http', '$timeout', '$q', 'practiceDao', 'taskEnvironmentService',
    function ($http, $timeout, $q, practiceDao, taskEnvironmentService) {

      var attemptReport = null;
      var taskInstanceId = null;
      var taskStartTimestamp = null;
      var taskFinishedDeferred = null;

      // === public API ===
      return {
        practicingTask: practicingTask,
        sendFinalAttempt: sendFinalAttempt,
      };

      /*
       * Start practicing task.
       * The promise is finished only after resolving task.
       */
      function practicingTask() {
        taskFinishedDeferred = $q.defer();
        settingNextTask();
        return taskFinishedDeferred.promise;
      }

      /*
       * Send final report about task resolving including flow report.
       */
      function sendFinalAttempt(flowReport) {
        // add flow report
        attemptReport.flowReport = flowReport;

        // send
        practiceDao.sendingAttemptReport(attemptReport);

        // reset attempt object -> prepare for next task
        attemptReport = null;
      }

      function attemptFinished(result) {
        // we don't count additional attempts after the first successful one
        if (attemptReport !== null) {
          attemptReport.time = calculateSolvingTime();
          attemptReport.attempt += 1;
          attemptReport.solved = result.solved;
          if (result.solved) {
            // give control back to practice controller
            taskFinishedDeferred.resolve();
          } else {
            // send unfinished attempt
            console.log('Unsuccessful attempt.');
            practiceDao.sendingAttemptReport(attemptReport);
          }
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

      function settingNextTask() {
        var taskPromise = practiceDao.gettingNextTask()
          .then(function (newTaskInstance) {
            taskInstanceId = newTaskInstance['task-instance-id'];
            var newTask = newTaskInstance['task'];
            newAttemptReport(newTask);
            taskStartTimestamp = Date.now();
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
