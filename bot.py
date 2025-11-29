import http.client
import json
import time
import os

class TelegramBot:
    def __init__(self):
        # ضع التوكن هنا مباشرة (للتجربة)
        self.token = "8544536572:AAGHDqopyImERuqjciEEKTRSiWsjlhzkX_o"
        self.base_url = "api.telegram.org"
        self.last_update_id = 0
        
        self.sensitive_words = ['بيع', 'شراء', 'مقابل', 'تبديل', 'كردت', 'عروض', 'سعر', 'متوفر', 'متجر', 'كميه', 'حساب', 'مطلوب', 'تجار', 'دفع']
    
    # ... باقي الكود بدون تغيير ...

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
