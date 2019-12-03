from rest_framework.response import Response 
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
import logging
from . import appsettings
from .serializers import NameSearchSerializer
from .services import searchujs

logger = logging.getLogger(__name__)

#class SearchName(APIView):
class SearchName(generics.CreateAPIView):

    queryset = []
    serializer_class = NameSearchSerializer
    permission_classes = appsettings.PERMISSION_CLASSES

    def post(self, request, *args, **kwargs):
        try:
            to_search = NameSearchSerializer(data=request.data)
            if to_search.is_valid():
                # search ujs portal for a name.
                # and return the results.
                results = searchujs.search_by_name(**to_search.validated_data)
                return Response({
                    "searchResults": results
                })
            else:
                return Response({
                    "errors": to_search.errors
                }, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({
                "errors": [str(ex)]
            })

