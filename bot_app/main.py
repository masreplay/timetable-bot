import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from asc_scrapper.main import get_schedule_image
from config import get_settings

logging.basicConfig(level=logging.INFO)

API_TOKEN = get_settings().telegram_bot_api_token

bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    branch = State()  # Will be represented in storage as 'Form:name'
    stage = State()  # Will be represented in storage as 'Form:age'
    shift = State()  # Will be represented in storage as 'Form:gender'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.branch.set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("امنية", "برمجيات")
    markup.add("وسائط", "وسائط")
    markup.add("شبكات", "نظم")

    await message.reply("اختر الفرع", reply_markup=markup)


@dp.message_handler(state=Form.branch)
async def process_branch(message: types.Message, state: FSMContext):
    """
    Process branch name
    """
    async with state.proxy() as data:
        data['branch'] = message.text

    await Form.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("ثاني", "اول")
    markup.add("رابع", "ثالث")

    await message.reply("اختر المرحلة", reply_markup=markup)


@dp.message_handler(state=Form.stage)
async def process_stage(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['stage'] = message.text

    await Form.next()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("مسائي", "صباحي")

    await message.reply("اختر نوع الدراسة", reply_markup=markup)


@dp.message_handler(state=Form.shift)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['shift'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        name = f'{data["stage"]} {data["branch"]} {data["shift"]}'
        human_name = f'{data["branch"]} {data["stage"]} {data["shift"]}'

        url = get_schedule_image(name)

        # And send message
        await bot.send_photo(
            chat_id=message.chat.id,
            caption=md.text(
                md.text(f"جدول: {md.bold(human_name)}"),
                sep='\n',
            ),
            photo=url,
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
