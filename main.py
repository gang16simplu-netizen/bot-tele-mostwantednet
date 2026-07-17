import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# CONFIGURARE FINALĂ
TOKEN = "import os⁠
⁠TOKEN = os.environ.get("TOKEN")⁠"
ADMIN_ID = 8201035899
STAFF_GROUP_ID = -1003936586656
MAIN_GROUP_ID = -1003864809495

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Trimite pozele/video-urile pentru verificare.")

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Funcția 13: Detectare Forward
    is_forwarded = update.message.forward_from or update.message.forward_sender_name
    caption = "⚠ ATENȚIE: Conținut forwardat!" if is_forwarded else "Verificare nouă:"
    
    keyboard = [
        [InlineKeyboardButton("Aprobă", callback_data=f"app_{update.message.from_user.id}")],
        [InlineKeyboardButton("Respinge", callback_data=f"rej_{update.message.from_user.id}")]
    ]
    
    # Redirecționare către grupul de Staff
    await context.bot.forward_message(chat_id=STAFF_GROUP_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    await context.bot.send_message(chat_id=STAFF_GROUP_ID, text=f"{caption} User: {update.message.from_user.id}", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action, user_id = query.data.split('_')
    
    if action == "app":
        # Generare link unic și log către tine
        link = await context.bot.create_chat_invite_link(chat_id=MAIN_GROUP_ID, member_limit=1)
        await context.bot.send_message(chat_id=user_id, text=f"Aprobat! Link: {link.invite_link}")
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Log: User {user_id} aprobat de {query.from_user.username}")
    else:
        # Hard-Reject
        await context.bot.send_message(chat_id=user_id, text="Cerere respinsă. Revino în 30 de minute.")
    
    await query.message.delete()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Botul MostWanted este activ și rulează.")
    app.run_polling()
