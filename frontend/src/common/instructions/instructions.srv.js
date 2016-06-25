// @ngInject
angular.module('flocs.instructions')
.service('instructionsService', function ($q, $timeout, workspaceService) {

  var self = this;  // necessary to access this service in different calling contexts
  var instructions = {};
  var instructionsToShow = [];
  var instructionAreas = {};

  self.instructionsPlacements = {};

  self.settingInstructions = function(allInstructions, newInstructions) {
    console.log('instructions:', newInstructions);
    var instructionsSet = $q.defer();
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
      "BLOCK_TURN": {
        concept: "BLOCK_TURN",
        type: 'block',
        blockKey: 'maze_turn',
        priority: 200,
        text: "Tady je blok pohybu..",
      },
      "GAME_BLOCK_LIMIT": {
        concept: "GAME_BLOCK_LIMIT",
        priority: 200,
        text: "Tady je limit na bloky..",
      },
      "GAME_COLORS": {
        concept: "GAME_COLORS",
        priority: 200,
        text: "Tady jsou barvy!",
      },
      "GAME_PITS": {
        concept: "GAME_PITS",
        priority: 200,
        text: "Tady jsou jamy!",
      },
      "GAME_TOKENS": {
        concept: "GAME_TOKENS",
        priority: 200,
        text: "Tady jsou tokeny!",
      }
    };

    // get blocks in toolbox (only for corresponding instructions)
    //self.blockInstructionsPlacements.length = 0;
    self.instructionsPlacements.blocks = [];
    var block = workspaceService.getBlockInToolbox('maze_move_forward');
    self.instructionsPlacements.blocks.push({
      key: 'BLOCK_MOVE',
      offset: block.getOffset(),
      size: block.getSize(),
    });
    block = workspaceService.getBlockInToolbox('maze_turn');
    self.instructionsPlacements.blocks.push({
      key: 'BLOCK_TURN',
      offset: block.getOffset(),
      size: block.getSize(),
    });
    // TODO: decomposition...
    var startBlock = workspaceService.getBlockInProgram('start');
    var startOffset = startBlock.getOffset();
    var startSize = startBlock.getSize();
    startOffset.y += 0.6 * startSize.height;
    startSize.width *= 0.3;
    startSize.height *= 0.8;
    self.instructionsPlacements.snapping = {
      offset: startOffset,
      size: startSize
    };

    // pozor na poradi pushovani / pripadne popovat z druhe strany?
    //instructionsToShow.push("ENV_SNAPPING");
    //instructionsToShow.push("BLOCK_MOVE");
    //instructionsToShow.push("BLOCK_TURN");
    instructionsToShow.push("ENV_TOOLBOX");
    instructionsToShow.push("ENV_WORKSPACE");
    //instructionsToShow.push("ENV_MAZE");
    //instructionsToShow.push("GAME_BLOCK_LIMIT");
    //instructionsToShow.push("ENV_RUN_RESET");
    //instructionsToShow.push("GAME_PITS");
    //instructionsToShow.push("GAME_TOKENS");
    //console.log('instructions are set');

    // just let the dynamic instruction areas to be rendered, then resolve
    $timeout(instructionsSet.resolve);

    return instructionsSet.promise;
  };

  self.registerInstructionArea = function(area) {
    var key = area.key;
    console.log('registered instruction-area for key:', key);
    instructionAreas[key] = area;
  };

  self.showingSelectedInstruction = function(key) {
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


  self.showingScheduledInstructions = function() {
    var scheduledInstructionsSeen = $q.defer();

    var showNextInstructionIfAny = function() {
      if (instructionsToShow.length === 0) {
        // TODO: try to remove $timeout...
        $timeout(function() {
          scheduledInstructionsSeen.resolve();
        });
      } else {
        var instructionKey = instructionsToShow.pop();
        self.showingSelectedInstruction(instructionKey)
            .then(showNextInstructionIfAny);
      }
    };

    showNextInstructionIfAny();
    return scheduledInstructionsSeen.promise;
  };
});
