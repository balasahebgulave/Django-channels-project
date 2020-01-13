from channels.routing import ProtocolTypeRouter, URLRouter
from Application.consumer import CpuRamConsumer, ChatConsumer, AddMachineConsumer, DisplayAllMachineConsumer
from django.urls import path
from channels.auth import AuthMiddlewareStack


urlpatterns = ProtocolTypeRouter({

	"websocket":AuthMiddlewareStack(URLRouter([
	path('ws/',CpuRamConsumer),
	path('chat/',ChatConsumer),
	path('addmachine/',AddMachineConsumer),
	path('displaymachines/',DisplayAllMachineConsumer)
	])
  )
})