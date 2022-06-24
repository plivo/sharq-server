import os
from .server import setup_server


server = setup_server('/app/config/sharq.conf')
app = server.app
