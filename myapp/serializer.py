from rest_framework import serializers
from .models import ScrummyUser, ScrummyGoals, GoalStatus, Users, Admin


class AdminUsersSerializers(serializers.ModelSerializer):
    # organization = serializers.CharField()


    class Meta:
        model = Users
        fields = ('id', 'username', 'email','is_admin', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        # instance.is_user = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UsersSerializers(serializers.ModelSerializer):
    # organization = serializers.CharField()


    class Meta:
        model = Users
        fields = ('id', 'username','first_name', 'last_name', 'email', 'is_user', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        # instance.is_user = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ScrummySerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """
    user = UsersSerializers()

    class Meta:
        model = ScrummyUser
        fields = ('user', 'org','role')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')
        user = UsersSerializers.create(UsersSerializers(), validated_data=user_data)
        scrummy, created = ScrummyUser.objects.update_or_create(user=user,
                            org=validated_data.pop('org'), role=validated_data.pop('role'))
        return scrummy

class AdminSerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """
    user = AdminUsersSerializers()

    class Meta:
        model = Admin
        fields = ('user','organization')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')

        user = UsersSerializers.create(UsersSerializers(), validated_data=user_data)
        admin, created = Admin.objects.update_or_create(user=user,
                            organization=validated_data.pop('organization'))
        return admin

class ScrummyUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ScrummyUser
        fields = ('id','username','url' )

class ScrummyGoalsSerializer(serializers.Serializer):
    user_name = ScrummySerializer()

    class Meta:
        model = ScrummyGoals
        fields = ('id','task', 'target_name', 'user_name')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user_name')

        user = ScrummySerializer.create(ScrummySerializer(), validated_data=user_data)
        admin, created = ScrummyGoals.objects.update_or_create(user_name= user_data,
                                                        task=validated_data.pop('task'), target_name=validated_data.pop('target_name'))
        return admin

# class ScrummyGoalsSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = ScrummyGoals
#         fields = ('id','task', 'target_name', 'user_name','url')


class GoalStatusSerializer(serializers.HyperlinkedModelSerializer):
    #target = serializers.HyperlinkedIdentityField(view_name='status', lookup_field='pk')
    class Meta:
        model = GoalStatus
        fields  = ('id','target', 'url')