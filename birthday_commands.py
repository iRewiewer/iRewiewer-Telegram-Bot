from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from json import dumps, loads
from os import getcwd
from support import TryParseInt

async def bdaynew(update: Update, context: CallbackContext):
    await update.message.reply_text("Whose birthday do you want to add?")
    context.user_data['adding_birthday'] = True
    return "_get_name"
async def _get_name(update: Update, context: CallbackContext):
    name = update.message.text
    context.user_data['name'] = name
    await update.message.reply_text("On what date were they born?")
    return "_get_birthdate"
async def _get_birthdate(update: Update, context: CallbackContext):
    birthdate = update.message.text
    name = context.user_data.get('name', 'Unknown')
    _add_birthday(name, birthdate, update.message.chat.id)

    await update.message.reply_text(f"Added birthday for {name} on {birthdate}")
    context.user_data.clear()
    return ConversationHandler.END
def _add_birthday(name, birthdate, user_id):
    file = open(f"{getcwd()}\\BirthdaysData\\{user_id}.json", 'w+')
    bdays: {} = loads(file.read())
    bdays[bdays.keys()[-1] + 1] = (name, birthdate)
    file.write(dumps(bdays))
    file.close()

async def bdayremove(update: Update, context: CallbackContext):
    print("in bdayremove")
    await update.message.reply_text("Whose birthday do you want to remove by id?")
    return "_get_id"
async def _get_id(update: Update, context: CallbackContext):
    print("Entering _get_id function")
    bday_id = update.message.text
    response = _remove_birthday(update, bday_id)
    await update.message.reply_text(response)
    context.user_data.clear()
    return ConversationHandler.END
def _remove_birthday(update: Update, bday_id):
    file = open(f"{getcwd()}\\BirthdaysData\\{update.message.chat.id}.json", 'w+')
    contents = file.read()
    if contents == "":
        return "You don't have any birthdays added yet."
    if TryParseInt(bday_id) == None:
        return "That's not a valid numerical id."
    if int(bday_id) not in bdays.keys():
        return "Did not find a birthday with that id."

    bdays: {} = loads(contents)
    bdays.pop(bday_id)
    file.write(dumps(bdays))
    file.close()

    return f"Removed birthday for {bdays[bday_id]} ({bday_id})."

async def bdaylist(update: Update, context: CallbackContext):
    file = open(f"{getcwd()}\\BirthdaysData\\{update.message.chat.id}.json", 'w+')
    contents = file.read()
    if contents == "":
        await update.message.reply_text("You don't have any birthdays added yet.")
        return
    bdays: {} = loads(contents)
    file.close()

    response = "Your list of birthdays:\n"
    for bday_id in bdays:
        response += f"{bday_id}) {bdays[bday_id][0]} - {bdays[bday_id][1]}"

    await update.message.reply_text(response)

async def end(update: Update, context: CallbackContext):
    await update.message.reply_text("------- TRANSMISSION ENDED -------")
    context.user_data.clear()
    return ConversationHandler.END

bdaynew_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('bdaynew', bdaynew)],
    states={
        "_get_name": [MessageHandler(filters.TEXT & ~filters.COMMAND, _get_name)],
        "_get_birthdate": [MessageHandler(filters.TEXT & ~filters.COMMAND, _get_birthdate)],
    },
    fallbacks=[],
    allow_reentry=True,
)
bdayremove_conv_handler = ConversationHandler(
    entry_points=[CommandHandler(command='bdayremove', callback=bdayremove)],
    states={
        "_get_id": [MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=_get_id)],
    },
    fallbacks=[CommandHandler("end", end)],
    allow_reentry=True,
)
