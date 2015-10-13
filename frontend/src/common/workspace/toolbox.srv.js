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
   * Creates XML string describing the toolbox.
   *
   * @param blockNames {Array.<string>} List of block names.
   * @return {string} string of XML
   */
  function createToolboxXml(blockNames) {
    var xmlString = '<xml>';
    angular.forEach(blockNames, function(blockName) {
      xmlString += '<block type="' + blockName + '"></block>';
    });
    xmlString += '</xml>';
    return xmlString;
  }


}]);



