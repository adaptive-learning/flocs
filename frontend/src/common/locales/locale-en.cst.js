/**
 * English localization
 */
angular.module('flocs.locales')
.constant('localeEn', {
  ABOUT: 'About',
  BLOCKS: 'Blocks',
  CLOSE: 'Close',
  EASIER_TASK: 'Easier task',
  ERROR_404: "This page doesn't exist.",
  FEEDBACK: 'Feedback',
  KEYS: 'Keys',
  LEARN_PROGRAMMING: 'Learn programming!',
  LOG_IN: 'Log in',
  LOG_OUT: 'Log out',
  PASSWORD: 'Password',
  PASSWORD_AGAIN: 'Password again',
  RUN_PROGRAM: 'Run program',
  SEND: 'Send',
  SIGN_UP: 'Sign up',
  SPEED: 'Speed',
  TITLE: 'Adaptive programming',
  TOGGLE_NAVIGATION: 'Toggle navigation',
  USERNAME:  'Username',
  PROFILE: 'Profile',
  PROFILE_PAGE: {
    USERPROFILE: 'User profile',
    EMAIL: 'Email',
    SOLVED_TASKS_COUNT: 'Number of solved tasks',
    SOLVED_DISTINCT_TASKS_COUNT: 'Of which distinct',
    LOGGED_USER_NEEDED: 'In order to make this page function properly you must first log in.'
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

  TASK_COMPLETION: {
    TASK_SOLVED: 'Task solved!',
    CREDITS_INFO: 'You have earned {CREDITS, plural, one{1 credit} other{# credits} }.',
    FLOW_QUESTION: 'How difficult was the task for you?',
    EASY: 'Too Easy',
    RIGHT: 'Just Right',
    DIFFICULT: 'Too Difficult'
  },

});
