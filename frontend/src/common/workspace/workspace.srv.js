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
    reset();
  }

  /**
  * Set new workspace settings.
  * @param settings Object with toolbox and other settings for workspace.
  */
  function set(newSettings) {
    console.log('workspaceService:set');
    settings = newSettings;
    reset();
  }


  /**
  * Reset workspace the with current settings.
  */
  function reset() {
    console.log('workspaceService:reset');
    if (!blocklyDiv) {
      return;
    }

    var toolboxXml = toolboxService.createToolboxXml(settings.toolbox);
    blocklyDiv.updateToolbox(toolboxXml);
  }

  /**
   * Highlight block with given id
   */
  function highlightBlock(id) {
    // TODO: fix highlight of block with given id (not working)
    console.log('highlighting block with id', id);
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
