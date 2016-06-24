/*
 * Workspace Service
 */
angular.module('flocs.workspace')
.factory('workspaceService', function($rootScope, $log, blocklyService,
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
    //console.log("settings.toolbox is " + settings.toolbox);
    var toolboxXml = toolboxService.createToolboxXml(settings.toolbox);

    // inject blockly into the workspace with new toolbox
    blocklyDiv = Blockly.inject('blocklyDiv', {
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

  function getBlockInToolbox(key) {
    // TODO: find blocks in toolbox using public attributes only
    var blocks = blocklyDiv.flyout_.workspace_.getAllBlocks();
    var block = null;
    for (var i=0; i <= blocks.length; i++) {
      if (blocks[i].type == key) {
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
        var xy = block.getRelativeToSurfaceXY();
        // convert to POJO
        return {
          x: xy.x,
          y: xy.y,
        };
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
  };
});
