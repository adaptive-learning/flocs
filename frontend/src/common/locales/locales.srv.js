/**
 * Localization service
 */
angular.module('flocs.locales')
.factory('localesService', function($translate, blocklyMessages) {
  var API = {
    setLanguage: setLanguage,
    getLanguage: getLanguage,
    setLanguageDomains: setLanguageDomains,
    getLanguageDomains: getLanguageDomains,
  };

  var _domains = {};

  function setLanguage(languageCode) {
    $translate.use(languageCode);
    Blockly.Msg = blocklyMessages[languageCode];
  }

  function getLanguage() {
    return $translate.use();
  }

  function setLanguageDomains(domains) {
    _domains = domains;
  }

  function getLanguageDomains() {
    return _domains;
  }

  return API;
});
