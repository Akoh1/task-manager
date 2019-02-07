from rest_framework import serializers
from .models import ScrummyUser, ScrummyGoals, GoalStatus

class ScrummyUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ScrummyUser
        fields = ('id','username','url' )



class ScrummyGoalsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ScrummyGoals
        fields = ('id','task', 'target_name', 'user_name','url')


class GoalStatusSerializer(serializers.HyperlinkedModelSerializer):
    #target = serializers.HyperlinkedIdentityField(view_name='status', lookup_field='pk')
    class Meta:
        model = GoalStatus
        fields  = ('id','target', 'url')