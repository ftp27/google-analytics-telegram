import logging
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, Defaults

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TelegramBot:
    def __init__(self, config):
        self.chat_id = config['chat_id']
        self.application = (
            ApplicationBuilder()
            .token(config['token'])
            .defaults(Defaults(parse_mode=ParseMode.MARKDOWN))
            .build()
        )

    def format_report(self, title, data): 
        message = f'*{title}:*\n'
        index = 1
        for row in data:
            message += f'{str(index)}. {row.name} - _{row.amount}_'
            if row.difference > 0:
                message += f' *↑+{row.difference}*'
            elif row.difference < 0:
                message += f' *↓{row.difference}*'
            message += '\n'
            index += 1
        
        if index > 1:
            message += f'Updated at - {data[0].current} (UTC)\n'
        return message

    async def send_report(self, report, title):
        message = self.format_report(title, report)
        await self.application.bot.send_message(
            chat_id=self.chat_id,
            text=message
        )