# -*- coding: utf-8 -*-
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

# بارگذاری داده‌های محصولات
from generate_department_data import apparel_men_products, apparel_women_products, gym_gear_products

# استخراج کدهای قبلی ۳۵ مکمل
with open("mokamel/index.html", "r", encoding="utf-8") as f:
    old_content = f.read()

# استخراج تابع render3DSupplementSVG
render_svg_match = re.search(r'(function render3DSupplementSVG[\s\S]*?)(?=const supplementsStoreDB)', old_content)
render_svg_code = render_svg_match.group(1) if render_svg_match else ""

# استخراج ۳۵ مکمل
supp_match = re.search(r'const supplementsStoreDB = (\[[\s\S]*?\n\s*\];)', old_content)
supp_json_code = supp_match.group(1) if supp_match else "[]"

# تبدیل به آرایه در پایتون با اجرای یک خط پایتون یا ریجکس
# برای سادگی در جاوااسکریپت:
# const fullStoreDB = [
#    ...supplementsStoreDB.map(s => ({ ...s, department: "supplements" })),
#    ...apparelMenDB,
#    ...apparelWomenDB,
#    ...gymGearDB
# ];

print("Extracted render3DSupplementSVG and supplements data.")
