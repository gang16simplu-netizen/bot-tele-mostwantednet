import os
import pyotp
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, 
    filters, ContextTypes, ConversationHandler
)

# Configurare logare
logging.basicConfig(level=logging.INFO)

# Inițializare cheie TOTP - asigură-te că variabila TOTP_SECRET este setată în Railway
SECRET = os.environ.get("TOTP_SECRET")
totp = pyotp.TOTP(SECRET)
WAITING_FOR_PASS = 1

# Funcție pentru salvarea în baza de date
def log_to_file(user_id, username, status):
    with open("baza_date.txt", "a") as f:
        f.write(f"{user_id} | {username} | {status}\n")

# --- Comenzi ---
async def start_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Introdu codul de 6 cifre:")
    return WAITING_FOR_PASS

async def check_totp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text
    if totp.verify(user_code):
        if os.path.exists("baza_date.txt"):
            with open("baza_date.txt", "rb") as f:
                await update.message.reply_document(document=f)
        else:
            await update.message.reply_text("Baza de date este goală.")
    else:
        await update.message.reply_text("Cod incorect!")
    return ConversationHandler.END

async def start_kyc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_to_file(update.effective_user.id, update.effective_user.username, "In asteptare")
    await update.message.reply_text("Datele au fost salvate.")

if __name__ == '__main__':
    # Token-ul trebuie să fie în variabilele de mediu din Railway
    TOKEN = os.environ.get("TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    admin_conv = ConversationHandler(
        entry_points=[CommandHandler("admin", start_admin)],
        states={WAITING_FOR_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_totp)]},
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)]
    )

    app.add_handler(admin_conv)
    app.add_handler(CommandHandler("kyc", start_kyc))

    print("Botul a pornit!")
    app.run_polling()
