from rest_framework import serializers
from .models import *

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name',
                  'description',
                  'owner',
                  'visibility',
                  'members']

class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id',
                  'name',
                  'description',
                  'visibility',
                  'members']


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'role', 'join_date']
        read_only_fields = False



class ProjectMemberIdsSerializer(serializers.Serializer):

    MAX_USER = 100

    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),
                                               many=True,
                                               allow_empty=False)

    def validate_user(self, users):
        users = list({u.pk: u for u in users}.value())
        if len(users)> self.MAX_USER:
            raise serializers.ValidationError(
                f'Bir sorovda eng kop {self.MAX_USER} ta user'
            )
        if any(u.pk == self.context['project'].owner_id for u in users):
            raise serializers.ValidationError('Owner azo sifatilda qoshilmaydi')
        return users


# class ProjectAddMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectMember
#         fields = ['project',
#                   'user',
#                   'role',
#                   'join_date']
#         read_only_fields = [
#             'project',
#             'join_date'
#         ]
