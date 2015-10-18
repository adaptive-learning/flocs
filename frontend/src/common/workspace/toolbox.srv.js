/*
 * Toolbox Service
 */
angular.module('flocs.workspace')
  .factory('toolboxService', [function() {

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
    if (blockNames.length === 0) {
        return; 
    }
    var xmlString = '';
    angular.forEach(blockNames, function(blockName) {
      if (typeof blockName === 'string' || blockName instanceof String) {
          xmlString += '<block type="' + blockName + '"></block>';
      } else {
          if (blockName.custom) {
            xmlString += '<category ' +
                'name="' + blockName.category + '" ' +
                'custom="' + blockName.custom + '">';
          } else {
            xmlString += '<category name="' + blockName.category + '">';
          }
          xmlString += blocksToXml(blockName.items);
          xmlString += '</category>';
      }
    });
    return xmlString;
  }

}]);



