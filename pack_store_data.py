# -*- coding: utf-8 -*-
import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

# بارگذاری محصولات
from generate_department_data import apparel_men_products, apparel_women_products, gym_gear_products

# استخراج داده‌های قبلی مکمل‌ها
with open("mokamel/index.html", "r", encoding="utf-8") as f:
    old_content = f.read()

# استخراج تابع render3DSupplementSVG
render_svg_match = re.search(r'(function render3DSupplementSVG[\s\S]*?)(?=const supplementsStoreDB)', old_content)
render_svg_code = render_svg_match.group(1).strip() if render_svg_match else ""

# استخراج ۳۵ مکمل
supp_match = re.search(r'const supplementsStoreDB = (\[[\s\S]*?\n\s*\];)', old_content)
supp_json_code = supp_match.group(1).strip() if supp_match else "[]"

# تولید کد جاوااسکریپت محصولات مکمل با department: "supplements"
supp_json_code = re.sub(r'(id:\s*"[^"]+",)', r'\1\n                department: "supplements",', supp_json_code)

men_json = json.dumps(apparel_men_products, ensure_ascii=False, indent=12)
women_json = json.dumps(apparel_women_products, ensure_ascii=False, indent=12)
gear_json = json.dumps(gym_gear_products, ensure_ascii=False, indent=12)

# ساخت کل فایل mokamel/index.html
with open("assemble_megastore.py", "w", encoding="utf-8") as f:
    f.write(f'''# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

supplements_code = """{supp_json_code}"""
men_code = """{men_json}"""
women_code = """{women_json}"""
gear_code = """{gear_json}"""
render_svg_func = """{render_svg_code}"""

print("Data packed ready for write.")
''')

print("Created data packing script.")
