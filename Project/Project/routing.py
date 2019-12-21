from channels.routing import ProtocolTypeRouter, URLRouter
from Application.consumer import TickTockConsumer
from django.urls import path

urlpatterns = ProtocolTypeRouter({
	"websocket":URLRouter([
	path('ws/',TickTockConsumer),

	])
})