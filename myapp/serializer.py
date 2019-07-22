from rest_framework import serializers
from .models import ScrummyUser, ScrummyGoals, GoalStatus, Users, Admin
from .choice import target


class AdminUsersSerializers(serializers.ModelSerializer):
    # organization = serializers.CharField()


    class Meta:
        model = Users
        fields = ('id', 'username', 'email','is_admin', 'password')
        write_only_fields = ('password',)

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     # instance.is_user = True
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance

class UsersSerializers(serializers.ModelSerializer):
    # organization = serializers.CharField()


    class Meta:
        model = Users
        fields = ('id', 'username','first_name', 'last_name', 'email', 'is_user', 'password')
        write_only_fields = ('password',)

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     # instance.is_user = True
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance


class ScrummySerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """
    user = UsersSerializers()

    class Meta:
        model = ScrummyUser
        # fields = ( 'org', 'role')
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

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
        user = instance.user

        instance.org = validated_data.get('org', instance.org)
        instance.role = validated_data.get('role', instance.role)
        user.username = user_data.get('username', user.username)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        # user.user = user_data.get('username', user.username)

        instance.save()


        user.save()

        return instance



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

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
        user = instance.user

        instance.organization = validated_data.get('organization', instance.organization)
        user.username = user_data.get('username', user.username)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        # user.user = user_data.get('username', user.username)

        instance.save()


        user.save()

        return instance


class StatusSerializer(serializers.ModelSerializer):
    # target = serializers.ChoiceField(choices= target,source='get_target_display')
    class Meta:
        model = GoalStatus
        fields = ('id', 'target')



class ScrummyGoalsSerializer(serializers.ModelSerializer):
    # username = UserTaskSerializer()
    # target_name = StatusSerializer()

    # user_name = UserTaskSerializer()

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
        target_data = validated_data.pop('target_name')

        # user = ScrummySerializer.create(ScrummySerializer(), validated_data=user_data)
        # status = StatusSerializer.create(StatusSerializer(), validated_data=target_data)
        task, created = ScrummyGoals.objects.update_or_create(user_name= user_data,
                                                        task=validated_data.pop('task'), target_name=target_data)
        return task

    def update(self, instance, validated_data):
        instance.task = validated_data.get('task', instance.task)
        instance.target_name = validated_data.get('target_name', instance.target_name)
        instance.user_name= validated_data.get('user_name', instance.user_name)

        instance.save()
        return instance