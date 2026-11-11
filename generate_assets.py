# -*- coding: utf-8 -*-
import os
import shutil

brands_dir = "images/brands"
products_dir = "images/products"
mokamel_brands_dir = "mokamel/images/brands"
mokamel_products_dir = "mokamel/images/products"

for d in [brands_dir, products_dir, mokamel_brands_dir, mokamel_products_dir]:
    os.makedirs(d, exist_ok=True)

# ۱. لوگوی رسمی برندها
brand_logos = {
    "kalleh": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <circle cx="60" cy="60" r="56" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
        <circle cx="60" cy="60" r="48" fill="#ffffff"/>
        <circle cx="60" cy="60" r="42" fill="#0369a1"/>
        <text x="60" y="55" font-size="16" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="1">KALLEH</text>
        <rect x="42" y="64" width="36" height="15" rx="4" fill="#dc2626"/>
        <text x="60" y="75" font-size="10" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="1.5">PRO</text>
    </svg>''',

    "pnc": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#0f172a" stroke="#334155" stroke-width="2"/>
        <rect x="10" y="10" width="100" height="100" rx="16" fill="#b91c1c"/>
        <polygon points="60,22 96,44 96,76 60,98 24,76 24,44" fill="#ffffff" opacity="0.18"/>
        <text x="60" y="62" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Arial Black, Impact, sans-serif" letter-spacing="2">PNC</text>
        <rect x="25" y="73" width="70" height="14" rx="3" fill="#1e293b"/>
        <text x="60" y="83" font-size="8" font-weight="800" fill="#f87171" text-anchor="middle" font-family="'Segoe UI', sans-serif">KAREN PHARMA</text>
    </svg>''',

    "genestar": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#090d16" stroke="#d97706" stroke-width="2"/>
        <circle cx="60" cy="60" r="46" fill="none" stroke="#f59e0b" stroke-width="3" opacity="0.3"/>
        <polygon points="60,18 69,38 91,41 75,56 79,77 60,67 41,77 45,56 29,41 51,38" fill="#f59e0b"/>
        <circle cx="60" cy="50" r="12" fill="#090d16"/>
        <text x="60" y="94" font-size="12" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="1">GENESTAR</text>
        <text x="60" y="105" font-size="7" font-weight="700" fill="#fbbf24" text-anchor="middle" font-family="'Segoe UI', sans-serif">NUTRITION</text>
    </svg>''',

    "doobis": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#4c1d95" stroke="#7c3aed" stroke-width="2"/>
        <circle cx="60" cy="52" r="30" fill="#5b21b6" stroke="#a78bfa" stroke-width="2"/>
        <path d="M45 42 Q60 26 75 42 Q75 62 60 70 Q45 62 45 42 Z" fill="#facc15"/>
        <circle cx="60" cy="48" r="8" fill="#4c1d95"/>
        <text x="60" y="96" font-size="16" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="'Segoe UI', sans-serif" letter-spacing="2">DOOBIS</text>
    </svg>''',

    "pegah": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <circle cx="60" cy="60" r="56" fill="#047857" stroke="#34d399" stroke-width="2"/>
        <path d="M60 22 C60 22 88 52 88 74 C88 88 75 98 60 98 C45 98 32 88 32 74 C32 52 60 22 60 22 Z" fill="#ffffff"/>
        <circle cx="60" cy="74" r="16" fill="#047857"/>
        <text x="60" y="79" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="'B Nazanin', Tahoma, sans-serif">پگاه</text>
        <text x="60" y="112" font-size="8" font-weight="700" fill="#a7f3d0" text-anchor="middle" font-family="sans-serif">PEGAH PROTEIN</text>
    </svg>''',

    "vitap": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#1e3a8a" stroke="#3b82f6" stroke-width="2"/>
        <g transform="translate(60, 48)">
            <circle cx="-16" cy="0" r="16" fill="#ef4444"/>
            <circle cx="16" cy="0" r="16" fill="#ffffff"/>
            <path d="M-8 -14 L8 -14 L8 14 L-8 14 Z" fill="#0284c7" opacity="0.8"/>
        </g>
        <text x="60" y="88" font-size="17" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Arial Black, Impact, sans-serif" letter-spacing="1">VITAP</text>
        <text x="60" y="102" font-size="7.5" font-weight="700" fill="#93c5fd" text-anchor="middle" font-family="sans-serif">HEALTH & SPORTS</text>
    </svg>''',

    "on": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#000000" stroke="#b91c1c" stroke-width="2"/>
        <circle cx="60" cy="48" r="32" fill="#18181b"/>
        <text x="44" y="60" font-size="40" font-weight="900" fill="#dc2626" text-anchor="middle" font-family="Impact, Arial Black, sans-serif">O</text>
        <text x="76" y="60" font-size="40" font-weight="900" fill="#f59e0b" text-anchor="middle" font-family="Impact, Arial Black, sans-serif">N</text>
        <line x1="20" y1="84" x2="100" y2="84" stroke="#dc2626" stroke-width="2"/>
        <text x="60" y="98" font-size="7.5" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="0.5">OPTIMUM NUTRITION</text>
    </svg>''',

    "dymatize": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#090d16" stroke="#0284c7" stroke-width="2"/>
        <polygon points="25,28 60,84 38,84" fill="#0284c7"/>
        <polygon points="52,28 87,84 65,84" fill="#38bdf8"/>
        <polygon points="80,28 98,56 86,56" fill="#0ea5e9"/>
        <text x="60" y="104" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Arial Black, sans-serif" letter-spacing="1">DYMATIZE</text>
    </svg>''',

    "muscletech": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#111827" stroke="#dc2626" stroke-width="2"/>
        <rect x="16" y="34" width="88" height="30" rx="6" fill="#dc2626"/>
        <text x="60" y="55" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="'Arial Black', Impact, sans-serif" letter-spacing="1">MUSCLETECH</text>
        <line x1="20" y1="76" x2="100" y2="76" stroke="#ffffff" stroke-width="1" opacity="0.3"/>
        <text x="60" y="88" font-size="7.5" font-weight="700" fill="#9ca3af" text-anchor="middle" font-family="sans-serif">RESEARCH & DEVELOPMENT</text>
    </svg>''',

    "carnivor": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#2d0606" stroke="#ef4444" stroke-width="2"/>
        <polygon points="60,18 92,36 86,72 60,88 34,72 28,36" fill="#dc2626"/>
        <polygon points="60,26 84,40 79,68 60,80 41,68 36,40" fill="#7f1d1d"/>
        <text x="60" y="54" font-size="12" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Arial Black, Impact, sans-serif" letter-spacing="1">CARNIVOR</text>
        <text x="60" y="67" font-size="7" font-weight="900" fill="#fca5a5" text-anchor="middle" font-family="sans-serif">BEEF PROTEIN</text>
        <text x="60" y="104" font-size="8" font-weight="800" fill="#ffffff" text-anchor="middle" font-family="sans-serif">MUSCLEMEDS</text>
    </svg>''',

    "cellucor": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#000000" stroke="#eab308" stroke-width="2"/>
        <polygon points="60,16 98,38 98,82 60,104 22,82 22,38" fill="#eab308"/>
        <polygon points="60,24 90,42 90,78 60,96 30,78 30,42" fill="#000000"/>
        <text x="60" y="68" font-size="34" font-weight="900" fill="#eab308" text-anchor="middle" font-family="Impact, Arial Black, sans-serif">C4</text>
        <text x="60" y="112" font-size="8" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="sans-serif" letter-spacing="1">CELLUCOR</text>
    </svg>''',

    "bsn": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#450a0a" stroke="#dc2626" stroke-width="2"/>
        <path d="M22 28 L98 28 L90 74 L60 96 L30 74 Z" fill="#dc2626" stroke="#f87171" stroke-width="2"/>
        <text x="60" y="62" font-size="24" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Arial Black, Impact, sans-serif" letter-spacing="2">BSN</text>
        <rect x="30" y="72" width="60" height="12" rx="3" fill="#18181b"/>
        <text x="60" y="81" font-size="7" font-weight="800" fill="#fca5a5" text-anchor="middle" font-family="sans-serif">FINISH FIRST.</text>
    </svg>''',

    "applied": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#000000" stroke="#334155" stroke-width="2"/>
        <rect x="20" y="32" width="80" height="34" fill="#ffffff" rx="4"/>
        <text x="60" y="56" font-size="18" font-weight="900" fill="#000000" text-anchor="middle" font-family="Arial Black, Impact, sans-serif" letter-spacing="1">A.B.E.</text>
        <text x="60" y="88" font-size="7.5" font-weight="800" fill="#ffffff" text-anchor="middle" font-family="sans-serif" letter-spacing="0.5">APPLIED NUTRITION</text>
    </svg>''',

    "myprotein": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
        <line x1="20" y1="58" x2="100" y2="58" stroke="#ffffff" stroke-width="3"/>
        <text x="60" y="50" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="1">MYPROTEIN</text>
        <text x="60" y="78" font-size="8" font-weight="700" fill="#e0f2fe" text-anchor="middle" font-family="sans-serif">FUEL YOUR AMBITION</text>
    </svg>''',

    "levrone": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#0a0e17" stroke="#d97706" stroke-width="2"/>
        <circle cx="60" cy="54" r="34" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
        <circle cx="60" cy="54" r="28" fill="#1e293b"/>
        <text x="60" y="63" font-size="24" font-weight="900" fill="#fbbf24" text-anchor="middle" font-family="Times New Roman, serif">KL</text>
        <text x="60" y="98" font-size="8.5" font-weight="800" fill="#ffffff" text-anchor="middle" font-family="sans-serif" letter-spacing="0.5">KEVIN LEVRONE</text>
        <text x="60" y="109" font-size="6.5" font-weight="700" fill="#d97706" text-anchor="middle" font-family="sans-serif">SIGNATURE SERIES</text>
    </svg>''',

    "rule1": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#7f1d1d" stroke="#ef4444" stroke-width="2"/>
        <text x="48" y="70" font-size="44" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Impact, Arial Black, sans-serif">R</text>
        <text x="82" y="70" font-size="44" font-weight="900" fill="#fca5a5" text-anchor="middle" font-family="Impact, Arial Black, sans-serif">1</text>
        <text x="60" y="96" font-size="8.5" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="sans-serif" letter-spacing="1">RULE ONE</text>
    </svg>''',

    "universal": '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="20" fill="#18181b" stroke="#475569" stroke-width="2"/>
        <text x="60" y="58" font-size="24" font-weight="900" fill="#ef4444" text-anchor="middle" font-family="Impact, sans-serif" letter-spacing="1.5">ANIMAL</text>
        <rect x="22" y="68" width="76" height="14" rx="3" fill="#dc2626"/>
        <text x="60" y="79" font-size="8.5" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="sans-serif" letter-spacing="1">UNIVERSAL</text>
    </svg>'''
}

for name, svg_code in brand_logos.items():
    with open(os.path.join(brands_dir, f"{name}.svg"), "w", encoding="utf-8") as f:
        f.write(svg_code)
    with open(os.path.join(mokamel_brands_dir, f"{name}.svg"), "w", encoding="utf-8") as f:
        f.write(svg_code)

print(f"Created {len(brand_logos)} brand logos in both directories.")
