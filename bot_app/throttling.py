async def timetable_throttled(*args, **kwargs):
    message = args[0]  # as message was the first argument in the original handler
    await message.answer("الرجاء الانتظار")
