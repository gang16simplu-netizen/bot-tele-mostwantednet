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

# Inițializare variabile
TOTP_SECRET = os.environ.get("TOTP_SECRET")
totp = pyotp.TOTP(TOTP_SECRET)
WAITING_FOR_PASS = 1

# Funcție pentru salvarea în baza de date simplă
def log_to_file(user_id, username, status):
    with open("baza_date.txt", "a") as f:
        f.write(f"{user_id} | {username} | {status}\n")

# --- Funcții Autentificare Admin ---
async def start_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Introdu codul de 6 cifre din Google Authenticator:")
    return WAITING_FOR_PASS

async def check_totp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text
    if totp.verify(user_code):
        try:
            with open("baza_date.txt", "rb") as f:
                await update.message.reply_document(document=f)
            await update.message.reply_text("Autentificare reușită. Iată baza de date.")
        except FileNotFoundError:
            await update.message.reply_text("Baza de date este goală.")
    else:
        await update.message.reply_text("Cod incorect! Încearcă din nou.")
    return ConversationHandler.END

# --- Exemplu de utilizare în bot ---
async def start_kyc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Aici ar veni logica ta de primire poze/date
    log_to_file(update.effective_user.id, update.effective_user.username, "In asteptare")
    await update.message.reply_text("Datele au fost salvate. Așteaptă aprobarea.")

# --- Configurare Aplicație ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get("TOKEN")).build()

    # ConversationHandler pentru /admin
    admin_conv = ConversationHandler(
        entry_points=[CommandHandler("admin", start_admin)],
        states={WAITING_FOR_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_totp)]},
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)]
    )

    app.add_handler(admin_conv)
    app.add_handler(CommandHandler("kyc", start_kyc))

    print("Botul a pornit!")
    app.run_polling()
