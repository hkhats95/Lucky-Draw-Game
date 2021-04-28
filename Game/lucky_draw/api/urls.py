from django.urls import path
from . import views

from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'luckydraw_api'

urlpatterns = [
	# path('docs/', include_docs_urls(title="Docs")),
	path('', views.index, name='index'),
	path('login', obtain_auth_token, name='login'),
	path('register', views.registration_view, name='register'),
	path('ticket/buy', views.buyTicket, name='ticket-buy'),
	path('events/future', views.nextLuckyDrawEvents, name='next-lucky-draw-events'),
	path('events/<int:pk>/participate', views.participateInLuckyDraw, name='participate-in-lucky-draw'),
	path('events/winners/lastweek', views.lastWeekWinners, name='last-week-winners'),
	path('events/<int:pk>/close', views.closeEvent, name='close-event'),
    path('events/toclose', views.eventToClose, name='to-close-events'),
    path('events/create', views.eventCreate, name='create-event'),
]