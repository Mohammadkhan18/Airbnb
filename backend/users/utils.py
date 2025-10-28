
from .models import User

def get_current_user(request):
    print("HEADERS:", request.headers)
    user_id = request.headers.get("X-User-Id")
    print("USER_ID:", user_id)
    if not user_id:
        return None
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None