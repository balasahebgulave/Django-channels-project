from channels.routing import ProtocolTypeRouter, URLRouter
from Application.consumer import TickTockConsumer, ChatConsumer, AddMachineConsumer, DisplayAllMachine
from django.urls import path
from channels.auth import AuthMiddlewareStack


urlpatterns = ProtocolTypeRouter({

	"websocket":AuthMiddlewareStack(URLRouter([
	path('ws/',TickTockConsumer),
	path('chat/',ChatConsumer),
	path('addmachine/',AddMachineConsumer),
	path('displaymachines/',DisplayAllMachine)
	])
  )
})