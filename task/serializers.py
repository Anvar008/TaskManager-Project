from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['project',
                  'title',
                  'description',
                  'status',
                  'priority',
                  'assigned_to',]


    def validate(self, attrs):
        assigned_to = attrs.get('assigned_to')
        project = attrs.get('project')
        if assigned_to and project and not project.members.filter(id=assigned_to.id).exists():
            raise serializers.ValidationError({
                'assign_to': "User not found"
            })
        return attrs
