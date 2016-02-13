"""
Service functions of practice session.
"""

import logging

from practice.models import StudentModel
from practice.models import PracticeSession

logger = logging.getLogger(__name__)


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
        logger.debug('Student id ', student.pk, ' has no current session, '
                     'creating new session id ', session.pk, ' .')
    else:
        # student is in active session, lets increase task counter
        session.task_counter += 1
        logger.debug(('Student id {student_id} with session id {session_id}'
                      ' getting next task with session number '
                      '{counter}.').format(student_id=student.pk, 
                         session_id=session.pk, counter=session.task_counter))
                     
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
