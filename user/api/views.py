from .serializers import UserRegistrationSeralizer, LoginSeralizer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny



class UserRegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSeralizer
    permission_classes = [AllowAny]

   
    
class UserLoginView(APIView):

    def post(self, request):

        data = request.data
        serializer = LoginSeralizer(data = data)

        if serializer.is_valid():

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            print(f"{username} and {password} is this")
            if user is not None:

                refresh = RefreshToken.for_user(user)
                return Response({

                    'refresh' : str(refresh),
                    'access' : str(refresh.access_token),

                 }, status= status.HTTP_200_OK)
            return Response({"message":"Invalid Credentials"}, status= status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    
        
