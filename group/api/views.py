from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import GroupSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from group.models import Group,Membership

import random
import string






class GroupViewSets(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):

        try:

            group_id =  ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            group_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            data = request.data.copy()

            data['group_id'] = group_id
            data['group_password'] = group_password


            group = Group.objects.create(
                name = data['name'],
                description = data['description'],
                group_id = group_id,
                group_password = group_password
            )
            
            Membership.objects.create(
                group = group,
                user = request.user,
                role = 'admin'
            )

            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods =['post'], permission_classes =[IsAuthenticated])
    def invite(self,request, pk=None):

        try:
            group = self.get_object()
            group_id = request.data.get('group_id')
            group_password = request.data.get('group_password')
            username = self.request.user

            if group_id != group.group_id:
                return Response({"message":"ID didn't match"}, status=status.HTTP_400_BAD_REQUEST)

            if group_password != group.group_password:
                return Response({"message":"Password didn't match"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.get(username = username)
            
            except User.DoesNotExist:
                return Response({"message":"User Doesnot Exist."}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                if Membership.objects.filter(group=group, user=user).exists():
                    return Response({"message":f"username {user.username} is already a member of this group."})
                else:
            
                    Membership.objects.create(
                        group = group,
                        user = user,
                        role = 'member'
                    )

                    return Response({"message":f"{user.username} added to the group."}, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response({"error": str(e)}, status= status.HTTP_400_BAD_REQUEST)
            
            
        except Exception as e:
                return Response({"error": str(e)}, status= status.HTTP_400_BAD_REQUEST)
            

        

        

        

    
    



        


