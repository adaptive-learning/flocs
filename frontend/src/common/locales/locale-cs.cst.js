/**
 * Czech localization
 */
angular.module('flocs.locales')
.constant('localeCs', {
  ABOUT: 'O projektu',
  AUTHORS: 'Kdo za tím stojí',
  BLOCKS: 'Bloky',
  CLOSE: 'Zavřít',
  EASIER_TASK: 'Jednodušší úlohu',
  ERROR_404: "Tato stránka neexistuje.",
  FEEDBACK: 'Napiš nám',
  FREE_CREDITS: 'Neutracených kreditů',
  KEYS: 'Klíče',
  LEARN_PROGRAMMING: 'Nauč se programovat!',
  LOG_IN: 'Přihlásit se',
  LOG_OUT: 'Odhlásit se',
  PASSWORD: 'Heslo',
  PASSWORD_AGAIN: 'Heslo znovu',
  PRACTICE: 'Trénink',
  PRIVACY: 'Soukromí',
  PROFILE: 'Profil',
  RUN_PROGRAM: 'Spusť program',
  SEND: 'Odeslat',
  SIGN_UP: 'Registrovat se',
  SPEED: 'Rychlost',
  SUPPORT: 'Podpora',
  TITLE: 'Adaptabilní programování',
  TOGGLE_NAVIGATION: 'Přepnout navigaci',
  TOTAL_CREDITS: 'Kreditů celkem',
  USERNAME:  'Uživatelské jméno',

  ABOUT_PAGE: {
    INTRO_TEXT: 'Cílem projektu je, aby se každý mohl naučit programovat efektivně a zábavně.',
    AUTHORS_TEXT: 'Projekt vyvíjí <a href="http://www.fi.muni.cz/adaptivelearning/">Laboratoř adaptabilního učení</a>' +
                  ' na <a href="http://www.fi.muni.cz/">Fakultě informatiky Masarykovy univerzity</a>.' +
                  ' Mezi další projekty této skupiny patří:' +
                  '  <ul>' +
                  '    <li><a href="http://slepemapy.cz">Slepé mapy</a></li>' +
                  '    <li><a href="http://matmat.cz">MatMat</a></li>' +
                  '    <li><a href="http://umimecesky.cz">Umíme česky</a></li>' +
                  '    <li><a href="http://www.poznavackaprirody.cz/">Poznávačka přírody</a></li>' +
                  '    <li><a href="http://anatom.cz">Anatom</a></li>' +
                  '    <li><a href="http://www.autoskolachytre.cz/">Autoškola chytře</a></li>' +
                  '    <li><a href="http://tutor.fi.muni.cz">Problem Solving Tutor</a></li>' +
                  '  </ul>' +
                  ' Na vývoji aplikace se podílí Jaroslav Čechák, Tomáš Effenberger a Jiří Mauritz.' +
                  ' Náměty a připomínky můžete zasílat na' +
                  ' <a href="mailto:adaptive-programming@googlegroups.com">adaptive-programming@googlegroups.com</a>.',
    SUPPORT_TEXT: ' Za podporu při vývoji děkujeme' +
                  ' <a href="http://www.fi.muni.cz/">Fakultě informatiky</a>' +
                  ' a společnosti <a href="https://www.redhat.com">RedHat</a>.',
    PRIVACY_TEXT: ' Data z procesu učení využíváme pro určení obtížnosti jednotlivých úloh, pro výběr vhodných úloh a pro výzkumné účely.' +
                  ' Všechna tato data jsou zpracovávána anonymně. ' +
                  ' Přihlašovací údaje jsou použity pouze pro určení identity při opakovaných návštěvách, jinak se s nimi nepracuje.',
  },

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
    USERPROFILE: 'Uživatelský profil',
    EMAIL: 'E-mail',
    SOLVED_TASKS_COUNT: 'Počet vyřešených úloh',
    SOLVED_DISTINCT_TASKS_COUNT: 'Z toho unikátních úloh',
    LOGGED_USER_NEEDED: 'Pro správné fungování této stránky je potřeba se prihlásit.',
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
