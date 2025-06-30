import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.bot_token or not self.chat_id:
            raise ValueError("請在 .env 文件中設置 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")
    
    def send_message(self, message):
        """發送消息到 Telegram"""
        if not message:
            return False
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        # 添加時間戳
        est_time = datetime.now(pytz.timezone('US/Eastern'))
        message_with_time = f"[{est_time.strftime('%Y-%m-%d %H:%M:%S')} EST]\n{message}"
        
        try:
            response = requests.post(url, json={
                'chat_id': self.chat_id,
                'text': message_with_time,
                'parse_mode': 'HTML'
            })
            
            if response.status_code == 200:
                return True
            else:
                print(f"發送 Telegram 消息失敗: {response.text}")
                return False
                
        except Exception as e:
            print(f"發送 Telegram 消息時發生錯誤: {str(e)}")
            return False
    
    def send_error(self, error_message):
        """發送錯誤消息到 Telegram"""
        message = f"❌ 錯誤:\n{error_message}"
        return self.send_message(message)
    
    def send_success(self, success_message):
        """發送成功消息到 Telegram"""
        message = f"✅ 成功:\n{success_message}"
        return self.send_message(message)
    
    def send_warning(self, warning_message):
        """發送警告消息到 Telegram"""
        message = f"⚠️ 警告:\n{warning_message}"
        return self.send_message(message)

# 使用示例
if __name__ == "__main__":
    notifier = TelegramNotifier()
    notifier.send_message("測試消息") 