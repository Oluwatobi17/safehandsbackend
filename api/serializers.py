# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from .models import User, TradeAccounts
# from .models import InterestHistory, TransactionHistory;

from django.contrib.auth import get_user_model

User = get_user_model();

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "fullName", "refID", "phoneno"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['email'], **validated_data)
        return user

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "walletAddress", "wallet", "fullName", "refID", "phoneno"]

    def create(self, validated_data):
        User.objects.create(**validated_data);

class LoginSerializers(serializers.Serializer):
    email = serializers.CharField() #max_length=255
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=True,
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        username = data.get('email')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "fullName", "wallet", "phoneno", "walletAddress"]

class ConnectAccountSerializer(serializers.ModelSerializer):
    account_password = serializers.CharField(write_only=True, required=True);

    class Meta:
        model = TradeAccounts;
        fields = ['user','account_id','account_name','account_password','broker','brokerNo','broker_server','broker_server_id','subscription'];

class ConnectedAccountSerializer(serializers.ModelSerializer):
    account_password = serializers.CharField(write_only=True, required=True);

    class Meta:
        model = TradeAccounts;
        fields = ['user','id','account_id','account_name','account_password','broker','brokerNo','broker_server','broker_server_id','subscription', 'expiration'];

class ReferedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User;
        fields = ['fullName', 'date_joined'];

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TransactionHistory
#         fields = ["amount", "status", "date", "wallet", "transaction_type", "user"]

# class UserUpdatePasswordSerialier(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True) 

# class UserUpdatePinSerialier(serializers.Serializer):
#     old_pin = serializers.CharField(required=True)
#     new_pin = serializers.CharField(required=True) 

# class UserUpdatePinSerialier(serializers.ModelSerializer):
#     password = serializers.CharField(
#         style={'input_type': 'pin'}
#     )
#     class Meta:
#         model = User
#         fields = ('pk', 'username', 'pin')

#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.set_password(validated_data.get('pin', instance.pin))
#         instance.save()
#         return instance
