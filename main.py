from rubiko import RubikaBot
import paho.mqtt.client as mqtt
import json

# ⚠️ توکن رباتی که از BotFather گرفتید را اینجا بگذارید
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = RubikaBot(BOT_TOKEN)

# تنظیمات MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC_VERIFY = "bugTracker/IR/v2/auth/verify/"

# اتصال به MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@bot.on_message()
async def handle_message(message):
    text = message.text
    
    # وقتی کاربر روی لینک کلیک می‌کند، پیامی مثل /start AUTH_XXXX می‌آید
    if text and text.startswith("/start"):
        parts = text.split()
        
        if len(parts) > 1:
            token = parts[1] # کد امن را جدا می‌کنیم
            
            # پیام موفقیت را از طریق MQTT به سایت می‌فرستیم
            payload = json.dumps({"status": "success"})
            mqtt_client.publish(MQTT_TOPIC_VERIFY + token, payload)
            
            await bot.send_message(message.chat_id, "✅ شماره شما با موفقیت تایید شد! حالا به سایت برگردید.")
        else:
            await bot.send_message(message.chat_id, "سلام! برای تایید حساب، لطفاً از لینکی که در سایت به شما داده شده استفاده کنید.")

print("ربات روبیکا روشن شد و منتظر پیام است...")
bot.run()
