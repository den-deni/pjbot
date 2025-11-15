from routers.navigation import select_router
from routers.handler_encoder import encoder_router
from routers.settings_handler import settings_router
from routers.key_handler import key_router
from routers.encoderfile import file_router
from admin.adminhandler import admin_router



routers = [select_router,
           encoder_router,
           settings_router,
           key_router,
           file_router,
           admin_router]