/**
 * English localization
 */
angular.module('flocs.locales')
.constant('localeEn', {
  ABOUT: 'About',
  AUTHORS: 'About Authors',
  BLOCKS: 'Blocks',
  CLOSE: 'Close',
  CONTINUE: 'Continue',
  EASIER_TASK: 'Easier task',
  ERROR_404: "This page doesn't exist.",
  FEEDBACK: 'Feedback',
  FREE_CREDITS: 'Credits to spend',
  KEYS: 'Keys',
  LEARN_PROGRAMMING: 'Learn programming!',
  LOG_IN: 'Log in',
  LOG_OUT: 'Log out',
  PASSWORD: 'Password',
  PASSWORD_AGAIN: 'Password again',
  PRACTICE: 'Practice',
  PRIVACY: 'Privacy',
  PROFILE: 'Profile',
  RUN_PROGRAM: 'Run program',
  SEND: 'Send',
  SESSION_OVERVIEW: 'How did it go?',
  SIGN_UP: 'Sign up',
  SPEED: 'Speed',
  SUCCESSFUL: 'Successful',
  SUPPORT: 'Support',
  TASK: 'Task',
  TITLE: 'Adaptive programming',
  TOGGLE_NAVIGATION: 'Toggle navigation',
  TOTAL_CREDITS: 'Total credits',
  USERNAME:  'Username',
  UNSUCCESSFUL: 'Unsuccessful',

  ABOUT_PAGE: {
    INTRO_TEXT: 'The goal of the project is efficient and entertaining learning of programming for everybody.',
    AUTHORS_TEXT: 'Project is developed by <a href="http://www.fi.muni.cz/adaptivelearning/">Adaptive Learning research group</a>' +
                  ' at <a href="http://www.fi.muni.cz/">Faculty of Informatics, Masaryk University</a>.' +
                  ' Other projects by this group include:' +
                  '  <ul>' +
                  '    <li><a href="http://outlinemaps.org/">Outline Maps</a></li>' +
                  '    <li><a href="https://practiceanatomy.com/">Practice Anatomy</a></li>' +
                  '    <li><a href="http://tutor.fi.muni.cz/index.php?&changelang=en">Problem Solving Tutor</a></li>' +
                  '  </ul>' +
                  ' The application is developed by Jaroslav Čechák, Tomáš Effenberger and Jiří Mauritz.' +
                  ' You can send suggestions and issues to' +
                  ' <a href="mailto:adaptive-programming@googlegroups.com">adaptive-programming@googlegroups.com</a>.',
    SUPPORT_TEXT: ' We would like to thank ' +
                  ' <a href="http://www.fi.muni.cz/">Fakulty of Informatics, Masaryk University</a>' +
                  ' and <a href="https://www.redhat.com">RedHat</a>' +
                  ' for the support.',
    PRIVACY_TEXT: ' We use data from the learning process to determine difficulty of tasks, to select appropriate tasks and for research purposes.' +
                  ' All the data is processed anonymously. ' +
                  ' Login data is only used to determine identity during repeated visits, otherwise we do not work with it.'
  },

  FEEDBACK_MODAL: {
    MESSAGE_FIELD: 'Message:',
    EMAIL_FIELD: 'Your email address (optional):',
    SUCCESS_MESSAGE: 'Feedback received, thank you!',
    INVALID_MESSAGE: 'Invalid message!',
  },

  HOME: {
    INTRO_TEXT: 'This is a first prototype of application for adaptive learning of programming.',
  },

  PROFILE_PAGE: {
    AVAILABLE_BLOCKS: 'Available blocks',
    EMAIL: 'Email',
    LOGGED_USER_NEEDED: 'In order to make this page function properly you must first log in.',
    SOLVED_TASKS_COUNT: 'Number of solved tasks',
    SOLVED_DISTINCT_TASKS_COUNT: 'Of which distinct',
    USERPROFILE: 'User profile',
  },

  TASK_COMPLETION: {
    TASK_SOLVED: 'Task solved!',
    CREDITS_INFO: 'You have earned {CREDITS, plural, one{1 credit} other{# credits} }.',
    FLOW_QUESTION: 'How difficult was the task for you?',
    EASY: 'Too Easy',
    RIGHT: 'Just Right',
    DIFFICULT: 'Too Difficult'
  },

});
