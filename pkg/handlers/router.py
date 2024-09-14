from aiogram import Router
from .handler import r as handler_router

r = Router()

r.include_routers(handler_router)
