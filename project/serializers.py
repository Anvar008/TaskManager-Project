from rest_framework import serializers
from .models import *

class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name',
                  'description',
                  'owner',
                  'visibility',
                  'members']

class ProjectListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id',
                  'name',
                  'description',
                  'visibility',
                  'members']

class ProjectAddMemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ['project',
                  'user',
                  'role',
                  'join_date']
        read_only_fields = [
            'project',
            'join_date'
        ]
