from practice.models import StudentModel


def get_practice_details(user):
    details_dict = {}
    student = StudentModel.objects.get_or_create(user_id=user.pk)[0]
    details_dict['total-credits'] = student.total_credits
    details_dict['free-credits'] = student.free_credits
    return details_dict
