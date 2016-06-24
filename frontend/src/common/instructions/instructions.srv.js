// @ngInject
angular.module('flocs.instructions')
.service('instructionsService', function ($q, $timeout, workspaceService) {

  var instructions = {};
  var instructionsToShow = [];
  var instructionAreas = {};

  this.blockInstructionsPlacements = [];

  this.setInstructions = function(allInstructions, newInstructions) {
    // fake for now, TODO: implement
    instructions = {
      "ENV_RUN_RESET": {
        concept: "ENV_RUN_RESET",
        priority: 300,
        text: "Jakmile jsi spokojený se svým programem, spusť ho pomocí tohoto tlačítka. Pokud robot nedorazí k truhle, můžeš ho vrátit na původní pozici stisknutím 'Reset' tlačítka a zkusit jiný program.",
      },
      "ENV_MAZE": {
        concept: "ENV_MAZE",
        priority: 200,
        text: "Tady je bludiste...",
      },
      "ENV_WORKSPACE": {
        concept: "ENV_WORKSPACE",
        priority: 200,
        text: "Tady je workspace...",
      },
      "ENV_TOOLBOX": {
        concept: "ENV_TOOLBOX",
        priority: 200,
        text: "Tady je toolbox...",
      },
      "ENV_SNAPPING": {
        concept: "ENV_SNAPPING",
        priority: 200,
        text: "Takhle se snappuje...",
      },
      "BLOCK_MOVE": {
        concept: "BLOCK_MOVE",
        type: 'block',
        blockKey: 'maze_move_forward',
        priority: 200,
        text: "Tady je blok pohybu..",
      },
      "GAME_BLOCK_LIMIT": {
        concept: "GAME_BLOCK_LIMIT",
        priority: 200,
        text: "Tady je limit na bloky..",
      }
    };
    // pozor na poradi pushovani / pripadne popovat z druhe strany?
    //instructionsToShow.push("BLOCK_MOVE");
    //instructionsToShow.push("ENV_SNAPPING");
    //instructionsToShow.push("ENV_TOOLBOX");
    //instructionsToShow.push("ENV_WORKSPACE");
    //instructionsToShow.push("ENV_MAZE");
    instructionsToShow.push("GAME_BLOCK_LIMIT");
    //instructionsToShow.push("ENV_RUN_RESET");
    //console.log('instructions are set');

    // get blocks in toolbox (only for corresponding instructions)
    this.blockInstructionsPlacements.length = 0;
    var block = workspaceService.getBlockInToolbox('maze_move_forward');
    this.blockInstructionsPlacements.push({
      key: 'BLOCK_MOVE',
      offset: block.getOffset(),
      size: block.getSize(),
    });
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
        // TODO: try to remove $timeout...
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
