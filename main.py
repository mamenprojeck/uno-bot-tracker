import json
import os
import logging
import threading
import telebot
from telebot.types import Message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MASUKKAN TOKEN BOT KAMU DISINI
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8451868475:AAFkwwz1SL6BqgAUWdtrkMLWSpeXghDK-uE")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"
CONFIG_FILE = "config.json"
data_lock = threading.Lock()

# --- Load / Save Data ---
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "pesan_tambahan": "jangan sok keras tol! masi ada langit di atas langit"
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

data = load_data()
config = load_config()

# --- Utility Functions ---
def is_admin(message: Message):
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    return chat_member.status in ["creator", "administrator"]

def extract_winner(text: str):
    words = text.split()
    for word in words:
        if word.startswith("@"):
            return word
    return "Unknown"

def is_game_bot(message: Message):
    allowed_bots = ["MauMauMauMauBot", "play_unobot"]
    if message.via_bot and message.via_bot.username:
        return message.via_bot.username in allowed_bots
    return False

# --- Commands ---
@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.reply_to(message, "👋 Halo! Saya bot pelacak poin Uno.")

@bot.message_handler(commands=["cekpoin"])
def cmd_cekpoin(message):
    user = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    with data_lock:
        score = data.get(user, 0)
    bot.reply_to(message, f"🏆 {user}, poin kamu saat ini: {score}")

@bot.message_handler(commands=["ranking"])
def cmd_ranking(message):
    with data_lock:
        if not data:
            bot.reply_to(message, "Belum ada poin 😅")
            return
        sorted_scores = sorted(data.items(), key=lambda x: x[1], reverse=True)
    text = "🏆 *Leaderboard Uno*\n\n"
    for i, (user, score) in enumerate(sorted_scores, 1):
        text += f"{i}. {user} — {score} poin\n"
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=["addpoin"])
def cmd_addpoin(message):
    if not is_admin(message):
        bot.reply_to(message, "❌ Hanya admin yang bisa menambah poin!")
        return
    parts = message.text.split()[1:]
    if not parts:
        bot.reply_to(message, "Format: /addpoin @user 5")
        return
    user = parts[0]
    points = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
    with data_lock:
        data[user] = data.get(user, 0) + points
        save_data(data)
    bot.reply_to(message, f"✅ {points} poin ditambahkan untuk {user}")

@bot.message_handler(commands=["menuuno"])
def cmd_menuuno(message):
    if not is_admin(message):
        bot.reply_to(message, "❌ Hanya admin yang bisa membuka menu.")
        return
    menu = (
        "📜 *Menu Uno Bot* 📜\n"
        "/cekpoin — Cek poin sendiri\n"
        "/ranking — Lihat leaderboard\n"
        "/addpoin — Tambah poin manual (admin)\n"
        "/menuuno — Lihat menu (admin)\n"
        "/editpesan — Edit pesan tambahan (admin)\n"
    )
    bot.reply_to(message, menu, parse_mode="Markdown")

@bot.message_handler(commands=["editpesan"])
def cmd_editpesan(message):
    if not is_admin(message):
        bot.reply_to(message, "❌ Hanya admin yang bisa edit pesan.")
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Format: /editpesan <pesan_baru>")
        return
    new_msg = parts[1]
    config["pesan_tambahan"] = new_msg
    save_config(config)
    bot.reply_to(message, f"✅ Pesan tambahan berhasil diubah:\n{new_msg}")

# --- Message Handler ---
@bot.message_handler(func=lambda m: True)
def handle_message(message: Message):
    text = message.text or ""

    # Game Ended detection
    if "game ended" in text.lower():
        bot.reply_to(message, "lanjutla tol poin nya kentang kali tu")
        return

    # Detect win from allowed bots
    if is_game_bot(message) and "won!" in text.lower():
        winner = extract_winner(text)
        with data_lock:
            data[winner] = data.get(winner, 0) + 1
            total = data[winner]
            save_data(data)
        # Balas otomatis pemenang
        bot.reply_to(message, f"🎉 {winner} mendapatkan tambahan 1 poin! Total poin sekarang: {total}\n{config.get('pesan_tambahan','')}")


# --- Run Bot ---
if __name__ == "__main__":
    logger.info("🤖 Bot starting...")
    print("🤖 Bot berjalan...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise
