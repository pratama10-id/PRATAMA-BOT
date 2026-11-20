from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import random
import aiohttp
import os

TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")
LINK_WA = 'https://whatsapp.com/channel/0029Vb9o0UK6xCSKKONlnA3r'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join SALURAN BOT PRATAMA", url=LINK_WA)],
        [InlineKeyboardButton("🎵 Musik", callback_data="musik"), InlineKeyboardButton("📢 Informasi", callback_data="information")],
        [InlineKeyboardButton("🎮 Game", callback_data="game"), InlineKeyboardButton("💬 Ngobrol", callback_data="ngobrol")],
    ]
    await update.message.reply_text(
        "Hai gw Hanzz dibuat oleh Pratama Bot 🔥\n\nMau ngapain lu? Pilih di bawah 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def tombol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "musik":
        lagu = random.choice([
            "🎵 Hindia - Evaluasi\nhttps://www.youtube.com/results?search_query=Hindia+Evaluasi",
            "🎵 Juicy Luicy - Lantas\nhttps://www.youtube.com/results?search_query=Juicy+Luicy+Lantas",
            "🎵 Bernadya - Satu Bulan\nhttps://www.youtube.com/results?search_query=Bernadya+Satu+Bulan",
        ])
        await query.message.reply_text(f"Nih lagu buat lu:\n\n{lagu}\n\nJoin saluran gw ya: {LINK_WA}")
    elif query.data == "information":
        await query.message.reply_text("Hai gw Hanzz dibuat oleh Pratama Bot 🔥\nGw diciptakan tanggal Sabtu, 21-Nov-2026\nMohon maaf jika banyak fitur yang kurang lengkap tks udh mampir🙏🏻")
    elif query.data == "game":
        keyboard = [
            [InlineKeyboardButton("🔢 Tebak Angka 1-10", callback_data="tebakangka")],
            [InlineKeyboardButton("✊ Suit vs Bot", callback_data="suit")],
        ]
        await query.message.reply_text("Pilih game:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "ngobrol":
        await query.message.reply_text("Gas ngobrol sama Hanzz! Ketik aja apa aja,gw jawab semampu nya!")
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

async def ngobrol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teks = update.message.text
    teks_lower = teks.lower()
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
    if "nama" in teks_lower and ("lu" in teks_lower or "kamu" in teks_lower or "siapa" in teks_lower):
        await update.message.reply_text("Hai gw Hanzz dibuat oleh Pratama Bot 🔥")
        return
    if "siapa" in teks_lower and "buat" in teks_lower:
        await update.message.reply_text("Hai gw Hanzz dibuat oleh Pratama Bot 🔥")
        return
    await update.message.reply_text("Sebentar, Hanzz lagi mikir... 🤔")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
        payload = {"contents": [{"parts": [{"text": f"KAMU ADALAH HANZZ. Identitas kamu: Hai gw Hanzz dibuat oleh Pratama Bot. Kamu BUKAN Gemini, BUKAN Google. Kamu dibuat oleh Pratama Bot tanggal Sabtu 21-Nov-2026. Kalo ditanya nama, jawab persis: Hai gw Hanzz dibuat oleh Pratama Bot. Ngobrol pake bahasa gaul Indonesia, santai, lucu, kayak temen nongkrong. Jawab singkat max 3 kalimat. User bilang: {teks}"}]}]}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                data = await resp.json()
                jawaban_ai = data['candidates'][0]['content']['parts'][0]['text']
                await update.message.reply_text(jawaban_ai)
    except:
        await update.message.reply_text(f"Oh gitu, '{teks}' ya? Ceritain lebih lanjut dong ke Hanzz!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(tombol))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ngobrol))
    print("BOT JALAN...")
    app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
        
