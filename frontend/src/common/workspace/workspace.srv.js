/*
 * Workspace Service
 */
angular.module('flocs.workspace')
.factory('workspaceService', function($rootScope, $log, $timeout, blocklyService,
      toolboxService) {

  var blocklyDiv = null;
  // TODO: move default settings to a constant service?
  var settings = {
    toolbox: [],
    blocksLimit: null
  };
  var changeListeners = [];
  var startBlock = null;

  /**
   * Register new listener for changes
   */
  function addChangeListener(listener) {
    changeListeners.push(listener);
  }

  /**
   * Notify all change listeners about a change
   */
  function changeNotification() {
    angular.forEach(changeListeners, function(listener) {
      listener();
    });
  }

  /**
  * Register workspace view.
  * @param newWorkspace Api object of the view.
  */
  function setBlocklyDiv(newBlocklyDiv) {
    blocklyDiv = newBlocklyDiv;

    // in case that there is already available settings waiting to be set
    reset();
  }

  /**
  * Set new workspace settings.
  * @param settings Object with toolbox and other settings for workspace.
  */
  function set(newSettings) {
    //console.log('workspaceService:set');
    settings = newSettings;
    if (!settings.blocksLimit) {
      // make sure blocksLimit is not undefined
      settings.blocksLimit = null;
    }
    reset();
  }


  /**
  * Reset workspace the with current settings.
  */
  function reset() {
    //console.log('workspaceService:reset');

    // get rid of existing "workspace" (the actual displayed thing)
    if (blocklyDiv) {
      blocklyDiv.dispose();
    }

    // prepare toolbox
    var toolbox = toolboxService.prepareToolbox(settings.toolbox, settings.studentToolbox);
    var toolboxXml = toolboxService.toolboxToXml(toolbox);
    // inject blockly into the workspace with new toolbox
    blocklyDiv = Blockly.inject('blocklyDiv', {
      disable: true,
      toolbox: toolboxXml,
      maxBlocks: settings.blocksLimit || Infinity,
      trashcan: true
    });
    blocklyDiv.addChangeListener(handleBlocklyDivChange);

    // add start root block
    // Block.obtain call is depricated in newer versions of Blockly!
    //Blockly.BlockSvg.START_HAT = true;
    startBlock = Blockly.Block.obtain(blocklyDiv, 'start');
    startBlock.moveBy(10, 10);
    startBlock.initSvg();
    startBlock.render();
    startBlock.setDeletable(false);

    changeNotification();
    // NOTE: now we create (inject) new blockly div on reset, so there we do
    // not need to clear it (clear = set an empty program in workspace)
    //blocklyDiv.clear();

    // There seems to be a bug in Blockly - blocks are not disabled, so we will
    // need to disable them manually. But even if set as disabled, blocks are
    // reenabled after some events, e.g. user picking another block from
    // toolbox. So we also need to prevent these reenablings...
    // TODO: update to the new version of Blockly and remove this hack
    angular.forEach(toolbox, function(block) {
      if (block.disabled) {
        var blocklyBlock = getBlockInToolbox(block.identifier);
        blocklyBlock.setDisabled(true);
        blocklyBlock.setDisabled = function() {};
      }
    });
  }

  /**
   * Handle signals from blocklyDiv
   */
  function handleBlocklyDivChange() {
    // We need to call $apply after the notification to make views updated,
    // because the event is fired from non-angular component (Blockly).
    $rootScope.$apply(changeNotification);
  }

  /**
   * Return blocks limit or null if there is no limit.
   */
  function getBlocksLimit() {
    return settings.blocksLimit;
  }

  /**
   * Return number of currently used blocks.
   */
  function getBlocksUsed() {
    var blocksLeft = blocklyDiv.remainingCapacity();
    var blocksUsed = getBlocksLimit() - blocksLeft;
    return blocksUsed;
  }

  /**
   * Highlight block with given id
   */
  function highlightBlock(id) {
    blocklyDiv.highlightBlock(id);
  }

  /**
   * Hide current highlight
   */
  function noHighlight() {
    // TODO... if needed
    console.log('TODO:noHighlight');
  }

  /**
   * Return dump (XML text) of Blockly program in the current workspace
   */
  function getBlocklyCode() {
    //var xml_dom = Blockly.Xml.blockToDom_(startBlock);
    var xml_dom = Blockly.Xml.workspaceToDom(blocklyDiv);
    var xml_text = Blockly.Xml.domToText(xml_dom); // alt: domToPrettyText
    return xml_text;
  }

  /**
   * Return JavaScript representation of current code in the workspace
   */
  function getJavaScriptCode() {
    try {
      // TODO: make the highlight optional
      Blockly.JavaScript.STATEMENT_PREFIX = 'highlightBlock(%1);\n';
      Blockly.JavaScript.addReservedWords('highlightBlock');
      // initialize code generation (prepare variables etc.)
      Blockly.JavaScript.init(blocklyDiv);
      // get code from only those blocks that are connected to the start block
      var code = Blockly.JavaScript.blockToCode(startBlock);
      // add variable definitions if required
      code = Blockly.JavaScript.finish(code);
      // turn on block highlighting
      blocklyDiv.traceOn(true);
      //console.log(code);
      return code;
    } catch (err) {
      // TODO: do a proper exception handling and maybe inform the user
      $log.warn("Could not generate code from blocks. Some blocks might be missing an input.");
      $log.warn(err);
      return "";
    }
  }

  /**
   * Return Python representation of current code in the workspace
   */
  function getPythonCode() {
    var code = Blockly.Python.workspaceToCode(blocklyDiv);
    return code;
  }

  /**
   * Return first block with given key in current program in workspace
   */
  function getBlockInProgram(key) {
    var blocks = blocklyDiv.getAllBlocks();
    return findFirstBlockOfType(key, blocks);
  }

  /**
   * Return block in toolbox by key
   */
  function getBlockInToolbox(key) {
    // TODO: find blocks in toolbox using public attributes only
    var blocks = blocklyDiv.flyout_.workspace_.getAllBlocks();
    return findFirstBlockOfType(key, blocks);
  }

  function findFirstBlockOfType(type, blocks) {
    var block = null;
    for (var i=0; i <= blocks.length; i++) {
      if (blocks[i].type == type) {
        block = blocks[i];
        break;
      }
    }
    if (block !== null) {
      //var path = blocks[i].svgPath_;
      //var bbox = path.getBBox();

      // enrich block by functions for getting size and offset
      block.getSize = function() {
        var hw = block.getHeightWidth();
        // convert to POJO
        return {
          width: hw.width,
          height: hw.height,
        };
      };

      block.getOffset = function() {
        var blockly_xy = block.getRelativeToSurfaceXY();
        // convert to POJO
        var xy = {
          x: blockly_xy.x,
          y: blockly_xy.y,
        };
        // add offset caused by flyout
        if (!block.isInFlyout) {
          // TODO: factor out each access to Blockly private attributes to a
          // special service
          xy.x += blocklyDiv.flyout_.width_;
        }
        return xy;
      };

      return block;
    }
  }

  // initialization
  blocklyService.initializeBlockly();

  // public API
  return {
    setBlocklyDiv: setBlocklyDiv,
    set: set,
    reset: reset,
    addChangeListener: addChangeListener,
    highlightBlock: highlightBlock,
    noHighlight: noHighlight,
    getBlocklyCode: getBlocklyCode,
    getJavaScriptCode: getJavaScriptCode,
    getPythonCode: getPythonCode,
    getBlocksUsed: getBlocksUsed,
    getBlocksLimit: getBlocksLimit,
    getBlockInToolbox: getBlockInToolbox,
    getBlockInProgram: getBlockInProgram,
  };
});
