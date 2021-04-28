from datetime import datetime, timedelta
import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import TicketSerializer, LuckyDrawSerializer, UserSerializer, RegistrationSerializer

from lucky_draw.models import User, RaffleTicket, LuckyDraw
# Create your views here.

# View for handling index url
@api_view(['GET',])
def index(request):
    data = {}
    data['message'] = "Welcome to the Lucky Draw game."
    data['login'] = {
        "method": "POST",
        "url": "/login",
        "body": {
            "username": "email address.",
            "password": "password"
        }
    }
    data['register'] = {
        "method": "POST",
        "url": "/register",
        "body": {
            "username": "user name",
            "email": "email address",
            "password": "password",
            "password2": "confirm password",
        }
    }
    return Response(data)


# View for handling registration request
@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['Response'] = 'Successfully registered a new user.'
        data['email'] = user.email
        data['username'] = user.username
        token = Token.objects.get(user=user).key
        data['token'] = token
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


# View for handling buy ticket request.
@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def buyTicket(request):
    """
    API endpoint to buy a ticket. (Only logged-in users allowed)
    """
    user = request.user
    ticket = RaffleTicket.objects.create(owner=user)
    serializer = TicketSerializer(ticket, many=False)
    return Response(serializer.data)


# View for showing future lucky draw events
@api_view(['GET',])
def nextLuckyDrawEvents(request):
    """
    API endpoint to display upcoming lucky draw events. (No authentication required)
    """
    today = timezone.now()
    events = LuckyDraw.objects.filter(enddate__gte=today).order_by('-enddate')
    serializer = LuckyDrawSerializer(events, many=True)
    return Response(serializer.data)


# View for handling participation request
@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def participateInLuckyDraw(request, pk):
    """
    API endpoint to allow user to enter a lucky draw contest. (Only logged-in users allowed)
    """
    user = request.user
    data = {}
    try:
        event = LuckyDraw.objects.get(id=pk)
    except LuckyDraw.DoesNotExist:
        data['error'] = "Object does not exist."
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    draws = user.luckydraws.all()
    
    if event in draws:
        data['message'] = "Already entered in this lucky draw."
        return Response(data, status=status.HTTP_208_ALREADY_REPORTED)


    if (not event.live) or (timezone.now() > event.enddate):
        data['error'] = "This event is closed."
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    

    tickets = user.tickets.filter(luckydraw__isnull=True)
    if len(tickets) == 0:
        data['error'] = "No empty tickets found."
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    ticket = tickets[0]
    
    try:
        ticket.luckydraw = event
        ticket.save()
        event.players.add(user)
        event.save()
        data['message'] = "Successfully entered the lucky draw event."
        return Response(data)
    except:
        data['error'] = "Some error occured."
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View for handling last week winners request
@api_view(['GET',])
def lastWeekWinners(request):
    """
    API endpoint to display winners from the last week lucky draw events. (No authentication required)
    """
    today = timezone.now()
    last_week = today - timedelta(days=7)
    events = LuckyDraw.objects.filter(enddate__range=(last_week, today), live=False)
    serializer = LuckyDrawSerializer(events, many=True)
    return Response(serializer.data)


# View for closing the event and declaring winners
@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def closeEvent(request, pk):
    """
    API endpoint to close an active lucky draw. (Only admin users allowed)
    """
    data = {}
    try:
        event = LuckyDraw.objects.get(id=pk)
    except LuckyDraw.DoesNotExist:
        data['error'] = "Object does not exist."
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    
    if timezone.now() < event.enddate:
        data['error'] = f"Cannot end this event before {event.enddate}."
        return Response(data, status=status.HTTP_412_PRECONDITION_FAILED)
    
    if event.live == False:
        serializer = LuckyDrawSerializer(event, many=False)
        return Response(serializer.data)
    
    try:
        users = event.players.all()
        cnt = event.numberofwinners
        winnerind = random.sample(range(len(users)), min(cnt, len(users)))
        for ind in winnerind:
            event.winners.add(users[ind])
        event.live = False
        event.save()
        serializer = LuckyDrawSerializer(event, many=False)
        return Response(serializer.data)
    except:
        data['error'] = "Some error occured."
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


