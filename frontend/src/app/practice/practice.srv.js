/**
 * Practice Session Service
 * @ngInject
 */
angular.module('flocs.practice')
.factory('practiceService', function ($state,
                                      $timeout,
                                      $q,
                                      practiceDao,
                                      taskEnvironmentService,
                                      sessionBarService,
                                      userService) {

  var attemptReport = null;
  var taskStartTimestamp = null;
  var taskFinishedDeferred = null;
  var taskInstance = null;
  var session = {
    task: null,
    max: null,
    progress: null,
    taskInstances: null,
    active: false
  };
  var sessionOverview = {
  };

  var attemptEvaluation = null;
  var attemptEvaluationDeferred = null;

  var practiceInfo = {
    available: false,
    totalCredits: null,
    freeCredits: null,
    availableBlocks: null,
  };

  userService.onUserChange(userChangeListener);

  // === public API ===
  return {
    settingTaskById: settingTaskById,
    settingNextTask: settingNextTask,
    gettingPracticeInfo: gettingPracticeInfo,
    isSessionOver: isSessionOver,
    gettingSessionOverview: gettingSessionOverview,
    practicingTask: practicingTask,
    taskCompleted: taskCompleted,
    giveUpTask: giveUpTask,
    gettingAttemtpEvaluation: gettingAttemtpEvaluation,
    session: session,
    sessionOverview: sessionOverview,
    practiceInfo: practiceInfo,
  };

  function userChangeListener() {
    if (userService.isUserAvailable()) {
      gettingPracticeInfo();
    } else {
      practiceInfo.available = false;
    }
  }

  function gettingPracticeInfo() {
    return practiceDao.gettingPracticeDetails().then(function(details) {
      practiceInfo.available = true;
      practiceInfo.totalCredits = details.totalCredits;
      practiceInfo.freeCredits = details.freeCredits;
      practiceInfo.solvedTasksCount = details.solvedTasksCount;
      practiceInfo.availableBlocks = details.availableBlocks;
      return practiceInfo;
    }, function() {
      practiceInfo.available = false;
    });
  }

  function gettingSessionOverview() {
    return practiceDao.gettingSessionOverview().then(function(overview) {
      sessionOverview.taskInstances = overview.taskInstances;
      sessionOverview.overallTime = overview.overallTime;
      sessionOverview.percentils = overview.percentils;
      return overview;
    });
  }

  function isSessionOver() {
    return (session.active && (session.task == session.max));
  }

  function settingNextTask() {
    return practiceDao.gettingNextTask().then(function(newTaskInstance) {
      taskInstance = newTaskInstance;
      var newTaskId = taskInstance.task['task-id'];
      $state.go('practice-task', {taskId: newTaskId}, {reload: true});
    });
  }

  function settingTaskById(taskId) {
    if (taskInstance === null || taskInstance.task['task-id'] != taskId) {
      return practiceDao.gettingTaskById(taskId).then(function (newTaskInstance) {
        taskInstance = newTaskInstance;
        startCurrentTask();
        return taskInstance;
      }, function(response) {
        if (response.status == 404) {
          $state.go('httpErrors', {'event': 'taskNotExists'}, {'location': false});
        }
        if (response.status == 403) {
          $state.go('httpErrors', {'event': 'lowLevelForTask'}, {'location': false});
        }
      });
    } else {
      return $timeout(function() {
        startCurrentTask();
        return taskInstance;
      });
    }
  }

  function startCurrentTask() {
    var returnedSession = taskInstance.session;
    if (returnedSession !== null) {
      session.taskInstances = returnedSession['task-instances'];
      session.task = returnedSession.task;
      session.max = returnedSession.max;
      session.progress = (100 / session.max) * (session.task - 1) + 1;
      session.active = true;
      sessionBarService.updateSessionTasksStatutes(session);
    } else {
      session.active = false;
    }
    //userService.setUserAvailable();
    attemptReport = null;
    var newTask = taskInstance.task;
    newAttemptReport(newTask);
    taskStartTimestamp = Date.now();
    taskEnvironmentService.setTask(newTask, taskInstance.newInstructions,
                                   attemptFinished);
    //console.log('new instructions', taskInstance.newInstructions);
    //console.log('all instructions', taskInstance.allInstructions);
  }

  function giveUpTask() {
    var giveUpReport = {
      'task-instance-id': attemptReport['task-instance-id'],
      'time': calculateSolvingTime()
    };
    attemptReport = null;
    // rejecting the task is postponed after successfuly giving up, in order to
    // make sure the skill has been updated before requesting next task
    practiceDao.sendingGiveUpReport(giveUpReport).then(taskFinishedDeferred.reject);
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
    if (attemptReport.solved) {
      taskFinishedDeferred.notify(result);
    } else {
      attemptReport.time = calculateSolvingTime();
      attemptReport.attempt += 1;
      attemptReport.solved = result.solved;
      attemptReport.code = result.code;
      attemptEvaluationDeferred = $q.defer();
      practiceDao.sendingAttemptReport(attemptReport).then(function(newEvaluation) {
        attemptEvaluation = newEvaluation;
        attemptEvaluationDeferred.resolve(attemptEvaluation);
        gettingPracticeInfo();
        taskFinishedDeferred.notify(result);
      });
    }
  }

  function gettingAttemtpEvaluation() {
    return attemptEvaluationDeferred.promise;
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
      'task-instance-id': taskInstance.taskInstanceId,
      'attempt': 0,
      'time': 0,
      'solved': false,
    };
  }
});
