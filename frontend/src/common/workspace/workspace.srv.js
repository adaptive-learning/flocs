/*
 * Workspace Service
 */
angular.module('flocs.workspace')
.factory('workspaceService', ['$rootScope', '$log', 'blocklyService', 'toolboxService',
  function($rootScope, $log, blocklyService, toolboxService) {

  var blocklyDiv = null;
  // TODO: move default settings to a constant service?
  var settings = {
    toolbox: [],
    blocksLimit: null
  };
  var changeListeners = [];

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
    // make sure blocksLimit is not undefined
    settings.blocksLimit = settings.blocksLimit || null;
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

    console.log('max', settings.maxBlocks || Infinity);
    // inject blockly into the workspace with new toolbox
    blocklyDiv = Blockly.inject('blocklyDiv', {
      toolbox: toolboxXml,
      maxBlocks: settings.blocksLimit || Infinity,
      trashcan: true
    });

    blocklyDiv.addChangeListener(handleBlocklyDivChange);

    // what dose clear() do? Is it necessary after inject?
    blocklyDiv.clear();
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
    addChangeListener: addChangeListener,
    highlightBlock: highlightBlock,
    noHighlight: noHighlight,
    getJavaScriptCode: getJavaScriptCode,
    getPythonCode: getPythonCode,
    getBlocksUsed: getBlocksUsed,
    getBlocksLimit: getBlocksLimit
  };
}]);
