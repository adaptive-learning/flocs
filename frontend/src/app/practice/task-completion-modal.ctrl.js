/*
 * Controller for task completion modal
 */
angular.module('flocs.user')
.controller('taskCompletionModalCtrl', function($scope, $uibModalInstance,
      $uibModal, $timeout, $interval, practiceService, flowFactory) {

  $scope.reportFlow = function(flowKey) {
    // we try to convert the key to flow just to make sure the key corresponds
    // to an actual flow (to throw explicit error if the set of possible values
    // change)
    var flow = flowFactory.fromKey(flowKey);
    var report = {'flow': flow.key};
    $uibModalInstance.close(report);
  };

  // TODO: decomposition
  practiceService.gettingAttemtpEvaluation().then(function(evaluation) {
    $scope.evaluation = evaluation;
    if (!evaluation.taskSolvedFirstTime) {
      return;
    }

    $scope.state = {
      step: 0,
      level: $scope.evaluation.progress.length > 0 ? $scope.evaluation.progress[0].level : null,
      newBlocks: [],
    };
    angular.forEach($scope.evaluation.progress, function(level) {
      level.credits = level.creditsFrom;
      level.partialCredits = level.creditsFrom;
    });

    var animatingProgress = function() {
      var step = $scope.state.step;
      var level = $scope.evaluation.progress[step];
      return animatingProgressWithinLevel(level).then(function() {
        return $timeout(levelup, 300).then(function() {
          return $timeout(nextStep, 2500);
        });
      });
      function levelup() {
        if (step + 1 < $scope.evaluation.progress.length) {
          $scope.state.level = $scope.evaluation.progress[step+1].level;
        }
        angular.forEach(level.blocks, function(block) {
          $scope.state.newBlocks.push(block);
        });
      }
      function nextStep() {
        if (step + 1 < $scope.evaluation.progress.length) {
          $scope.state.step += 1;
          return animatingProgress();
        }
      }
    };

    var animatingProgressWithinLevel = function(level) {
      var initialDelay = 700;
      return $timeout(function() {
        var steps = level.creditsTo - level.creditsFrom;
        if (steps <= 0) {
          return;
        }
        var relativeGain = steps / level.maxCredits;
        var animationTime = 500 + 1000 * relativeGain;
        var delay = 80;
        var partialSteps = Math.round(animationTime / delay);
        var partialStepSize = steps / partialSteps;
        var partialStep = 1;
        var promise = $interval(function() {
          level.partialCredits = level.creditsFrom + partialStep * partialStepSize;
          level.credits = Math.round(level.partialCredits);
          partialStep += 1;
        }, delay, partialSteps).then(function() {
          // just in case there is some bad rounding
          level.credits = level.creditsTo;
        });
        return promise;
      }, initialDelay);
    };
    if ($scope.evaluation.progress.length > 0) {
      animatingProgress();
    }
  });
});

