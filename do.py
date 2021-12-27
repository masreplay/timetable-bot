from config import *


def set_hook():
    import asyncio
    from aiogram import Bot
    bot = Bot(token=get_settings().telegram_bot_api_token)

    async def hook_set():
        if not get_settings().heroku_app_name:
            print('You have forgot to set HEROKU_APP_NAME')
            quit()
        await bot.set_webhook(WEBHOOK_URL)
        print(await bot.get_webhook_info())

    asyncio.run(hook_set())
    bot.close()


def start():
    from bot_app.main import main
    main()
