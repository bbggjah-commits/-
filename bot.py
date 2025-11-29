import http.client
import json
import time
import os

class TelegramBot:
    def __init__(self):
        # 🔑 ضع توكن البوت هنا
        self.token = "8544536572:AAGHDqopyImERuqjciEEKTRSiWsjlhzkX_o"
        self.base_url = "api.telegram.org"
        self.last_update_id = 0
        
        # الكلمات المطلوب تشفيرها
        self.sensitive_words = [
            'بيع', 'شراء', 'مقابل', 'تبديل', 'كردت',
            'عروض', 'سعر', 'متوفر', 'متجر', 'كميه',
            'حساب', 'مطلوب', 'تجار', 'دفع',
            'يبيع', 'تبيع', 'بائع', 'مبيع',
            'يشترى', 'يشتري', 'مشتري', 'شراءات',
            'يعرض', 'العروض', 'عروضات',
            'اسعار', 'أسعار', 'سعرها',
            'التجار', 'تجاري', 'متجري'
        ]
    
    def make_request(self, method, params=None):
        """تنفيذ طلب HTTP"""
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
            print(f"❌ خطأ في الاتصال: {e}")
            return None
    
    def get_updates(self):
        """جلب التحديثات"""
        params = {'offset': self.last_update_id + 1, 'timeout': 30}
        return self.make_request('getUpdates', params)
    
    def send_message(self, chat_id, text, reply_markup=None):
        """إرسال رسالة مع أزرار اختيارية"""
        params = {
            'chat_id': chat_id, 
            'text': text,
            'parse_mode': 'HTML'
        }
        
        if reply_markup:
            params['reply_markup'] = reply_markup
            
        return self.make_request('sendMessage', params)

    def send_photo(self, chat_id, photo_url, caption, reply_markup=None):
        """إرسال صورة"""
        params = {
            'chat_id': chat_id,
            'photo': photo_url,
            'caption': caption,
            'parse_mode': 'HTML'
        }
        
        if reply_markup:
            params['reply_markup'] = reply_markup
            
        return self.make_request('sendPhoto', params)
    
    def delete_message(self, chat_id, message_id):
        """حذف رسالة محددة"""
        params = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        return self.make_request('deleteMessage', params)
    
    def create_main_menu(self):
        """إنشاء قائمة الأزرار الرئيسية"""
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "🛒 سيرفر C7 Shop على الدسكورد",
                        "url": "https://discord.gg/xPqyvTthsa"
                    }
                ],
                [
                    {
                        "text": "🔐 بدأ تشفير الرسائل",
                        "callback_data": "start_encryption"
                    }
                ],
                [
                    {
                        "text": "🗑️ مسح المحادثة",
                        "callback_data": "clear_chat"
                    }
                ]
            ]
        }
        return keyboard
    
    def encrypt_word(self, word):
        """تشفير كلمة واحدة بوضع فاصلة في المنتصف"""
        if len(word) <= 2:
            return word
            
        mid = len(word) // 2
        encrypted = word[:mid] + '،' + word[mid:]
        
        return encrypted
    
    def encrypt_text(self, text):
        """تشفير النص الكامل"""
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
    
    def send_welcome_message(self, chat_id):
        """إرسال رسالة الترحيب مع الصورة والأزرار"""
        photo_url = "http://my-host-imager-production.up.railway.app/uploads/1764431423697-786224292.png"
        caption = """<b>مرحباً بك في بوت تشفير الرسائل! 👋</b>

🤖 <b>هذا البوت مقدم من سيرفر C7 Shop</b>

🎯 <b>المميزات:</b>
• تشفير تلقائي للكلمات الحساسة
• حماية رسائلك من الحذف
• تشفير ذكي وغير ملحوظ

📝 <b>الكلمات المشفرة:</b>
بيع، شراء، سعر، متجر، عروض، كميه، وغيرها...

🔧 <b>الأوامر المتاحة:</b>
• <code>~امسح~</code> - مسح المحادثة

<code>اختر أحد الخيارات أدناه:</code>"""
        
        reply_markup = self.create_main_menu()
        return self.send_photo(chat_id, photo_url, caption, reply_markup)
    
    def send_encryption_instructions(self, chat_id):
        """إرسال تعليمات التشفير"""
        message = """<b>🔐 وضع تشفير الرسائل مفعل</b>

📝 <b>الآن يمكنك كتابة أي رسالة وسأقوم بتشفيرها تلقائياً!</b>

<b>مثال:</b>
<code>أريد بيع هاتف بسعر جيد ومتوفر كميات كبيرة</code>

<b>ستصبح:</b>
<code>أريد بـ،ـيع هاتف بسـ،ـعر جيد ومتـ،ـوفر كـ،ـميات كبيرة</code>

🔧 <b>للمسح:</b> اكتب <code>~امسح~</code>

✍️ <b>اكتب رسالتك الآن:</b>"""
        
        return self.send_message(chat_id, message)
    
    def clear_chat_messages(self, chat_id, user_message_id):
        """محاولة مسح رسائل المحادثة"""
        try:
            # حذف رسالة الأمر الأولى
            self.delete_message(chat_id, user_message_id)
            
            # إرسال رسالة تأكيد ثم حذفها بعد ثواني
            result = self.send_message(chat_id, "🗑️ جاري مسح الرسائل...")
            if result and result.get('ok'):
                time.sleep(2)
                self.delete_message(chat_id, result['result']['message_id'])
            
            # إرسال رسالة نهائية
            self.send_message(chat_id, "✅ تم مسح الرسائل بنجاح!")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في مسح الرسائل: {e}")
            self.send_message(chat_id, "❌ لم أستطع مسح بعض الرسائل")
            return False
    
    def process_message(self, message):
        """معالجة الرسالة"""
        if 'text' in message:
            original_text = message['text']
            chat_id = message['chat']['id']
            message_id = message['message_id']
            
            print(f"📩 رسالة من {message['chat'].get('first_name', 'مستخدم')}: {original_text}")
            
            # ✅ أمر مسح المحادثة
            if original_text.strip() == '~امسح~':
                self.clear_chat_messages(chat_id, message_id)
                return
            
            # إذا كانت رسالة start أو بداية محادثة
            if original_text in ['/start', 'start', 'بدء']:
                self.send_welcome_message(chat_id)
                return
            
            # تشفير الرسالة العادية
            encrypted_text = self.encrypt_text(original_text)
            
            if encrypted_text != original_text:
                response = f"""<b>✅ تم تشفير رسالتك:</b>

<code>{encrypted_text}</code>

🔒 <b>تم تشفير الكلمات الحساسة بنجاح</b>

🔧 <b>للمسح:</b> اكتب <code>~امسح~</code>"""
                self.send_message(chat_id, response)
                print(f"✅ تم تشفير رسالة")
            else:
                # إذا لا توجد كلمات للتشفير
                response = """<b>⚠️ لم أجد كلمات للتشفير</b>

الكلمات المدعومة: بيع، شراء، سعر، متجر، عروض، كميه، إلخ...

<code>جرب كتابة رسالة تحتوي على كلمات حساسة</code>

🔧 <b>للمسح:</b> اكتب <code>~امسح~</code>"""
                self.send_message(chat_id, response)
    
    def process_callback_query(self, callback_query):
        """معالجة النقر على الأزرار"""
        chat_id = callback_query['message']['chat']['id']
        data = callback_query['data']
        
        if data == "start_encryption":
            self.send_encryption_instructions(chat_id)
        elif data == "clear_chat":
            self.send_message(chat_id, "🔧 لمسح المحادثة، اكتب: <code>~امسح~</code>")
    
    def run(self):
        """دالة التشغيل الرئيسية"""
        print("🚀 بدأ تشغيل بوت التشفير مع الواجهة المتقدمة...")
        
        # اختبار البوت
        test = self.make_request('getMe')
        if test and test.get('ok'):
            print(f"✅ البوت نشط: @{test['result']['username']}")
        else:
            print("❌ البوت غير نشط - تحقق من التوكن")
            return
        
        while True:
            try:
                updates = self.get_updates()
                
                if updates and updates.get('ok'):
                    for update in updates['result']:
                        self.last_update_id = update['update_id']
                        
                        # معالجة الرسائل النصية
                        if 'message' in update:
                            self.process_message(update['message'])
                        
                        # معالجة النقر على الأزرار
                        if 'callback_query' in update:
                            self.process_callback_query(update['callback_query'])
                
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ خطأ: {e}")
                time.sleep(10)

# التشغيل الرئيسي
if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
