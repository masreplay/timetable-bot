from aiogram.utils.callback_data import CallbackData

classrooms_cb = CallbackData('classrooms', 'id', 'action')

teachers_paging_cb = CallbackData('teachers', 'page', 'action')
teacher_cb = CallbackData('teacher', 'id', 'action')

subjects_paging_cb = CallbackData('subjects', 'page', 'action')
subject_cb = CallbackData('subject', 'id', 'action')

rooms_paging_cb = CallbackData('rooms', 'page', 'action')
room_cb = CallbackData('room', 'id', 'action')
