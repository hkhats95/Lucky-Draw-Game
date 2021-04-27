from rest_framework import serializers
from .models import User, RaffleTicket, LuckyDraw


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'email']


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username']
        )
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user
        



class TicketSerializer(serializers.ModelSerializer):
    
    owner = UserSerializer(many=False)

    class Meta:
        model = RaffleTicket
        exclude = ('created',)


class LuckyDrawSerializer(serializers.ModelSerializer):
    
    winners = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = LuckyDraw
        fields = ['id', 'title', 'reward', 'numberofwinners', 'winners', 'live', 'enddate',]