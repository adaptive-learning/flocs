"""
Feedback controllers
"""

from django.http import JsonResponse
from django.shortcuts import render
import json

from .services import process_feedback_message

def add_feedback_message(request):
    """Process new feedback message.

    POST params:
        text: string
        email: string

    Returns:
        success: bool
        error-message (if success is False): string
    """
    post_data = json.loads(request.body.decode('utf-8'))
    text = post_data.get('text')
    email = post_data.get('email')

    process_feedback_message(
            text=text,
            email=email,
            user_id=request.user.id
    )
    return JsonResponse({'success': True})
    #except Exception as exc:
    #    return JsonResponse({
    #        "success": False,
    #        "message": "Invalid message!"
    #    })
