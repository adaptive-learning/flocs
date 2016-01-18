/**
 * Convert language code to native language name, e.g. 'en' to 'English'
 */
angular.module('flocs.locales')

.filter('languageNativeName', function () {
  var NATIVE_NAME = {
    'cs': 'Česky',
    'en': 'English'
  };

  return function(languageCode) {
    return NATIVE_NAME[languageCode];
  };
});
