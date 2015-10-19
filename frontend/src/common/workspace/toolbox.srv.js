/*
 * Toolbox Service
 */
angular.module('flocs.workspace')
  .factory('toolboxService', ['blocks', function(blocks) {

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
    return '<xml>' + blocksToXml(blockNames) + '</xml>';
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
}]);



