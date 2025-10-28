from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    name = request.data.get('name')
    password = request.data.get('password')

    if not email or not name or not password:
        return Response({"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response(
            {"message": "User with this email already exists. Please log in instead."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = UserSerializer(data={"email": email, "name": name, "password": password})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
