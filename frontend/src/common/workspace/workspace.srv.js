/*
 * Workspace Service
 */
angular.module('flocs.workspace')
.factory('workspaceService', ['$log', 'blocklyService', 'toolboxService',
  function($log, blocklyService, toolboxService) {

  var blocklyDiv = null;
  // TODO: move default settings to a constant service?
  var settings = {
    toolbox: []
  };

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
      // TODO: create special service for initial settings
      toolbox: toolboxXml
    });

    // what dose clear() do? Is it necessary after inject?
    blocklyDiv.clear();
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
    // TODO...
    console.log('TODO:noHighlight');
  }

  /**
   * Return JavaScript representation of current code in the workspace
   */
  function getJavaScriptCode() {
    // TODO: make the highlight optional
    Blockly.JavaScript.STATEMENT_PREFIX = 'highlightBlock(%1);\n';
    Blockly.JavaScript.addReservedWords('highlightBlock');
    var code = Blockly.JavaScript.workspaceToCode(blocklyDiv);
    // trun on block highlighting
    blocklyDiv.traceOn(true);
    console.log(code);
    return code;
  }

  /**
   * Return Python representation of current code in the workspace
   */
  function getPythonCode() {
    var code = Blockly.Python.workspaceToCode(blocklyDiv);
    return code;
  }

  // initialization
  blocklyService.initializeBlockly();

  // public API
  return {
    setBlocklyDiv: setBlocklyDiv,
    set: set,
    reset: reset,
    highlightBlock: highlightBlock,
    noHighlight: noHighlight,
    getJavaScriptCode: getJavaScriptCode,
    getPythonCode: getPythonCode
  };
}]);
