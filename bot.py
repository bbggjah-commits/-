import http.client
import json
import time
import os

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.base_url = "api.telegram.org"
        self.last_update_id = 0
        
        self.sensitive_words = [
            'بيع', 'شراء', 'مقابل', 'تبديل', 'كردت',
            'عروض', 'سعر', 'متوفر', 'متجر', 'كميه',
            'حساب', 'مطلوب', 'تجار', 'دفع'
        ]
    
    def make_request(self, method, params=None):
        try:
            conn = http.client.HTTPSConnection(self.base_url)
            url = f"/bot{self.token}/{method}"
            
            if params:
                body = json.dumps(params)
                headers = {'Content-Type': 'application/json'}
                conn.request("POST", url, body, headers)
            else:
                conn.request("GET", url)
            
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            conn.close()
            return json.loads(data)
        except Exception as e:
            print(f"❌ خطأ: {e}")
            return None
    
    def get_updates(self):
        params = {'offset': self.last_update_id + 1, 'timeout': 30}
        return self.make_request('getUpdates', params)
    
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        return self.make_request('sendMessage', params)
    
    def encrypt_word(self, word):
        if len(word) <= 2:
            return word
        mid = len(word) // 2
        return word[:mid] + '،' + word[mid:]
    
    def encrypt_text(self, text):
        words = text.split()
        encrypted_words = []
        
        for word in words:
            clean_word = ''.join(char for char in word if char.isalnum())
            
            if clean_word.lower() in [w.lower() for w in self.sensitive_words]:
                encrypted_word = self.encrypt_word(clean_word)
                if word != clean_word:
                    encrypted_word = encrypted_word + word[len(clean_word):]
                encrypted_words.append(encrypted_word)
            else:
                encrypted_words.append(word)
        
        return ' '.join(encrypted_words)
    
    def process_message(self, message):
        if 'text' in message:
            original_text = message['text']
            chat_id = message['chat']['id']
            
            print(f"📩 رسالة: {original_text}")
            
            encrypted_text = self.encrypt_text(original_text)
            
            if encrypted_text != original_text:
                response = f"🔐 الرسالة المشفرة:\n{encrypted_text}"
                self.send_message(chat_id, response)
                print(f"✅ تم إرسال النص المشفر")
    
    def run(self):
        print("🚀 بدأ تشغيل البوت على GitHub...")
        
        while True:
            try:
                updates = self.get_updates()
                
                if updates and updates.get('ok'):
                    for update in updates['result']:
                        self.last_update_id = update['update_id']
                        if 'message' in update:
                            self.process_message(update['message'])
                
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ خطأ: {e}")
                time.sleep(10)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
