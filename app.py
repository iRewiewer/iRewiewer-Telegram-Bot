from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from os import getcwd
import simple_commands as simple_command
import birthday_commands as birthday_command

TOKEN = open(f"{getcwd()}\\token.txt", 'r').read()
USERNAME = "@irewiewerbot"

commands = """
ping - Test your ping.
random - Get a random number.
bdaynew - Add a birthday date.
bdayremove - Remove a birthday date by id.
bdaylist - List all birthdays
"""

async def handle_message(update: Update, context: CallbackContext):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User [{update.message.chat.full_name}] ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if USERNAME not in text:
            return

    response: str = "I don't talk, I just respond to commands."

    print(f'Bot: {response}')

    await update.message.reply_text(response)

async def error(update: Update, context: CallbackContext):
    print(f"Command {update.message.text} caused error {context.error}")

def main() -> None:
    print("Starting bot")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', simple_command.start))
    app.add_handler(CommandHandler('ping', simple_command.ping))
    app.add_handler(CommandHandler('random', simple_command.random))
    app.add_handler(CommandHandler('bdaynew', birthday_command.bdaynew))
    app.add_handler(CommandHandler('bdayremove', birthday_command.bdayremove))
    app.add_handler(CommandHandler('bdaylist', birthday_command.bdaylist))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(birthday_command.bdaynew_conv_handler)
    app.add_handler(birthday_command.bdayremove_conv_handler)

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval = 3, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()