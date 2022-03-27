from aiogram.utils.callback_data import CallbackData

classrooms_cb = CallbackData('classrooms', 'id', 'action')  # classrooms:<id>:<action>
teachers_cb = CallbackData('teachers', 'page', 'action')  # teachers:<id>:<action>
