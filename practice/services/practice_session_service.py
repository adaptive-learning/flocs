"""
Service functions of practice session.
"""

import logging

from practice.models import StudentModel
from practice.models import PracticeSession

logger = logging.getLogger(__name__)

TASKS_IN_SESSION = 7


def next_task_in_session(student, taskInstance):
    """
    Move to next task in the session.
    Method increases task counter in the student's session.
    If the student has no current session, new is created and assigned to him.

    Args:
        session - must be active session
        taskInstance - new task to assign

    """
    # get or create session
    session = get_session(student)
    if session is None:
        session = create_session(taskInstance)
        logger.debug(('Session id {session_id}'
                      ' created for student {student}').format( 
                         session_id=session.pk, student=student))
    elif session.task_counter < TASKS_IN_SESSION:
        session.task_counter += 1
        session.last_task = taskInstance
        session.save()
        logger.debug(('Session id {session_id}'
                      ' proceed to the next task with session number '
                      '{counter}.').format( 
                         session_id=session.pk, counter=session.task_counter))
    else:
        # student finished last task of the session, creating new one
        session.active = False
        session.save()
        new_session = PracticeSession.objects.create(
                student=session.student,
                last_task=taskInstance)
        logger.debug('Student id ', session.student.pk, ' finished current session, '
                     'creating new session id ', new_session.pk, ' .')


def has_unresolved_task(student):
    """
    True if the student is in the middle of the session and has unresolved task.

    Returns:
        boolean
    """
    session = get_session(student)
    if get_active_task_instance(session) is None:
        return False
    else:
        return True


def get_active_task_instance(session):
    """
    Returns the last and non resolved task of the given session.
    If the session is None or is not active or the last task is solved, returns None.

    Returns:
        task instance
    """
    if session is None or session.active is None:
        return None
    if session.last_task.solved == True:
        return None
    return session.last_task


def get_session(student):
    """
    Retrieve session for the given student.
    If there is no such a session,  
    
    Returns:
        session
    """
    retrieved_sessions = PracticeSession.objects.filter(student=student, active=True)
    if len(retrieved_sessions) == 1:
        return retrieved_sessions[0]
    elif len(retrieved_sessions) == 0:
        # no session
        return None
    else:
        # illegal state
        raise ValueError('More active sessions for student ' + student.pk)


def create_session(taskInstance):
    """
    Creates session for specified task instance.
    If there is active session, it will close it first.

    Returns:
        new created session
    """
    # first close one, if exists
    # TODO: replace with session = get_session(taskInstance.student)
    student_model = StudentModel.objects.get(user=taskInstance.student)
    session = get_session(student_model)
    if session is not None:
        end_session(session)
    # create
    return PracticeSession.objects.create(student=student_model, last_task=taskInstance)


def end_session(session):
    """
    Ends session even if the student did not reach the session limit for tasks.
    """
    session.active = False
    session.save()
