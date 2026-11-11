# -*- coding: utf-8 -*-
import os
import shutil

products_dir = "images/products"
mokamel_products_dir = "mokamel/images/products"
os.makedirs(products_dir, exist_ok=True)
os.makedirs(mokamel_products_dir, exist_ok=True)

def generate_tub_svg(cfg):
    """
    تولید فایل وکتور تصویری فوق‌العاده با کیفیت و دقیق برای انواع قوطی، سطل، قوطی قرص و کیسه مکمل
    """
    shape = cfg.get("shape", "tub") # tub, bucket, pill, pouch
    pid = cfg["id"]
    main_color = cfg["main_color"]
    label_bg = cfg["label_bg"]
    accent_color = cfg["accent_color"]
    text_color = cfg.get("text_color", "#ffffff")
    brand_text = cfg["brand_text"]
    title_en = cfg["title_en"]
    sub_title = cfg.get("sub_title", "")
    badge_text = cfg.get("badge_text", "100% ORIGINAL")
    cap_color = cfg.get("cap_color", "#18181b")
    spec_text = cfg.get("spec_text", "")
    glow_color = cfg.get("glow_color", accent_color)

    svg = f'''<svg viewBox="0 0 300 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="shadow_{pid}" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#000000" flood-opacity="0.8"/>
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="{glow_color}" flood-opacity="0.25"/>
    </filter>
    <linearGradient id="bodyGrad_{pid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{main_color}" stop-opacity="0.9"/>
      <stop offset="18%" stop-color="#ffffff" stop-opacity="0.35"/>
      <stop offset="38%" stop-color="{main_color}"/>
      <stop offset="75%" stop-color="#070a12"/>
      <stop offset="100%" stop-color="#020408"/>
    </linearGradient>
    <linearGradient id="capGrad_{pid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{cap_color}"/>
      <stop offset="25%" stop-color="#ffffff" stop-opacity="0.4"/>
      <stop offset="50%" stop-color="{cap_color}"/>
      <stop offset="85%" stop-color="#090d16"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>
    <linearGradient id="labelGrad_{pid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{label_bg}"/>
      <stop offset="30%" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="70%" stop-color="{label_bg}"/>
      <stop offset="100%" stop-color="#05070d"/>
    </linearGradient>
    <radialGradient id="highlight_{pid}" cx="40%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- سایه بیضی کف محصول -->
  <ellipse cx="150" cy="335" rx="90" ry="16" fill="#000000" opacity="0.6" filter="url(#shadow_{pid})"/>
'''

    if shape == "pouch": # کیسه ایستاده مانند مای پروتئین
        svg += f'''
  <!-- بدنه کیسه ایستاده -->
  <g filter="url(#shadow_{pid})">
    <path d="M75,90 L225,90 L240,320 L60,320 Z" fill="url(#bodyGrad_{pid})"/>
    <path d="M75,90 Q150,75 225,90 L230,110 L70,110 Z" fill="{cap_color}"/>
    <!-- خط زیپ کیپ -->
    <line x1="72" y1="102" x2="228" y2="102" stroke="#ffffff" stroke-width="2" stroke-dasharray="4,2" opacity="0.6"/>
    <!-- لیبل روی کیسه -->
    <rect x="75" y="125" width="150" height="175" rx="8" fill="url(#labelGrad_{pid})" stroke="{accent_color}" stroke-width="1.5"/>
    <rect x="75" y="125" width="150" height="12" fill="{accent_color}"/>
    <!-- متن‌ها -->
    <text x="150" y="160" font-size="16" font-weight="900" fill="{accent_color}" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="1.5">{brand_text}</text>
    <line x1="95" y1="170" x2="205" y2="170" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
    <text x="150" y="200" font-size="18" font-weight="900" fill="{text_color}" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif">{title_en}</text>
    <text x="150" y="222" font-size="12" font-weight="700" fill="{accent_color}" text-anchor="middle" font-family="sans-serif">{sub_title}</text>
    <rect x="90" y="238" width="120" height="24" rx="4" fill="{accent_color}" opacity="0.9"/>
    <text x="150" y="254" font-size="11" font-weight="900" fill="#000000" text-anchor="middle" font-family="sans-serif">{badge_text}</text>
    <text x="150" y="284" font-size="11" font-weight="800" fill="#94a3b8" text-anchor="middle" font-family="sans-serif">{spec_text}</text>
  </g>
'''
    elif shape == "bucket": # سطل بزرگ گینر مس
        svg += f'''
  <!-- سطل بزرگ مس ۵ کیلویی -->
  <g filter="url(#shadow_{pid})">
    <!-- دسته سطل -->
    <path d="M50,110 C50,25 250,25 250,110" fill="none" stroke="#64748b" stroke-width="6" stroke-linecap="round"/>
    <circle cx="50" cy="110" r="8" fill="#334155"/>
    <circle cx="250" cy="110" r="8" fill="#334155"/>
    <!-- درپوش لبه‌دار سطل -->
    <ellipse cx="150" cy="85" rx="100" ry="22" fill="url(#capGrad_{pid})"/>
    <rect x="50" y="85" width="200" height="26" fill="url(#capGrad_{pid})"/>
    <ellipse cx="150" cy="111" rx="100" ry="18" fill="url(#capGrad_{pid})" stroke="#000000" stroke-width="1"/>
    <!-- بدنه مخروطی سطل -->
    <path d="M52,110 L68,325 Q150,345 232,325 L248,110 Z" fill="url(#bodyGrad_{pid})"/>
    <!-- هایلایت روی بدنه -->
    <path d="M68,115 L78,320 Q110,330 130,328 L115,115 Z" fill="url(#highlight_{pid})"/>
    <!-- لیبل بزرگ سطل -->
    <path d="M60,135 L70,305 Q150,325 230,305 L240,135 Z" fill="url(#labelGrad_{pid})" stroke="{accent_color}" stroke-width="2"/>
    <rect x="63" y="140" width="174" height="15" fill="{accent_color}"/>
    <!-- محتوای لیبل -->
    <text x="150" y="180" font-size="18" font-weight="900" fill="{accent_color}" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="2">{brand_text}</text>
    <line x1="85" y1="192" x2="215" y2="192" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <text x="150" y="224" font-size="20" font-weight="900" fill="{text_color}" text-anchor="middle" font-family="Arial Black, Impact, sans-serif">{title_en}</text>
    <text x="150" y="248" font-size="14" font-weight="800" fill="{accent_color}" text-anchor="middle" font-family="sans-serif">{sub_title}</text>
    <rect x="85" y="262" width="130" height="26" rx="5" fill="{accent_color}"/>
    <text x="150" y="280" font-size="12" font-weight="900" fill="#000000" text-anchor="middle" font-family="sans-serif">{badge_text}</text>
    <text x="150" y="302" font-size="11" font-weight="800" fill="#cbd5e1" text-anchor="middle" font-family="sans-serif">{spec_text}</text>
  </g>
'''
    elif shape == "pill": # قوطی قرص و کپسول (استوانه‌ای کشیده‌تر با درپوش پیچی شیاردار)
        svg += f'''
  <!-- قوطی قرص / کپسول -->
  <g filter="url(#shadow_{pid})">
    <!-- درپوش پیچی شیاردار -->
    <rect x="100" y="48" width="100" height="38" rx="6" fill="url(#capGrad_{pid})"/>
    <ellipse cx="150" cy="48" rx="50" ry="12" fill="url(#capGrad_{pid})"/>
    <!-- شیارهای روی درپوش -->
    <line x1="110" y1="56" x2="110" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <line x1="120" y1="56" x2="120" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <line x1="130" y1="56" x2="130" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <line x1="140" y1="56" x2="140" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <line x1="150" y1="56" x2="150" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <line x1="160" y1="56" x2="160" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <line x1="170" y1="56" x2="170" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <line x1="180" y1="56" x2="180" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <line x1="190" y1="56" x2="190" y2="80" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <!-- گردن قوطی -->
    <rect x="108" y="84" width="84" height="14" fill="#090d16"/>
    <!-- شانه و بدنه قوطی قرص -->
    <path d="M108,98 C80,105 70,125 70,145 L70,305 Q150,330 230,305 L230,145 C230,125 220,105 192,98 Z" fill="url(#bodyGrad_{pid})"/>
    <!-- هایلایت شیشه‌ای / براق -->
    <path d="M80,135 L80,295 Q105,305 115,295 L115,135 Z" fill="url(#highlight_{pid})"/>
    <!-- برچسب دور قوطی -->
    <rect x="70" y="140" width="160" height="155" fill="url(#labelGrad_{pid})" stroke="{accent_color}" stroke-width="1.5"/>
    <rect x="70" y="140" width="160" height="10" fill="{accent_color}"/>
    <!-- متن‌های لیبل -->
    <text x="150" y="170" font-size="14" font-weight="900" fill="{accent_color}" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="1">{brand_text}</text>
    <line x1="90" y1="180" x2="210" y2="180" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
    <text x="150" y="210" font-size="16" font-weight="900" fill="{text_color}" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif">{title_en}</text>
    <text x="150" y="230" font-size="12" font-weight="700" fill="{accent_color}" text-anchor="middle" font-family="sans-serif">{sub_title}</text>
    <!-- قرص / کپسول گرافیکی کوچک روی لیبل -->
    <g transform="translate(150, 248)">
      <rect x="-18" y="-6" width="18" height="12" rx="6" fill="{accent_color}"/>
      <rect x="0" y="-6" width="18" height="12" rx="6" fill="#ffffff"/>
    </g>
    <rect x="85" y="260" width="130" height="20" rx="4" fill="{accent_color}" opacity="0.95"/>
    <text x="150" y="274" font-size="10.5" font-weight="900" fill="#000000" text-anchor="middle" font-family="sans-serif">{badge_text}</text>
    <text x="150" y="292" font-size="9.5" font-weight="800" fill="#94a3b8" text-anchor="middle" font-family="sans-serif">{spec_text}</text>
  </g>
'''
    else: # tub: قوطی استاندارد ۲ کیلویی پروتئین وی و کراتین
        svg += f'''
  <!-- قوطی پودر استاندارد ۲ پوند تا ۵ پوند -->
  <g filter="url(#shadow_{pid})">
    <!-- درپوش عریض و شیاردار -->
    <rect x="82" y="44" width="136" height="36" rx="6" fill="url(#capGrad_{pid})"/>
    <ellipse cx="150" cy="44" rx="68" ry="14" fill="url(#capGrad_{pid})"/>
    <!-- شیارهای روی درپوش -->
    <line x1="95" y1="50" x2="95" y2="76" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <line x1="108" y1="50" x2="108" y2="76" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <line x1="122" y1="50" x2="122" y2="76" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <line x1="136" y1="50" x2="136" y2="76" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <line x1="150" y1="50" x2="150" y2="76" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <line x1="164" y1="50" x2="164" y2="76" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <line x1="178" y1="50" x2="178" y2="76" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <line x1="192" y1="50" x2="192" y2="76" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <line x1="205" y1="50" x2="205" y2="76" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
    <!-- گردن قوطی -->
    <rect x="92" y="78" width="116" height="12" fill="#080c14"/>
    <!-- شانه و بدنه عضلانی قوطی -->
    <path d="M92,90 C60,98 50,118 50,140 L50,305 Q150,335 250,305 L250,140 C250,118 240,98 208,90 Z" fill="url(#bodyGrad_{pid})"/>
    <!-- بازتاب نور شیشه/پلاستیک براق روی شانه و چپ بدنه -->
    <path d="M62,115 L62,298 Q90,315 105,305 L105,115 Z" fill="url(#highlight_{pid})"/>
    <!-- برچسب لیبل سراسری قوطی -->
    <rect x="50" y="130" width="200" height="165" fill="url(#labelGrad_{pid})" stroke="{accent_color}" stroke-width="1.5"/>
    <rect x="50" y="130" width="200" height="12" fill="{accent_color}"/>
    <!-- متن‌های لیبل -->
    <text x="150" y="165" font-size="16" font-weight="900" fill="{accent_color}" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="2">{brand_text}</text>
    <line x1="75" y1="176" x2="225" y2="176" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
    <text x="150" y="208" font-size="19" font-weight="900" fill="{text_color}" text-anchor="middle" font-family="'Segoe UI', Roboto, Arial Black, sans-serif">{title_en}</text>
    <text x="150" y="232" font-size="13" font-weight="800" fill="{accent_color}" text-anchor="middle" font-family="sans-serif">{sub_title}</text>
    <!-- روبان تاییدیه اورجینال -->
    <rect x="75" y="248" width="150" height="24" rx="4" fill="{accent_color}"/>
    <text x="150" y="264" font-size="11" font-weight="900" fill="#000000" text-anchor="middle" font-family="sans-serif" letter-spacing="1">{badge_text}</text>
    <text x="150" y="288" font-size="11" font-weight="800" fill="#94a3b8" text-anchor="middle" font-family="sans-serif">{spec_text}</text>
  </g>
'''

    svg += "</svg>"
    return svg

# لیست مشخصات ۳۵ محصول
products_catalog = [
    # ۱. پروتئین بیف
    {
        "id": "carnivor-beef-2000",
        "shape": "tub",
        "main_color": "#450a0a",
        "label_bg": "#1c0404",
        "accent_color": "#dc2626",
        "cap_color": "#18181b",
        "brand_text": "CARNIVOR",
        "title_en": "BEEF PROTEIN",
        "sub_title": "ISOLATE 99% PURE",
        "badge_text": "350% MORE AMINOS",
        "spec_text": "ZERO FAT • ZERO LACTOSE"
    },
    # ۲. آلبومین تخم مرغ ژن استار
    {
        "id": "genestar-egg-albumin-2000",
        "shape": "tub",
        "main_color": "#18181b",
        "label_bg": "#090d16",
        "accent_color": "#f59e0b",
        "cap_color": "#d97706",
        "brand_text": "GENESTAR",
        "title_en": "EGG ALBUMIN",
        "sub_title": "PURE EGG WHITE PROTEIN",
        "badge_text": "BIOLOGICAL VALUE 100",
        "spec_text": "2000g • RICH IN BCAAs"
    },
    # ۳. آلبومین دوبیس
    {
        "id": "doobis-egg-albumin-1000",
        "shape": "tub",
        "main_color": "#4c1d95",
        "label_bg": "#2e1065",
        "accent_color": "#facc15",
        "cap_color": "#ca8a04",
        "brand_text": "DOOBIS",
        "title_en": "EGG PROTEIN",
        "sub_title": "PASTEURIZED ALBUMIN",
        "badge_text": "CHOLESTEROL FREE",
        "spec_text": "1000g • SUSTAINED RELEASE"
    },
    # ۴. وگان ویتاپی
    {
        "id": "vitap-vegan-protein-1000",
        "shape": "tub",
        "main_color": "#064e3b",
        "label_bg": "#022c22",
        "accent_color": "#34d399",
        "cap_color": "#f8fafc",
        "brand_text": "VITAP FIT",
        "title_en": "VEGAN PROTEIN",
        "sub_title": "PEA & SOY BLEND",
        "badge_text": "100% PLANT BASED",
        "spec_text": "DAIRY FREE • ORGANIC"
    },
    # ۵. سینتا ۶ بی اس ان
    {
        "id": "bsn-syntha6-2270",
        "shape": "tub",
        "main_color": "#7f1d1d",
        "label_bg": "#450a0a",
        "accent_color": "#ef4444",
        "cap_color": "#18181b",
        "brand_text": "BSN",
        "title_en": "SYNTHA-6",
        "sub_title": "ULTRA-PREMIUM PROTEIN",
        "badge_text": "22G PROTEIN MATRIX",
        "spec_text": "2.27KG • RIDICULOUS TASTE"
    },
    # ۶. وی ایزوله کاله
    {
        "id": "kalleh-isolate-650",
        "shape": "tub",
        "main_color": "#0284c7",
        "label_bg": "#082f49",
        "accent_color": "#38bdf8",
        "cap_color": "#ffffff",
        "brand_text": "KALLEH PRO",
        "title_en": "WHEY ISOLATE 90%",
        "sub_title": "ULTRA FILTERED PURE",
        "badge_text": "SUGAR FREE • ZERO FAT",
        "spec_text": "650g • RAPID ABSORPTION"
    },
    # ۷. وی ۱۰۰٪ کاله
    {
        "id": "kalleh-whey-650",
        "shape": "tub",
        "main_color": "#0369a1",
        "label_bg": "#0c203a",
        "accent_color": "#dc2626",
        "cap_color": "#18181b",
        "brand_text": "KALLEH PRO",
        "title_en": "100% WHEY CONCENTRATE",
        "sub_title": "NATURAL HIGH AMINO",
        "badge_text": "PRO ATHLETE CHOICE",
        "spec_text": "650g • 24G PROTEIN"
    },
    # ۸. ایزو ۱۰۰ دایماتیز
    {
        "id": "dymatize-iso-100-2270",
        "shape": "tub",
        "main_color": "#0f172a",
        "label_bg": "#020617",
        "accent_color": "#0284c7",
        "cap_color": "#0284c7",
        "brand_text": "DYMATIZE",
        "title_en": "ISO•100 HYDROLYZED",
        "sub_title": "100% WHEY ISOLATE",
        "badge_text": "AWARD WINNING TASTE",
        "spec_text": "5.5G BCAAs • 2.27KG"
    },
    # ۹. وی گلد اپتیموم ON
    {
        "id": "on-gold-whey-2270",
        "shape": "tub",
        "main_color": "#18181b",
        "label_bg": "#000000",
        "accent_color": "#f59e0b",
        "cap_color": "#000000",
        "brand_text": "OPTIMUM NUTRITION",
        "title_en": "GOLD STANDARD WHEY",
        "sub_title": "100% WHEY PROTEIN",
        "badge_text": "WORLD'S #1 PROTEIN",
        "spec_text": "24G PROTEIN • 2.27KG"
    },
    # ۱۰. کازئین گلد ON
    {
        "id": "on-casein-1800",
        "shape": "tub",
        "main_color": "#18181b",
        "label_bg": "#090d16",
        "accent_color": "#eab308",
        "cap_color": "#000000",
        "brand_text": "OPTIMUM NUTRITION",
        "title_en": "100% CASEIN GOLD",
        "sub_title": "SLOW DIGESTING PROTEIN",
        "badge_text": "OVERNIGHT RECOVERY",
        "spec_text": "24G MICELLAR CASEIN"
    },
    # ۱۱. پیور وی کارن PNC
    {
        "id": "pnc-pure-whey-2270",
        "shape": "tub",
        "main_color": "#334155",
        "label_bg": "#0f172a",
        "accent_color": "#dc2626",
        "cap_color": "#b91c1c",
        "brand_text": "KAREN PHARMA",
        "title_en": "PURE WHEY PNC",
        "sub_title": "PREMIUM PROTEIN MATRIX",
        "badge_text": "PHARMACEUTICAL GRADE",
        "spec_text": "2270g • HIGH BCAA & GLUTAMINE"
    },
    # ۱۲. سوپر مس کارن (سطل ۵ کیلویی)
    {
        "id": "pnc-super-mass-5000",
        "shape": "bucket",
        "main_color": "#1e293b",
        "label_bg": "#0f172a",
        "accent_color": "#dc2626",
        "cap_color": "#b91c1c",
        "brand_text": "KAREN (PNC)",
        "title_en": "SUPER MASS GAINER",
        "sub_title": "HIGH CALORIE WEIGHT GAIN",
        "badge_text": "5000 GRAM BUCKET",
        "spec_text": "COMPLEX CARB & PROTEIN"
    },
    # ۱۳. سریوس مس اپتیموم
    {
        "id": "on-serious-mass-5400",
        "shape": "bucket",
        "main_color": "#090d16",
        "label_bg": "#000000",
        "accent_color": "#84cc16",
        "cap_color": "#18181b",
        "brand_text": "OPTIMUM NUTRITION",
        "title_en": "SERIOUS MASS",
        "sub_title": "HIGH PROTEIN WEIGHT GAIN",
        "badge_text": "1250 CALORIES • 50G PRO",
        "spec_text": "5.44KG BUCKET • 25 VITAMINS"
    },
    # ۱۴. کربو کارن
    {
        "id": "pnc-carbo-2000",
        "shape": "tub",
        "main_color": "#0284c7",
        "label_bg": "#075985",
        "accent_color": "#38bdf8",
        "cap_color": "#ffffff",
        "brand_text": "KAREN PHARMA",
        "title_en": "PURE CARBO PNC",
        "sub_title": "GLYCOGEN REPLENISHMENT",
        "badge_text": "100% COMPLEX CARB",
        "spec_text": "2000g • RAPID ENERGY"
    },
    # ۱۵. گلد لین مس کوین لورون
    {
        "id": "levrone-gold-lean-mass-3000",
        "shape": "tub",
        "main_color": "#0a0e17",
        "label_bg": "#020408",
        "accent_color": "#fbbf24",
        "cap_color": "#d97706",
        "brand_text": "KEVIN LEVRONE",
        "title_en": "GOLD LEAN MASS",
        "sub_title": "LEAN MUSCLE BUILDER",
        "badge_text": "SIGNATURE SERIES",
        "spec_text": "3000g • DAA & FENUGREEK"
    },
    # ۱۶. کراتین بتا آلانین دوبیس
    {
        "id": "doobis-creatine-beta-300",
        "shape": "tub",
        "main_color": "#3b0764",
        "label_bg": "#1e1b4b",
        "accent_color": "#38bdf8",
        "cap_color": "#6366f1",
        "brand_text": "DOOBIS",
        "title_en": "CREATINE + BETA",
        "sub_title": "EXPLOSIVE POWER & STAMINA",
        "badge_text": "300g ULTRA MICRONIZED",
        "spec_text": "ZERO FATIGUE FORMULA"
    },
    # ۱۷. کراتین میکرونایزد کارن
    {
        "id": "pnc-creatine-300",
        "shape": "tub",
        "main_color": "#e2e8f0",
        "label_bg": "#f8fafc",
        "accent_color": "#dc2626",
        "text_color": "#0f172a",
        "cap_color": "#dc2626",
        "brand_text": "KAREN (PNC)",
        "title_en": "CREATINE MONOHYDRATE",
        "sub_title": "PHARMACEUTICAL HPLC PURE",
        "badge_text": "100% MICRONIZED 300G",
        "spec_text": "STRENGTH & ATP BOOSTER"
    },
    # ۱۸. سل تک ماسل تک
    {
        "id": "muscletech-celltech-2700",
        "shape": "tub",
        "main_color": "#1e293b",
        "label_bg": "#0f172a",
        "accent_color": "#06b6d4",
        "cap_color": "#0ea5e9",
        "brand_text": "MUSCLETECH",
        "title_en": "CELL-TECH ELITE",
        "sub_title": "ADVANCED CREATINE FORMULA",
        "badge_text": "MOST POWERFUL CREATINE",
        "spec_text": "2700g • CLINICAL DOSES"
    },
    # ۱۹. کریپیور مای پروتئین (کیسه Pouch)
    {
        "id": "myprotein-creapure-500",
        "shape": "pouch",
        "main_color": "#0284c7",
        "label_bg": "#0369a1",
        "accent_color": "#38bdf8",
        "cap_color": "#0284c7",
        "brand_text": "MYPROTEIN",
        "title_en": "CREAPURE® CREATINE",
        "sub_title": "GERMAN HIGHEST PURITY",
        "badge_text": "99.99% ULTRA PURE",
        "spec_text": "500g • UNFLAVOURED"
    },
    # ۲۰. آرژنین ۱۰۰۰ کارن (قوطی قرص)
    {
        "id": "pnc-arginine-1000",
        "shape": "pill",
        "main_color": "#f1f5f9",
        "label_bg": "#ffffff",
        "accent_color": "#dc2626",
        "text_color": "#0f172a",
        "cap_color": "#b91c1c",
        "brand_text": "KAREN (PNC)",
        "title_en": "L-ARGININE 1000",
        "sub_title": "NITRIC OXIDE PUMP",
        "badge_text": "100 TABLETS • 1000MG",
        "spec_text": "VASODILATION & FLOW"
    },
    # ۲۱. آمینو وی دوبیس
    {
        "id": "doobis-amino-whey-300",
        "shape": "pill",
        "main_color": "#2e1065",
        "label_bg": "#1e1b4b",
        "accent_color": "#a855f7",
        "cap_color": "#4c1d95",
        "brand_text": "DOOBIS",
        "title_en": "AMINO WHEY 300",
        "sub_title": "100% WHEY HYDROLYZATE",
        "badge_text": "300 TABLETS",
        "spec_text": "MUSCLE RECOVERY & GROWTH"
    },
    # ۲۲. بی سی ای ای کارن
    {
        "id": "pnc-bcaa-300",
        "shape": "tub",
        "main_color": "#0f172a",
        "label_bg": "#020617",
        "accent_color": "#ef4444",
        "cap_color": "#b91c1c",
        "brand_text": "KAREN (PNC)",
        "title_en": "BCAA 2:1:1 POWDER",
        "sub_title": "BRANCHED CHAIN AMINOS",
        "badge_text": "300 GRAMS PURE",
        "spec_text": "ANTI-CATABOLIC MATRIX"
    },
    # ۲۳. گلوتامین ژن استار
    {
        "id": "genestar-pure-glutamine-300",
        "shape": "tub",
        "main_color": "#18181b",
        "label_bg": "#090d16",
        "accent_color": "#eab308",
        "cap_color": "#ca8a04",
        "brand_text": "GENESTAR",
        "title_en": "100% L-GLUTAMINE",
        "sub_title": "MICRO INTRA-WORKOUT",
        "badge_text": "IMMUNITY & CELL VOLUMIZER",
        "spec_text": "300g MICRONIZED"
    },
    # ۲۴. اچ ام بی کارن (قوطی قرص)
    {
        "id": "pnc-hmb-120",
        "shape": "pill",
        "main_color": "#1e293b",
        "label_bg": "#0f172a",
        "accent_color": "#f97316",
        "cap_color": "#334155",
        "brand_text": "KAREN (PNC)",
        "title_en": "HMB 1000 CAPS",
        "sub_title": "LEUCINE METABOLITE",
        "badge_text": "120 CAPSULES",
        "spec_text": "STOPS MUSCLE BREAKDOWN"
    },
    # ۲۵. بتا آلانین کارن
    {
        "id": "pnc-beta-alanine-300",
        "shape": "tub",
        "main_color": "#1e293b",
        "label_bg": "#0f172a",
        "accent_color": "#eab308",
        "cap_color": "#ca8a04",
        "brand_text": "KAREN (PNC)",
        "title_en": "BETA-ALANINE CARNOSYN",
        "sub_title": "CARNOSINE BUFFER",
        "badge_text": "300g ULTRA FINE",
        "spec_text": "DELAYS MUSCLE BURNOUT"
    },
    # ۲۶. سیترولین ژن استار
    {
        "id": "genestar-citrulline-300",
        "shape": "tub",
        "main_color": "#18181b",
        "label_bg": "#090d16",
        "accent_color": "#f43f5e",
        "cap_color": "#e11d48",
        "brand_text": "GENESTAR",
        "title_en": "CITRULLINE MALATE 2:1",
        "sub_title": "NITRIC OXIDE SURGE",
        "badge_text": "300 GRAMS PURE",
        "spec_text": "MAXIMUM BLOOD FLOW PUMP"
    },
    # ۲۷. کافئین کارن (قوطی قرص)
    {
        "id": "pnc-caffeine-200",
        "shape": "pill",
        "main_color": "#78350f",
        "label_bg": "#451a03",
        "accent_color": "#d97706",
        "cap_color": "#78350f",
        "brand_text": "KAREN (PNC)",
        "title_en": "CAFFEINE 200MG",
        "sub_title": "ANHYDROUS PURE PHARMA",
        "badge_text": "60 TABLETS",
        "spec_text": "FOCUS & METABOLISM"
    },
    # ۲۸. پمپ سی ۴ سلوکور
    {
        "id": "cellucor-c4-180",
        "shape": "tub",
        "main_color": "#000000",
        "label_bg": "#000000",
        "accent_color": "#eab308",
        "cap_color": "#eab308",
        "brand_text": "CELLUCOR",
        "title_en": "C4 ORIGINAL PUMP",
        "sub_title": "EXPLOSIVE PRE-WORKOUT",
        "badge_text": "30 SERVINGS • 180G",
        "spec_text": "ENERGY & FOCUS PUMP"
    },
    # ۲۹. ال کارنیتین کارن (قوطی قرص)
    {
        "id": "pnc-l-carnitine-100",
        "shape": "pill",
        "main_color": "#047857",
        "label_bg": "#064e3b",
        "accent_color": "#34d399",
        "cap_color": "#047857",
        "brand_text": "KAREN (PNC)",
        "title_en": "L-CARNITINE 1000",
        "sub_title": "FAT CONVERTER TO ENERGY",
        "badge_text": "100 TABLETS",
        "spec_text": "CARDIO & ENDURANCE"
    },
    # ۳۰. سی ال ای ژن استار (قوطی قرص)
    {
        "id": "genestar-cla-1000",
        "shape": "pill",
        "main_color": "#78350f",
        "label_bg": "#451a03",
        "accent_color": "#fbbf24",
        "cap_color": "#d97706",
        "brand_text": "GENESTAR",
        "title_en": "CLA 1000MG SOFTGELS",
        "sub_title": "CONJUGATED LINOLEIC",
        "badge_text": "90 SOFTGELS",
        "spec_text": "TARGET ABDOMINAL FAT"
    },
    # ۳۱. هیدروکسی کات الیت ماسل تک
    {
        "id": "muscletech-hydroxycut-110",
        "shape": "pill",
        "main_color": "#450a0a",
        "label_bg": "#1c0404",
        "accent_color": "#ef4444",
        "cap_color": "#18181b",
        "brand_text": "MUSCLETECH",
        "title_en": "HYDROXYCUT ELITE",
        "sub_title": "HARDCORE THERMOGENIC",
        "badge_text": "110 RAPID CAPS",
        "spec_text": "INTENSE WEIGHT LOSS"
    },
    # ۳۲. زد ام ای کارن (قوطی قرص)
    {
        "id": "pnc-zma-60",
        "shape": "pill",
        "main_color": "#1e3a8a",
        "label_bg": "#0f172a",
        "accent_color": "#60a5fa",
        "cap_color": "#1e3a8a",
        "brand_text": "KAREN (PNC)",
        "title_en": "ZMA COMPLEX",
        "sub_title": "ZINC, MAGNESIUM & B6",
        "badge_text": "60 CAPSULES",
        "spec_text": "DEEP SLEEP & TESTOSTERONE"
    },
    # ۳۳. تریبولوس ژن استار (قوطی قرص)
    {
        "id": "genestar-tribulus-650",
        "shape": "pill",
        "main_color": "#14532d",
        "label_bg": "#052e16",
        "accent_color": "#86efac",
        "cap_color": "#166534",
        "brand_text": "GENESTAR",
        "title_en": "TRIBULUS 650MG",
        "sub_title": "STANDARDIZED SAPONINS",
        "badge_text": "90 CAPSULES",
        "spec_text": "NATURAL TESTOSTERONE SUPPORT"
    },
    # ۳۴. آلفا لیپوئیک اسید ALA (قوطی قرص)
    {
        "id": "ala-300-pure",
        "shape": "pill",
        "main_color": "#581c87",
        "label_bg": "#3b0764",
        "accent_color": "#c084fc",
        "cap_color": "#581c87",
        "brand_text": "KAREN PHARMA",
        "title_en": "ALA 300MG PURE",
        "sub_title": "UNIVERSAL ANTIOXIDANT",
        "badge_text": "60 CAPSULES",
        "spec_text": "INSULIN & RECOVERY SENSITIVITY"
    },
    # ۳۵. مولتی ویتامین دیلی ویتاپی (قوطی قرص)
    {
        "id": "vitap-daily-multi-60",
        "shape": "pill",
        "main_color": "#0284c7",
        "label_bg": "#075985",
        "accent_color": "#facc15",
        "cap_color": "#0369a1",
        "brand_text": "VITAP",
        "title_en": "DAILY MULTI VITAMIN",
        "sub_title": "COMPLETE MINERALS & VITAMINS",
        "badge_text": "60 TABLETS",
        "spec_text": "FULL DAY ATHLETE NUTRITION"
    }
]

for cfg in products_catalog:
    svg_code = generate_tub_svg(cfg)
    fname = f"{cfg['id']}.svg"
    with open(os.path.join(products_dir, fname), "w", encoding="utf-8") as f:
        f.write(svg_code)
    with open(os.path.join(mokamel_products_dir, fname), "w", encoding="utf-8") as f:
        f.write(svg_code)

print(f"Generated {len(products_catalog)} realistic product images in both directories.")
