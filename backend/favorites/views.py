from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from users.models import Listing
from users.models import User
from datetime import datetime
from users.utils import get_current_user  

@api_view(['POST', 'DELETE'])
def toggle_favorite(request, listing_id):
    current_user = get_current_user(request)
    print("Current User:", current_user)
    if not current_user:
        return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    if not listing_id or not ObjectId.is_valid(listing_id):
        return Response({"message": "Invalid listing ID"}, status=status.HTTP_400_BAD_REQUEST)

    listing = Listing.objects(id=listing_id).first()
    if not listing:
        return Response({"message": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)

    # Ensure favoriteIds exists
    if not hasattr(current_user, "favoriteIds"):
        current_user.favoriteIds = []

    if request.method == 'POST':
        # Add to favorites
        if listing not in current_user.favoriteIds:
            current_user.favoriteIds.append(listing)
            current_user.save()
            return Response({"message": "Added to favorites"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already in favorites"}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # Remove from favorites
        if listing in current_user.favoriteIds:
            current_user.favoriteIds.remove(listing)
            current_user.save()
            return Response({"message": "Removed from favorites"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not found in favorites"}, status=status.HTTP_404_NOT_FOUND)
