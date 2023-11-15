from telegram import Update
from telegram.ext import CallbackContext
from random import randint

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("ayo wassup")

async def ping(update: Update, context: CallbackContext):
    await update.message.reply_text(f"Your current latency: {randint(7, 250)}ms")

async def random(update: Update, context: CallbackContext):
    await update.message.reply_text(f"Here's your random number: {randint(0, 100)}")