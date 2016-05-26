/**
 * Czech localization
 */
angular.module('flocs.locales')
.constant('localeCs', {
  ABOUT: 'O projektu',
  AUTHORS: 'Kdo za tím stojí',
  BLOCKS: 'Bloky',
  CLOSE: 'Zavřít',
  CONCEPTS: 'Koncepty',
  CONTINUE: 'Pokračovat',
  CREDITS: 'Kredity',
  ERROR_404: "Tato stránka neexistuje.",
  FEEDBACK: 'Napiš nám',
  FREE_CREDITS: 'Neutracených kreditů',
  GAINED_CREDITS: 'Získaných kreditů',
  GIVE_UP_TASK: 'Vzdát úlohu',
  KEYS: 'Klíče',
  LEARN_PROGRAMMING: 'Nauč se programovat!',
  LOG_IN: 'Přihlásit se',
  LOG_OUT: 'Odhlásit se',
  OVERALL_TIME: 'Celkový čas',
  PASSWORD: 'Heslo',
  PASSWORD_AGAIN: 'Heslo znovu',
  PRACTICE: 'Trénink',
  PRICE: 'cena',
  PRIVACY: 'Soukromí',
  PROFILE: 'Profil',
  RUN_PROGRAM: 'Spusť program',
  SEND: 'Odeslat',
  SESSION_OVERVIEW: 'Jak se dařilo?',
  SIGN_UP: 'Registrovat se',
  SPEED: 'Rychlost',
  SUPPORT: 'Podpora',
  TASK: 'Úkol',
  TASK_TITLE: 'Název úlohy',
  TIME_SPENT: 'Čas',
  TITLE: 'Adaptabilní programování',
  TOGGLE_NAVIGATION: 'Přepnout navigaci',
  TOTAL_CREDITS: 'Kreditů celkem',
  UNSUCCESSFUL: 'Nesplněno',
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

  CONCEPT: {
    PROGRAMMING_SEQUENCE: 'sekvence příkazů',
    PROGRAMMING_REPEAT: 'cyklus s daným počtem opakování',
    PROGRAMMING_WHILE: 'cyklus s podmínkou',
    PROGRAMMING_IF: 'podmíněné příkazy',
    PROGRAMMING_LOGIC: 'logické operátory',
  },

  FLOW: {
    FLOW: 'Flow',
    UNKNOWN: 'neznámé',
    VERY_DIFFICULT: 'velmi složité',
    DIFFICULT: 'složité',
    RIGHT: 'akorát',
    EASY: 'jednoduché',
  },

  HOME: {
    INTRO_TEXT: 'Toto je první prototyp aplikace pro adaptabilní výuku programování.' +
                ' Pomoz nám aplikaci vylepšit tím, že po vyzkoušení zodpovíš krátký ' +
                '<a href="https://docs.google.com/forms/d/1PUcvwcmdGU18fWUEvXbteuI4FnN_9KKebahHHRHwr7c/viewform">' +
                'dotazník</a>.',
  },

  PROFILE_PAGE: {
    AVAILABLE_BLOCKS: 'Dostupné bloky',
    EMAIL: 'E-mail',
    LOGGED_USER_NEEDED: 'Pro správné fungování této stránky je potřeba se prihlásit.',
    SOLVED_TASKS_COUNT: 'Počet vyřešených úloh',
    SOLVED_DISTINCT_TASKS_COUNT: 'Z toho unikátních úloh',
    USERPROFILE: 'Uživatelský profil',
  },

  STATISTICS_PAGE: {
    BLOCKS: 'Bloky',
    SOLVED_TASKS: 'Vyřešené úlohy',
    TITLE: 'Statistiky',
  },

  TASK_COMPLETION: {
    TASK_SOLVED: 'Úloha vyřešena!',
    CREDITS_INFO: 'Získal jsi {CREDITS, plural, one{1 kredit} few{# kredity} other{# kreditů} }.',
    SPEED_BONUS: 'bonus za rychlost',
    PURCHASED_BLOCKS: 'Nové bloky',
    FLOW_QUESTION: 'Jak těžká pro tebe úloha byla?',
    EASY: 'Lehká',
    RIGHT: 'Akorát',
    DIFFICULT: 'Těžká'
  },

});
