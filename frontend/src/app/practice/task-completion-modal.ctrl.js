/*
 * Controller for task completion modal
 */
angular.module('flocs.user')
.controller('taskCompletionModalCtrl', function($scope, $uibModalInstance,
      $uibModal, $timeout, $interval, practiceService, flowFactory) {

  $scope.reportFlow = function(flowKey) {
    // we try to convert the key to flow just to make sure the key corresponds
    // to an actual flow (to throw explicit error if the set of possible values
    // chagne)
    var flow = flowFactory.fromKey(flowKey);
    var report = {'flow': flow.key};
    $uibModalInstance.close(report);
  };

  $scope.evaluation = practiceService.attemptEvaluation;

  // fake some date, TODO: unfake....
  $scope.evaluation.time = 66;
  $scope.evaluation.percentil = 40;
  $scope.evaluation.speedBonus = true;
  $scope.evaluation.earnedCredits = 15;

  $scope.evaluation.progress = [
  {
    creditsFrom: 25,
    creditsTo: 30,
    maxCredits: 30,
    blocks: [{name: 'pokud-pak-jinak'}, {name: 'jiny super blok'}],
  },
  {
    creditsFrom: 0,
    creditsTo: 10,
    maxCredits: 30,
    blocks: [],
  },
  ];

  $scope.state = {
    step: 0,
    newBlocks: [],
  };

  angular.forEach($scope.evaluation.progress, function(level) {
    level.credits = level.creditsFrom;
  });

  var animatingProgress = function() {
    var step = $scope.state.step;
    var level = $scope.evaluation.progress[step];
    return animatingProgressWithinLevel(level).then(function() {
      return $timeout(levelup, 300).then(function() {
        return $timeout(nextStep, 2000);
      });
    });
    function levelup() {
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
    var initialDelay = 500;
    return $timeout(function() {
      var steps = level.creditsTo - level.creditsFrom;
      var relativeGain = steps / level.maxCredits;
      var animationTime = 500 + 1000 * relativeGain;
      var delay = Math.round(animationTime / steps);
      var promise = $interval(function() {
        level.credits++;
      }, delay, steps);
      return promise;
    }, initialDelay);
  };
  animatingProgress();
  //animatingProgressWithinLevel($scope.evaluation.progress[0]);
});

