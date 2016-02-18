/**
 * Czech localization
 */
angular.module('flocs.locales')
.constant('localeCs', {
  ABOUT: 'O projektu',
  BLOCKS: 'Bloky',
  CLOSE: 'Zavřít',
  EASIER_TASK: 'Jednodušší úlohu',
  ERROR_404: "Tato stránka neexistuje.",
  FEEDBACK: 'Napiš nám',
  KEYS: 'Klíče',
  LEARN_PROGRAMMING: 'Nauč se programovat!',
  LOG_IN: 'Přihlásit se',
  LOG_OUT: 'Odhlásit se',
  PASSWORD: 'Heslo',
  PASSWORD_AGAIN: 'Heslo znovu',
  RUN_PROGRAM: 'Spusť program',
  SEND: 'Odeslat',
  SIGN_UP: 'Registrovat se',
  SPEED: 'Rychlost',
  TITLE: 'Adaptabilní programování',
  TOGGLE_NAVIGATION: 'Přepnout navigaci',
  USERNAME:  'Uživatelské jméno',
  PROFILE: 'Profil',

  FEEDBACK_MODAL: {
    MESSAGE_FIELD: 'Zpráva:',
    EMAIL_FIELD: 'E-mail (nepovinné):',
    SUCCESS_MESSAGE: 'Zpráva přijata, děkujeme!',
    INVALID_MESSAGE: 'Neplatná zpráva!',
  },

  HOME: {
    INTRO_TEXT: 'Toto je první prototyp aplikace pro adaptabilní výuku programování.' +
                ' Pomoz nám aplikaci vylepšit tím, že po vyzkoušení zodpovíš krátký ' +
                '<a href="https://docs.google.com/forms/d/1PUcvwcmdGU18fWUEvXbteuI4FnN_9KKebahHHRHwr7c/viewform">' +
                'dotazník</a>.',
  },

  PROFILE_PAGE: {
    USERPROFILE: 'Uživateslký profil',
    EMAIL: 'E-mail',
    SOLVED_TASKS_COUNT: 'Počet vyřešených úloh',
    SOLVED_DISTINCT_TASKS_COUNT: 'Z toho unikátních úloh',
    LOGGED_USER_NEEDED: 'Pro správné fungování této stránky je potřeba se prihlásit.',
    TOTAL_CREDITS: 'Kreditů celkem',
    FREE_CREDITS: 'Neutracených kreditů',
  },

  TASK_COMPLETION: {
    TASK_SOLVED: 'Úloha vyřešena!',
    CREDITS_INFO: 'Získal jsi {CREDITS, plural, one{1 kredit} few{# kredity} other{# kreditů} }.',
    FLOW_QUESTION: 'Jak těžká pro tebe úloha byla?',
    EASY: 'Lehká',
    RIGHT: 'Akorát',
    DIFFICULT: 'Těžká'
  },

});
