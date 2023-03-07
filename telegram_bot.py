import logging
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, Defaults
from telegram.helpers import escape_markdown

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
            .defaults(Defaults(parse_mode=ParseMode.MARKDOWN_V2))
            .build()
        )

    def format_report(self, title, data): 
        message = f'*{title}:*\n'
        index = 1
        for row in data:
            name = escape_markdown(row.name, version=2)
            message += f'{str(index)}\. {name} \- _{row.amount}_'
            if row.difference > 0:
                diff = escape_markdown(f'↑+{row.difference}', version=2)
                message += f' *{diff}*'
            elif row.difference < 0:
                diff = escape_markdown(f'↓{row.difference}', version=2)
                message += f' *{diff}*'
            message += '\n'
            index += 1
        
        if index > 1:
            message +=  escape_markdown(f'Updated at - {data[0].current} (UTC)\n', version=2) 
        print(message)
        return message

    async def send_report(self, report, title):
        message = self.format_report(title, report)
        await self.application.bot.send_message(
            chat_id=self.chat_id,
            text=message
        )