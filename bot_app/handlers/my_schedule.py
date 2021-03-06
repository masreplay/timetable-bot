import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from app import schemas
from app.core.config import settings
from bot_app import service
from bot_app.handlers.callbackes import classrooms_cb
from bot_app.main import dp, bot
from bot_app.states import ScheduleType, StageScheduleForm
from bot_app.status import MESSAGE_500_INTERNAL_SERVER_ERROR


@dp.callback_query_handler(lambda c: c.data == ScheduleType.stages)
async def process_stage_schedule(query: types.CallbackQuery):
    await StageScheduleForm.branch.set()

    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    branches: list[schemas.Branch] = service.get_branches()

    markup.add(*[
        types.InlineKeyboardButton(text=branch.name,
                                   callback_data=classrooms_cb.new(id=str(branch.id), action='branch'))
        for branch in branches
    ])
    await query.message.reply(f"اختر الفرع", reply_markup=markup)


@dp.callback_query_handler(classrooms_cb.filter(action='branch'), state=StageScheduleForm.branch)
async def process_branch(query: types.CallbackQuery, callback_data: dict[str, str]):
    branch_id = callback_data['id']
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)

    stages: list[schemas.Stage] = service.get_stages(branch_id).results
    markup.add(*[
        types.InlineKeyboardButton(text=stage.name, callback_data=classrooms_cb.new(id=str(stage.id), action='stage'))
        for stage in stages
    ])

    await query.message.reply(f"اختر المرحلة", reply_markup=markup)

    await StageScheduleForm.next()


@dp.callback_query_handler(classrooms_cb.filter(action='stage'), state=StageScheduleForm.stage)
async def process_stage(query: types.CallbackQuery, callback_data: dict[str, str], state: FSMContext):
    stage_id = callback_data['id']

    await query.message.reply('جاري ارسال الجدول...', reply_markup=types.ReplyKeyboardRemove())
    # Remove keyboard
    markup = types.InlineKeyboardMarkup()

    try:
        image_url = service.get_schedule_image_url(stage_id=stage_id)

        schedule_front_url = f"{settings().FRONTEND_URL}/schedule/stages/{stage_id}"

        message = await bot.send_photo(
            chat_id=query.message.chat.id,
            caption=md.text(
                md.text(f"جدول: {md.link(image_url.name, schedule_front_url)}"),
                sep='\n',
            ),
            photo=image_url.url,
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    except:
        await bot.send_message(chat_id=query.message.chat.id, text=MESSAGE_500_INTERNAL_SERVER_ERROR)
    finally:
        await state.finish()
