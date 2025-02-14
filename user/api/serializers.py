from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegistrationSeralizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,)

    class Meta:
        model = User
        fields = ['username','email','password']


    def validate(self, data):

        password = data.get('password')

        if not password:
            raise serializers.ValidationError({"message":"Password is Missing."})

            
            
        return data
        
    def create(self, validated_data):

        password = validated_data.pop('password')
        

        user = User.objects.create(
            username= validated_data['username'],
            email= validated_data['email']                      
            )
        user.set_password(password)
        user.save()

        return user

class LoginSeralizer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only = True)


            

            
