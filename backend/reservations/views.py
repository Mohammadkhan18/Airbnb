from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from datetime import datetime

from users.utils import get_current_user
from users.models import Reservation, Listing


# -------------------------
# Create Reservation
# -------------------------
@api_view(['POST'])
def create_reservation(request):
    current_user = get_current_user(request)
    if not current_user:
        return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    required_fields = ["listingId", "startDate", "endDate", "totalPrice"]

    for field in required_fields:
        if not data.get(field):
            return Response({"message": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate listing ID
    listing_id = data["listingId"]
    if not ObjectId.is_valid(listing_id):
        return Response({"message": "Invalid listingId"}, status=status.HTTP_400_BAD_REQUEST)

    listing = Listing.objects(id=listing_id).first()
    if not listing:
        return Response({"message": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)

    # Parse dates (string → datetime)
    try:
        start_date = datetime.fromisoformat(data["startDate"].replace("Z", "+00:00"))
        end_date = datetime.fromisoformat(data["endDate"].replace("Z", "+00:00"))
    except Exception:
        return Response({"message": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

    # Create reservation
    reservation = Reservation(
        userId=current_user,
        listingId=listing,
        startDate=start_date,
        endDate=end_date,
        totalPrice=int(data["totalPrice"]),
        createdAt=datetime.utcnow(),
    )
    reservation.save()

    return Response({
        "id": str(reservation.id),
        "userId": str(reservation.userId.id),
        "listingId": str(reservation.listingId),
        "startDate": reservation.startDate.isoformat(),
        "endDate": reservation.endDate.isoformat(),
        "totalPrice": reservation.totalPrice,
        "createdAt": reservation.createdAt.isoformat()
    }, status=status.HTTP_201_CREATED)


# -------------------------
# Delete Reservation
# -------------------------
@api_view(['DELETE'])
def delete_reservation(request, reservation_id):
    current_user = get_current_user(request)
    if not current_user:
        return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    if not reservation_id or not ObjectId.is_valid(reservation_id):
        return Response({"message": "Invalid reservation ID"}, status=status.HTTP_400_BAD_REQUEST)

    reservation = Reservation.objects(id=reservation_id).first()
    if not reservation:
        return Response({"message": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)

    if (
        str(reservation.userId.id) != str(current_user.id)
        and str(reservation.listingId.userId.id) != str(current_user.id)
    ):
        return Response({"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    reservation.delete()
    return Response({"message": "Reservation deleted successfully"}, status=status.HTTP_200_OK)
