"""
Listings app views.
"""
from rest_framework.views import APIView
from rest_framework.response import Response


class ListingListView(APIView):
    """
    Listing list view.
    """
    
    def get(self, request):
        return Response({
            'message': 'Listings endpoint accessed successfully',
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'path': request.path,
            'method': request.method
        })
