from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from utils.dp_api.db_postgresql import Database

from aiogram.enums import ParseMode
from data import config


bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.CHAT, event_isolation=None)
db = Database()

