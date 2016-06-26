/*
 * Toolbox Service
 */
angular.module('flocs.workspace')
.factory('toolboxService', function(blocksXml, blocksOrder) {

  var blocksOrderMap = null;

  // public API
  return {
    prepareToolbox: prepareToolbox,
    toolboxToXml: toolboxToXml
  };

  /**
   * Creates a single toolbox combining task and student toolbox, sorting all
   * blocks and expanding them, if there is enough space.
   */
  function prepareToolbox(taskToolbox, studentToolbox) {
    var toolbox =  mergeTaskAndStudentToolbox(taskToolbox, studentToolbox);
    return sortToolbox(expandToolbox(toolbox));
  }

  /**
   * Creates a single toolbox combining task and student toolbox.
   * The current behavior is to mark all blocks in student toolbox, which are
   * not in task toolbox as disabled.
   */
  function mergeTaskAndStudentToolbox(taskToolbox, studentToolbox) {
    var toolbox = taskToolbox.slice();
    angular.forEach(studentToolbox, function(block) {
      var alreadyIncluded = false;
      for (var i=0; i<taskToolbox.length; i++) {
        if (block.identifier == taskToolbox[i].identifier) {
          alreadyIncluded = true;
          break;
        }
      }
      if (!alreadyIncluded) {
        block.disabled = true;
        toolbox.push(block);
      }
    });
    return toolbox;
  }

  function expandToolbox(toolbox) {
    var MAX_BLOCKS = 9;
    var expandedToolbox = [];
    for (var i=0; i<toolbox.length; i++) {
      var identifiersExpanded = toolbox[i]['identifiers-expanded'];
      var remainingBlocks = toolbox.length - i - 1;
      var expandedLength = expandedToolbox.length + identifiersExpanded.length + remainingBlocks;
      if (toolbox[i].disabled || expandedLength > MAX_BLOCKS) {
        expandedToolbox.push(toolbox[i]);
      } else {
        for (var j=0; j<identifiersExpanded.length; j++) {
          var newBlock = angular.copy(toolbox[i]);
          newBlock.identifier = identifiersExpanded[j];
          expandedToolbox.push(newBlock);
        }
      }
    }
    return expandedToolbox;
  }

  function sortToolbox(toolbox) {
    var sortedToolbox =  toolbox.sort(function(a, b) {
      return blockComparator(a.identifier, b.identifier);
    });
    return sortedToolbox;
  }


  /**
   * Convert toolbox represented as a string of block objects into a string
   * describing the toolbox in XML.
   */
  function toolboxToXml(toolbox) {
    // TODO: unhack work with XML -- according to Blockly docs, it should be
    // possible to work just with XML nodes, no need to convert it to text
    var xmlLines = ['<xml>'];
    angular.forEach(toolbox, function(block) {
      var key = block.identifier;
      var line = blocksXml[key];
      if (!line) {
        // if not custom block, then it should be Blockly default block
        line = '<block type="' + key + '"></block>';
      }
      if (block.disabled) {
        // hack to mark disabled blocks
        line = line.replace('<block', '<block editable="false" disabled="true"');
      }
      xmlLines.push(line);
    });
    xmlLines.push('</xml>');
    var xmlString = xmlLines.join('\n');
    return xmlString;
  }


  /*
   * Coparator for comparing two blocks
   *
   * @param a block to compare
   * @param b block to compare
   */
  function blockComparator(a,b) {
    // prepare block ordering map if it does not already exist
    if (blocksOrderMap === null) {
      buildOrderMap();
    }

    // list items are strings
    if ((typeof a === 'string' || a instanceof String) &&
            (typeof b === 'string' || b instanceof String)) {
        // get ordinal values for blocks
        var orderA = blocksOrderMap[a];
        var orderB = blocksOrderMap[b];

        // compaer ordinal values
        if (orderA !== null && orderB !== null) {
            return orderA >= orderB;
        } else {
            return a >= b;
        }
    // Compare user defined category with predefined category. That is an
    // undefined operation.
    } else {
        return 1;
    }
  }

  /*
   * Helper function for building object from list
   */
  function buildOrderMap() {
    blocksOrderMap = {};
    // every item from list becomes object's attribute
    for (var i = 0; i < blocksOrder.length; i++) {
      blocksOrderMap[blocksOrder[i]] = i;
    }
  }
});
