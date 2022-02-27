def set_hook():
    import asyncio
    from aiogram import Bot
    from app.core.config import settings
    bot = Bot(token=settings().telegram_bot_api_token)

    async def hook_set():
        if not settings().heroku_app_name:
            print('You have forgot to set HEROKU_APP_NAME')
            quit()
        await bot.set_webhook(settings().WEBHOOK_URL)
        print(await bot.get_webhook_info())

    asyncio.run(hook_set())
    bot.close()


def start():
    from bot_app.main import main
    main()
