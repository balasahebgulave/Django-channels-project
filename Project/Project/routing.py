from channels.routing import ProtocolTypeRouter, URLRouter
from Application.consumer import TickTockConsumer, ChatConsumer
from django.urls import path

urlpatterns = ProtocolTypeRouter({
	"websocket":URLRouter([
	path('ws/',TickTockConsumer),
	path('chat/',ChatConsumer)

	])
})