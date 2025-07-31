from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os

TOKEN = os.getenv("7293066873:AAE6t4ueT8lm_0LhM-WF1bVx5SfhJMLeU5w")

data_file = 'user_data.json'

def load_data():
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! Botga xush kelibsiz.\nFormat: /add 10.5 1200000")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    try:
        doll = float(context.args[0])
        sum_uzs = float(context.args[1])
    except:
        await update.message.reply_text("❌ To'g'ri format: /add 10.5 1200000")
        return

    if user_id not in data:
        data[user_id] = {"$": 0.0, "UZS": 0.0}

    data[user_id]["$"] += doll
    data[user_id]["UZS"] += sum_uzs
    save_data(data)

    await update.message.reply_text(f"✅ Qo‘shildi: {data[user_id]['$']} $ va {data[user_id]['UZS']} so‘m.")

async def send_monthly_reports(app):
    data = load_data()
    for user_id, values in data.items():
        text = f"📊 Hisobot:\n💵 {values['$']} $\n🇺🇿 {values['UZS']} so‘m"
        try:
            await app.bot.send_message(chat_id=int(user_id), text=text)
        except Exception as e:
            print(f"Xatolik {user_id}: {e}")
    save_data({})

def schedule_monthly_report(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: app.create_task(send_monthly_reports(app)), 'cron', day=30, hour=23, minute=59)
    scheduler.start()

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    schedule_monthly_report(app)
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
