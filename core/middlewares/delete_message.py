from aiogram.dispatcher.middlewares.base import BaseMiddleware
import asyncio


class DeleteMessageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        handler,
        event,
        data
    ):
        # If chat type is private - just return
        if event.chat.type == "private":
            return await handler(event, data)
        
        # If message contains "погод" - just return
        if "погод" in event.text.lower() or "експертиз" in event.text.lower():
            return await handler(event, data)
        
        bot = data["bot"]  # Get the bot instance from data

        # Create async tasks for delayed message deletion
        async def delete_current_message():
            await asyncio.sleep(7)
            try:
                await bot.delete_message(event.chat.id, event.message_id)
            except Exception:
                pass  # Ignore errors if message was already deleted
        
        async def delete_next_message():
            await asyncio.sleep(7)
            try:
                await bot.delete_message(event.chat.id, event.message_id + 1)
            except Exception:
                pass  # Ignore errors if message was already deleted
        
        # Start the deletion tasks
        asyncio.create_task(delete_current_message())
        asyncio.create_task(delete_next_message())

        return await handler(event, data)
