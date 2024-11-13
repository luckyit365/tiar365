import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Memuat file .env
load_dotenv()

# Mengambil API Key dari .env
API_KEY = os.getenv("TELEGRAM_API_KEY")

# Fungsi untuk mengecek domain di situs Trust Positif
def check_domain(domain):
    url = "https://trustpositif.kominfo.go.id/check"
    response = requests.post(url, data={'search': domain})

    if "Ada" in response.text:
        return "Status: Ada dalam daftar Trust Positif"
    else:
        return "Status: Tidak ada dalam daftar Trust Positif"

# Fungsi yang akan dipanggil ketika command /check di Telegram
def check(update: Update, context: CallbackContext) -> None:
    if context.args:
        domain = context.args[0]
        status = check_domain(domain)
        update.message.reply_text(f"Hasil pengecekan untuk {domain}:\n{status}")
    else:
        update.message.reply_text("Silakan masukkan domain setelah perintah /check. Contoh: /check domain.com")

def main():
    # Pastikan API Key ada
    if not API_KEY:
        print("Error: TELEGRAM_API_KEY tidak ditemukan. Pastikan sudah disimpan di file .env.")
        return

    updater = Updater(API_KEY)
    dispatcher = updater.dispatcher

    # Daftarkan perintah /check ke handler
    dispatcher.add_handler(CommandHandler("check", check))

    # Mulai bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
