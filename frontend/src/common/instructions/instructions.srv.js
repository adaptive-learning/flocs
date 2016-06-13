// @ngInject
angular.module('flocs.instructions')
.service('instructionsService', function ($q, $timeout) {

  var instructions = {};
  var instructionsToShow = [];
  var instructionAreas = {};


  this.setInstructions = function(allInstructions, newInstructions) {
    // fake for now, TODO: implement
    instructions = {
      "ENV_RUN_RESET": {
        concept: "ENV_RUN_RESET",
        priority: 300,
        text: "Jakmile jsi spokojený se svým programem, spusť ho pomocí tohoto tlačítka. Pokud robot nedorazí k truhle, můžeš ho vrátit na původní pozici stisknutím 'Reset' tlačítka a zkusit jiný program.",
      },
      "ENV_TOOLBOX": {
        concept: "ENV_TOOLBOX",
        priority: 200,
        text: "Zde je místo pro tvoje bloky. Pokud budeš šikovný, budeš dostávat během hry další bloky, které se objeví na tomto místě. Můžeš je v programu používat opakovaně.",
      }
    };
    // pozor na poradi pushovani / pripadne popovat z druhe strany?
    instructionsToShow.push("ENV_TOOLBOX");
    instructionsToShow.push("ENV_RUN_RESET");
    console.log('instructions are set');
  };

  this.registerInstructionArea = function(area) {
    var key = area.key;
    console.log('registered instruction-area for key:', key);
    instructionAreas[key] = area;
  };


  this.showingSelectedInstruction = function(key) {
    var instruction = instructions[key];
    if (!instruction) {
      throw(new Error('no instruction for key: ' + key));
    }
    var area = instructionAreas[key];
    if (!area) {
      throw(new Error('no registered instruction area for key: ' + key));
    }
    /*
    var instructionSeen = $q.defer();
    //console.log('showing instruction:', instruction);
    instruction.showing().then(function() {
      console.log('seen');
      instructionSeen.resolve();
    });
    return instructionSeen.promise;
    */
    return area.showing(instruction);
  };


  this.showingScheduledInstructions = function() {
    var scheduledInstructionsSeen = $q.defer();
    // the following line is necessary to access this function inside closure
    var showingSelectedInstruction = this.showingSelectedInstruction;

    var showNextInstructionIfAny = function() {
      if (instructionsToShow.length === 0) {
        $timeout(function() {
          scheduledInstructionsSeen.resolve();
        });
      } else {
        var instructionKey = instructionsToShow.pop();
        showingSelectedInstruction(instructionKey).then(showNextInstructionIfAny);
      }
    };

    showNextInstructionIfAny();
    return scheduledInstructionsSeen.promise;
  };
});
