"""
Service functions of practice session.
"""

import logging

from practice.models import StudentModel
from practice.models import PracticeSession

logger = logging.getLogger(__name__)

TASKS_IN_SESSION = 7


def next_task_in_session(student):
    """
    Move to next task in the session.
    Method increases task counter in the student's session.
    If the student has no current session, new is created and assigned to him.

    """
    session = student.session
    if session == None:
        # student has no current session, lets create new one
        session = PracticeSession.objects.create()
        student.session = session
        student.save()
        logger.debug('Student id ', student.pk, ' has no current session, '
                     'creating new session id ', session.pk, ' .')
    elif session.task_counter < TASKS_IN_SESSION:
        # student is in active session, lets increase task counter
        session.task_counter += 1
        session.save()
        logger.debug(('Student id {student_id} with session id {session_id}'
                      ' getting next task with session number '
                      '{counter}.').format(student_id=student.pk, 
                         session_id=session.pk, counter=session.task_counter))
    else:
        # student finished last task of the session, creating new one
        new_session = PracticeSession.objects.create()
        student.session = new_session
        student.save()
        logger.debug('Student id ', student.pk, ' finished current session, '
                     'creating new session id ', new_session.pk, ' .')
                     
def get_task_in_session(student):
    """
    Returns task counter for a student.
    The number represents a count of solved tasks in the session 
    plus the current one.
    """
    session = student.session
    if session == None:
        return 0
    else:
        return session.task_counter

def end_session(student):
    """
    Ends session even if the student did not reach the session limit for tasks.
    """
    student.session = None
    student.save()
