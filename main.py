import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Preluăm Token-ul din variabilele de mediu
TOKEN = os.environ.get("TOKEN")

# Funcția care răspunde la /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut! Botul este activ și rulează pe Railway.")

def main():
    if not TOKEN:
        print("Eroare: Token-ul nu a fost găsit!")
        return

    # Configurăm botul
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Adăugăm comanda /start
    app.add_handler(CommandHandler("start", start))
    
    print("Botul a pornit cu succes!")
    app.run_polling()

if __name__ == '__main__':
    main()
