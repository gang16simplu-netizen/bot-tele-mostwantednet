import os
from telegram.ext import ApplicationBuilder

# Preluăm Token-ul din variabilele de mediu (Koyeb/Railway)
TOKEN = os.environ.get("TOKEN")

# ID-urile tale (le-am păstrat ca până acum)
STAFF_GROUP_ID = "ID_AICI" # Înlocuiește cu ID-ul real
MAIN_GROUP_ID = "ID_AICI"  # Înlocuiește cu ID-ul real

def main():
    if not TOKEN:
        print("Eroare: Token-ul nu a fost găsit în variabilele de mediu!")
        return

    # Aici vine restul codului tău de inițializare a botului
    # De exemplu:
    # app = ApplicationBuilder().token(TOKEN).build()
    # app.run_polling()
    
    print("Botul a pornit cu succes!")

if __name__ == '__main__':
    main()
