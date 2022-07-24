from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/poll_results',consumers.PollResultsConsumer.as_asgi()),
]