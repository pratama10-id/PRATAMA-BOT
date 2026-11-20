from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ChatMemberHandler, ContextTypes, filters
import random

TOKEN = '9150891723:AAHzrIAsroSej-_dSJ1OV5gAzajNKWdZO30'
LINK_WA = 'https://whatsapp.com/channel/0029Vb9o0UK6xCSKKONlnA3r'

async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("📢 Join SALURAN BOT PRATAMA", url=LINK_WA)],
        [InlineKeyboardButton("🎵 Musik", callback_data="musik"), InlineKeyboardButton("👋 Welcome", callback_data="welcome")],
        [InlineKeyboardButton("🎮 Game", callback_data="game"), InlineKeyboardButton("💬 Ngobrol", callback_data="ngobrol")],
    ]
    await update.message.reply_text(
        "🔥 HAI! Gw PRATAMA BOT!\n\nJangan lupa join saluran WA gw biar rame 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
async def tombol(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == "musik":
        lagu = random.choice([
            "🎵 Hindia - Evaluasi\nhttps://www.youtube.com/results?search_query=Hindia+Evaluasi",
            "🎵 Juicy Luicy - Lantas\nhttps://www.youtube.com/results?search_query=Juicy+Luicy+Lantas",
            "🎵 Bernadya - Satu Bulan\nhttps://www.youtube.com/results?search_query=Bernadya+Satu+Bulan",
        ])
        await query.message.reply_text(f"Nih lagu buat lu:\n\n{lagu}\n\nJoin saluran gw ya: {LINK_WA}")
    elif query.data == "welcome":
        await query.message.reply_text("Fitur Welcome udah aktif! Add bot ini ke grup, ada orang baru masuk nanti gw sambut otomatis.")
    elif query.data == "game":
        keyboard = [
            [InlineKeyboardButton("🔢 Tebak Angka 1-10", callback_data="tebakangka")],
            [InlineKeyboardButton("✊ Suit vs Bot", callback_data="suit")],
        ]
        await query.message.reply_text("Pilih game:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "ngobrol":
        await query.message.reply_text("Gas ngobrol! Ketik aja: halo, p, gabut, info")
    elif query.data == "tebakangka":
        angka = random.randint(1,10)
        context.user_data['angka'] = angka
        await query.message.reply_text("Gw udah mikir angka 1-10 nih! Coba tebak, ketik aja angkanya!")
    elif query.data == "suit":
        keyboard = [
            [InlineKeyboardButton("✊ Batu", callback_data="suit_batu"),
             InlineKeyboardButton("✋ Kertas", callback_data="suit_kertas"),
             InlineKeyboardButton("✌️ Gunting", callback_data="suit_gunting")],
        ]
        await query.message.reply_text("Suit sama gw! Pilih:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith("suit_"):
        pilih_lu = query.data.replace("suit_","")
        pilih_bot = random.choice(["batu","kertas","gunting"])
        if pilih_lu == pilih_bot:
            hasil = "SERI!"
        elif (pilih_lu=="batu" and pilih_bot=="gunting") or (pilih_lu=="kertas" and pilih_bot=="batu") or (pilih_lu=="gunting" and pilih_bot=="kertas"):
            hasil = "LU MENANG! 🔥"
        else:
            hasil = "LU KALAH! 😂"
        await query.message.reply_text(f"Lu: {pilih_lu}\nGw: {pilih_bot}\n\n{hasil}")	
async def welcome(update, context):
    for member in update.chat_member.new_chat_members:
        await update.effective_chat.send_message(
            f"👋 Welcome {member.first_name}!\nSelamat datang di grup!\n\nJangan lupa join juga 👇\n📢 SALURAN BOT PRATAMA\n{LINK_WA}"
        )

async def ngobrol(update, context):
    teks = update.message.text.lower()
    if 'angka' in context.user_data and teks.isdigit():
        jawaban = int(teks)
        if jawaban == context.user_data['angka']:
            await update.message.reply_text("BENER! 🔥 Lu jago! /start buat main lagi")
            del context.user_data['angka']
        elif jawaban < context.user_data['angka']:
            await update.message.reply_text("Kurang gede bro, naikin dikit!")
        else:
            await update.message.reply_text("Kegedean bro, turunin dikit!")
        return
    if "halo" in teks or "hi" in teks or teks == "p":
        await update.message.reply_text("Halo juga bro! Lagi ngapain?")
    elif "gabut" in teks:
        await update.message.reply_text("Sama, gw juga gabut. Mending main game, ketik /start terus pilih Game 🎮")
    elif "musik" in teks:
        await update.message.reply_text("Mau dengerin lagu? Ketik /start terus pencet Musik 🎵")
    elif "info" in teks:
        await update.message.reply_text(f"Gw bot buatan PRATAMA.\nJoin saluran gw: {LINK_WA}")
    else:
        await update.message.reply_text(f"Lu bilang: {teks}\n\nHehe gw masih belajar ngobrol, tapi gas aja!")
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(tombol))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ngobrol))
    print("BOT JALAN...")
    app.run_polling()

if __name__ == "__main__":
    main()
