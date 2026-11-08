import requests
import time
import json
import paho.mqtt.client as mqtt

# 👇 توکن رباتت رو اینجا بذار
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
API_URL = f"https://botapi.rubika.ir/v1/bot{BOT_TOKEN}"

# تنظیمات MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC_VERIFY = "bugTracker/IR/v2/auth/verify/"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

def send_rubika_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error sending message: {e}")

print("Bot started polling... Waiting for messages.")
offset_id = None

while True:
    try:
        payload = {}
        if offset_id:
            payload["offset_id"] = offset_id
            
        res = requests.post(f"{API_URL}/getUpdates", json=payload, timeout=15)
        data = res.json()

        if data.get("status") == "OK" and data.get("updates"):
            for update in data["updates"]:
                offset_id = update["update_id"] + 1
                
                msg = update.get("message")
                if msg:
                    text = msg.get("text", "")
                    chat_id = msg.get("sender_id")
                    
                    # اگر کاربر ربات رو استارت زد (مثلا /start AUTH_12345)
                    if text and text.startswith("/start"):
                        parts = text.split()
                        if len(parts) > 1:
                            token = parts[1] # کد امن رو جدا میکنیم
                            
                            # پیام موفقیت رو به سایت میفرستیم
                            mqtt_client.publish(MQTT_TOPIC_VERIFY + token, json.dumps({"status": "success"}))
                            
                            send_rubika_message(chat_id, "✅ شماره شما با موفقیت تایید شد! حالا به سایت برگردید.")
                        else:
                            send_rubika_message(chat_id, "سلام! برای تایید حساب، لطفاً از لینکی که در سایت به شما داده شده استفاده کنید.")
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(3)
    
    time.sleep(1) # جلوگیری از بلاک شدن
