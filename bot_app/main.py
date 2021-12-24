import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
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

# branches = ["امنية", "برمجيات", "وسائط", "ذكاء", "شبكات", "نظم"]
# stages = ["ثاني", "اول", "رابع", "ثالث"]
# shifts = ["صباحي", "مسائي"]

branches = {
    "امنية": {
        "اول": ["صباحي", "مسائي"],
        "ثاني": ["صباحي", "مسائي"],
        "ثالث": ["صباحي", "مسائي"],
        "رابع": ["صباحي", "مسائي"],
    },
    "برمجيات": {
        "ثاني": ["صباحي", "مسائي"],
        "اول": ["صباحي", "مسائي"],
        "رابع": ["صباحي", "مسائي"],
        "ثالث": ["صباحي", "مسائي"]
    },
    "وسائط": {
        "ثاني": ["صباحي", "مسائي"],
        "اول": ["صباحي", "مسائي"],
        "رابع": ["صباحي", "مسائي"],
        "ثالث": ["صباحي", "مسائي"]
    },
    "ذكاء": {
        "ثاني": ["صباحي", "مسائي"],
        "اول": ["صباحي", "مسائي"],
        "رابع": ["صباحي", "مسائي"],
        "ثالث": ["صباحي", "مسائي"]
    },
    "شبكات": {
        "ثاني": ["صباحي", "مسائي"],
        "اول": ["صباحي", "مسائي"],
        "رابع": ["صباحي", "مسائي"],
        "ثالث": ["صباحي", "مسائي"]
    },
    "نظم": {
        "ثاني": ["صباحي", "مسائي"],
        "اول": ["صباحي", "مسائي"],
        "رابع": ["صباحي", "مسائي"],
        "ثالث": ["صباحي", "مسائي"]
    },
}


# States
class Form(StatesGroup):
    branch = State()  # Will be represented in storage as 'Form:name'
    stage = State()  # Will be represented in storage as 'Form:age'
    shift = State()  # Will be represented in storage as 'Form:gender'


@dp.message_handler(commands='schedule')
async def cmd_schedule(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.branch.set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    # return list of branches
    items = list(branches.keys())
    for i in range(0, len(items), 2):
        markup.add(items[i], items[i + 1])

    await message.reply("اختر الفرع", reply_markup=markup)


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    types.ReplyKeyboardRemove()

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('تم الالغاء', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text not in branches.keys(), state=Form.branch)
async def process_branch_invalid(message: types.Message):
    return await message.reply("اختر من القائمة")


@dp.message_handler(state=Form.branch)
async def process_branch(message: types.Message, state: FSMContext):
    """
    Process branch name
    """
    async with state.proxy() as data:
        data['branch'] = message.text

    await Form.next()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    # Return list of stages remove stage witch doesn't have any shifts
    unfiltered_stages = list(branches[data['branch']].items())
    stages = [stage for stage, shifts in unfiltered_stages if len(shifts) > 0]

    for i in range(0, len(stages), 2):
        try:
            markup.add(stages[i], stages[i + 1])
        except IndexError:
            markup.add(stages[i])

    await message.reply("اختر المرحلة", reply_markup=markup)


# @dp.message_handler(lambda message: message.text not in branches, state=Form.stage)
# async def process_stage_invalid(message: types.Message):
#     return await message.reply("اختر من القائمة")


@dp.message_handler(state=Form.stage)
async def process_stage(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['stage'] = message.text

    await Form.next()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    shifts = list(branches[data['branch']][data['stage']])

    for i in range(0, len(shifts), 2):
        try:
            markup.add(shifts[i], shifts[i + 1])
        except IndexError:
            markup.add(shifts[i])

    await message.reply("اختر نوع الدراسة", reply_markup=markup)


# @dp.message_handler(lambda message: message.text not in shifts, state=Form.shift)
# async def process_shift_invalid(message: types.Message):
#     return await message.reply("اختر من القائمة")


@dp.message_handler(state=Form.shift)
async def process_shift(message: types.Message, state: FSMContext):
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


@dp.message_handler(commands='teachers')
async def cmd_schedule(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.branch.set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    # return list of branches
    items = list(branches.keys())
    for i in range(0, len(items), 2):
        markup.add(items[i], items[i + 1])

    await message.reply("اختر الفرع", reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
