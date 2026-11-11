# -*- coding: utf-8 -*-
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

# بارگذاری محصولات مکمل‌ها
with open("supplements_clean.json", "r", encoding="utf-8") as f:
    supplements_data = json.load(f)

# اطمینان از department: "supplements"
for s in supplements_data:
    s["department"] = "supplements"

# بارگذاری پوشاک و تجهیزات
from generate_department_data import apparel_men_products, apparel_women_products, gym_gear_products

supp_json_str = json.dumps(supplements_data, ensure_ascii=False, indent=8)
men_json_str = json.dumps(apparel_men_products, ensure_ascii=False, indent=8)
women_json_str = json.dumps(apparel_women_products, ensure_ascii=False, indent=8)
gear_json_str = json.dumps(gym_gear_products, ensure_ascii=False, indent=8)

# خواندن قالب اصلی تا اسکریپت
with open("generate_complete_app.py", "r", encoding="utf-8") as f:
    code = f.read()

# جایگزینی بخش داده‌ها
# در generate_complete_app.py خطوط مربوط به old_content را برمی‌داریم
