from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import Listing
from users.utils import get_current_user
from bson import ObjectId
from datetime import datetime

# -------------------------
# Create Listing
# -------------------------
@api_view(['POST'])
def create_listing(request):
    print("Incoming request data:", request.data)
    current_user = get_current_user(request)
    print("Current user:", current_user)
    if not current_user:
        return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data.copy()  # make a mutable copy

    # Extract locationValue if it's inside "location"
    if "location" in data and isinstance(data["location"], dict):
        data["locationValue"] = data["location"].get("value")

    required_fields = [
        "title", "description", "imageSrc", "category",
        "roomCount", "bathroomCount", "guestCount", "locationValue", "price"
    ]

    for field in required_fields:
        if not data.get(field):
            return Response({"message": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    listing = Listing(
        userId=current_user.id,
        title=data["title"],
        description=data["description"],
        imageSrc=data["imageSrc"],
        category=data["category"],
        roomCount=int(data["roomCount"]),
        bathroomCount=int(data["bathroomCount"]),
        guestCount=int(data["guestCount"]),
        locationValue=data["locationValue"],
        price=int(data["price"]),
        createdAt=datetime.utcnow()
    )
    listing.save()

    return Response({
        "id": str(listing.id),
        "userId": str(listing.userId),
        "title": listing.title,
        "description": listing.description,
        "imageSrc": listing.imageSrc,
        "category": listing.category,
        "roomCount": listing.roomCount,
        "bathroomCount": listing.bathroomCount,
        "guestCount": listing.guestCount,
        "locationValue": listing.locationValue,
        "price": listing.price,
        "createdAt": listing.createdAt
    }, status=status.HTTP_201_CREATED)


# -------------------------
# Delete Listing
# -------------------------
@api_view(['DELETE'])
def delete_listing(request, listing_id):
    current_user = get_current_user(request)
    if not current_user:
        return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    if not listing_id or not ObjectId.is_valid(listing_id):
        return Response({"message": "Invalid listing ID"}, status=status.HTTP_400_BAD_REQUEST)

    listing = Listing.objects(id=listing_id, userId=current_user.id).first()
    if not listing:
        return Response({"message": "Listing not found or you don't have permission"}, status=status.HTTP_404_NOT_FOUND)

    listing.delete()
    return Response({"message": "Listing deleted successfully"}, status=status.HTTP_200_OK)
