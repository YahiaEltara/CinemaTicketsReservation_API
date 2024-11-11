from django.shortcuts import render
from django.http.response import JsonResponse
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated



# 1 without rest_framework and no model (FBV)
def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'name': 'John',
            'mobile': 12345
        },
        {
            'id': 2,
            'name': 'Alice',
            'mobile': 67890
        },
    ]
    return JsonResponse(guests, safe = False)


# 2 without rest_framework but with model (FBV)
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
# The .values() method turns the QuerySet into a set of dictionaries,
# where each dictionary represents a record with only the specified fields (name and mobile). 
    return JsonResponse(response)






# 3.0 with rest_framework and with model (FBV with api_view decorator)
@api_view(['GET', 'POST'])
def FBV_List(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3.1 with rest_framework and with model (FBV with api_view decorator)
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk (request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# 4.0 with rest_framework and with model (CBV with APIView)
class CBV_List(APIView):
    def get (self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many = True)
        return Response(serializer.data)
    
    def post (self, request):
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

# 4.1 with rest_framework and with model (CBV with APIView)
class CBV_pk(APIView):
    def get_object (self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get (self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    def put (self, request, pk):
        serializer = GuestSerializer(self.get_object(pk), data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete (self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# 5.0 with rest_framework and with model (CBV with Mixins & generics)
class Mixins_List(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get (self, request):
        return self.list(request)
    
    def post (self, request):
        return self.create(request)
    

# 5.1 with rest_framework and with model (CBV with Mixins & generics)
class Mixins_pk(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get (self, request, pk):
        return self.retrieve(request)
    
    def put (self, request, pk):
        return self.update(request)
    
    def delete (self, request, pk):
        return self.delete(request)






# 6.0 with rest_framework and with model (CBV with generics)
class Generic_ListCreate(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# 6.1 with rest_framework and with model (CBV with generics)
class Generic_pk(generics.RetrieveUpdateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]






# 7 with rest_framework and with model (CBV with ViewSets & routers)
class Viewset_Guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class Viewset_Movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie', 'hall']


class Viewset_Reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class =ReservationSerializer





# 8 --> some business logic
@api_view(['GET'])
def find_movies(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie']
    )
    serializer = MovieSerializer(movies, many = True)
    return Response(serializer.data)


@api_view(['POST'])
def create_reservations(request):
    movies = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie']
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    
    reservation = Reservation()
    reservation.movie = movies
    reservation.guest = guest 
    reservation.save()

    serializer = ReservationSerializer(reservation)

    return Response(serializer.data, status=status.HTTP_201_CREATED)



