"""
Service functions of practice session.
"""

import logging

from practice.models import StudentModel
from practice.models import PracticeSession
from practice.models import SessionTaskInstance

logger = logging.getLogger(__name__)

TASKS_IN_SESSION = 7


def next_task_in_session(student, task_instance):
    """
    Move to next task in the session.
    Method increases task counter in the student's session.
    If the student has no current session, new is created and assigned to him.

    Args:
        session - must be active session
        task_instance - new task to assign

    """
    # get or create session
    session = get_session(student)

    # TODO: sessions should be (if possible) finished earlier (after the
    # processing of the results from the last task in the session)
    if session and session.task_counter >= TASKS_IN_SESSION:
        session.active = False
        session.save()
        logger.debug('Student id ', session.student.pk, ' finished current session.')
        session = None

    if session is None:
        session = create_session(task_instance)
        logger.debug(('Session id {session_id}'
                      ' created for student {student}').format(
                         session_id=session.pk, student=student))
    else:
        add_task_instance_to_session(task_instance, session)


def add_task_instance_to_session(task_instance, session):
    session.task_counter += 1
    session.last_task = task_instance
    session.save()
    SessionTaskInstance.objects.create(session=session, order=session.task_counter,
            task_instance=task_instance)
    logger.debug('Session {session_pk} proceed to the {counter}. task instance.'
                .format(session_pk=session.pk, counter=session.task_counter))


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
    if session.last_task.is_completed():
        return None
    return session.last_task


def get_all_task_instances(session):
    """
    Return list of task instances in this session in order they were taken
    by the student.
    """
    return session.get_task_instances()


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


def create_session(task_instance):
    """
    Creates session for specified task instance.
    If there is active session, it will close it first.

    Returns:
        new created session
    """
    # first close one, if exists
    # TODO: replace with session = get_session(task_instance.student)
    student = task_instance.student
    old_session = get_session(student)
    if old_session is not None:
        end_session(old_session)
    # create new session
    session = PracticeSession.objects.create(student=student, last_task=task_instance)
    SessionTaskInstance.objects.create(session=session, order=session.task_counter,
            task_instance=task_instance)
    return session


def end_session(session):
    """
    Ends session even if the student did not reach the session limit for tasks.
    """
    session.active = False
    session.save()
