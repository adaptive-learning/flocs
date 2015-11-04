/*
 * Toolbox Service
 */
angular.module('flocs.workspace')
  .factory('toolboxService', ['blocks', 'blocksOrder', function(blocks, blocksOrder) {

  var blocksOrderMap = null;

  // public API
  return {
    createToolboxXml: createToolboxXml
  };

  /**
   * Encapsulates recursively generated toolbox XML in root <xml> element.
   *
   * @param blockNames {Array.<Object>} List of block names and categories.
   * @return {string} string of XML
   */
  function createToolboxXml(blockNames) {
    // generate toolbox from sorted list
    return '<xml>' + blocksToXml(blockNames.sort(blockComparator)) + '</xml>';
  }

  /**
   * Creates XML string describing the toolbox.
   *
   * @param blockNames {Array.<Object>} List of block names and categories.
   * @return {string} string of XML without root element
   */
  function blocksToXml(blockNames) {
    // no more blocks to process
    if (typeof blockNames === 'undefined' || blockNames.length === 0) {
        return; 
    }

    var xmlString = '';

    angular.forEach(blockNames, function(blockName) {
        // is blockName a string (block or category name)
        if (typeof blockName === 'string' || blockName instanceof String) {
            // is it custom defined block/category
            if (blocks[blockName]) {
                // custom defined block/category identifier
                xmlString += blocks[blockName];
            } else {
                // the it better be an exact name of block
                xmlString += '<block type="' + blockName + '"></block>';
            }

        // blockName is a definiton of category
        } else {
            // does it contain attribute custom
            if (blockName.custom) {
                xmlString += '<category ' +
                    'name="' + blockName.category + '" ' +
                    'custom="' + blockName.custom + '">';
            } else {
                xmlString += '<category name="' + blockName.category + '">';
            }
            // process all category's items
            xmlString += blocksToXml(blockName.items);
            xmlString += '</category>';
        }
    });
    //console.log(xmlString);
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
}]);



