# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

supplements_code = """[
            // ۱. پروتئین بیف (گوشت خالص)
            {
                id: "carnivor-beef-2000",
                department: "supplements",
                image: "images/products/carnivor-beef-2000.svg",
                ingredients: ["beef_isolate", "bcaa_branched", "creatine_mono"],
                name: "پروتئین بیف ایزوله کارنیور ماسکوپولیس (Carnivor Beef)",
                brand: "MuscleMeds (Carnivor)",
                origin: "foreign",
                category: "protein",
                subType: "beef",
                weight: "2000 گرم",
                price: 6800000,
                svg: render3DSupplementSVG("beef", "Carnivor", "BEEF ISOLATE", "#991b1b", "#ef4444", "#7f1d1d"),
                purpose: "پروتئین خالص گوشت گاو هیدرولیزه شده با ۳۵۰٪ تراکم آمینو بیشتر از استیک، ۳۵۰ میلی‌گرم کراتین طبیعی، بدون لاکتوز و چربی صفر.",
                usage: "یک اسکوپ بعد از تمرین در آب سرد مصرف شود.",
                timings: [
                    { time: "بلافاصله بعد تمرین", desc: "جذب سریع پروتئین حیوانی خالص بدون نفخ و لاکتوز" }
                ],
                warnings: "افراد حساس به ترکیبات گوشت قرمز با احتیاط مصرف کنند."
            },

            // ۲. پروتئین سفیده تخم‌مرغ (آلبومین)
            {
                id: "genestar-egg-albumin-2000",
                department: "supplements",
                image: "images/products/genestar-egg-albumin-2000.svg",
                ingredients: ["egg_albumin", "bcaa_branched"],
                name: "پودر سفیده تخم مرغ آلبومین ژن استار (Egg Albumin)",
                brand: "ژن استار (Genestar)",
                origin: "iran",
                category: "protein",
                subType: "egg",
                weight: "2000 گرم",
                price: 2450000,
                svg: render3DSupplementSVG("egg", "Genestar", "EGG ALBUMIN", "#ca8a04", "#fef08a", "#a16207"),
                purpose: "پروتئین خالص سفیده تخم‌مرغ با ارزش بیولوژیکی ۱۰۰ (کامل‌ترین پروفایل آمینواسید)، هضم متوسط و مناسب رشد پایدار عضلانی.",
                usage: "یک اسکوپ صبح و یک اسکوپ بعد تمرین با آب یا شیر کم‌چرب مخلوط و میل شود.",
                timings: [
                    { time: "میان‌وعده و صبح", desc: "تغذیه تدریجی و مداوم عضلات با پروتئین تخم‌مرغ" }
                ],
                warnings: "برای افراد دارای حساسیت به آلبومین یا تخم‌مرغ منع مصرف دارد."
            },
            {
                id: "doobis-egg-albumin-1000",
                department: "supplements",
                image: "images/products/doobis-egg-albumin-1000.svg",
                ingredients: ["egg_albumin", "bcaa_branched"],
                name: "پودر پروتئین سفیده تخم مرغ دوبیس ۱۰۰۰ گرمی",
                brand: "دوبیس (Doobis)",
                origin: "iran",
                category: "protein",
                subType: "egg",
                weight: "1000 گرم",
                price: 1350000,
                svg: render3DSupplementSVG("egg_db", "Doobis", "EGG PROTEIN", "#a16207", "#fef08a", "#713f12"),
                purpose: "تامین پروتئین استاندارد از سفیده تخم‌مرغ پاستوریزه بدون کلسترول و چربی زرده.",
                usage: "یک پیمانه در آب خنک حل شده و میل شود.",
                timings: [
                    { time: "بعد تمرین یا قبل خواب", desc: "ماندگاری طولانی‌تر اسیدهای آمینه در خون" }
                ],
                warnings: "در افراد با ناراحتی‌های گوارشی خاص با مشورت مصرف شود."
            },

            // ۳. پروتئین گیاهی (وگان / سویا)
            {
                id: "vitap-vegan-protein-1000",
                department: "supplements",
                image: "images/products/vitap-vegan-protein-1000.svg",
                ingredients: ["plant_pea_soy", "bcaa_branched"],
                name: "پروتئین گیاهی فیت وگان ویتاپی (Plant Protein)",
                brand: "ویتاپی (VitaP)",
                origin: "iran",
                category: "protein",
                subType: "plant",
                weight: "1000 گرم",
                price: 980000,
                svg: render3DSupplementSVG("vegan", "VitaP", "PLANT VEGAN", "#047857", "#86efac", "#064e3b"),
                purpose: "ترکیب پروتئین نخود، سویا و برنج قهوه‌ای، بدون لاکتوز و بدون چربی اشباع، مناسب ورزشکاران گیاه‌خوار و حساس به لبنیات.",
                usage: "یک پیمانه ۳۰ گرمی همراه با آب یا شیر بادام.",
                timings: [
                    { time: "بعد تمرین و میان‌وعده", desc: "تامین پروتئین طبیعی گیاهی" }
                ],
                warnings: "به دلیل بافت فیبری، با آب بیشتری مخلوط شود."
            },

            // ۴. پروتئین ترکیبی (Blend)
            {
                id: "bsn-syntha6-2270",
                department: "supplements",
                image: "images/products/bsn-syntha6-2270.svg",
                ingredients: ["protein_blend", "whey_concentrate", "casein_micellar", "egg_albumin", "bcaa_branched"],
                name: "پروتئین ترکیبی سینتا ۶ بی اس ان (BSN Syntha-6)",
                brand: "BSN",
                origin: "foreign",
                category: "protein",
                subType: "blend",
                weight: "2270 گرم",
                price: 5200000,
                svg: render3DSupplementSVG("whey", "BSN", "SYNTHA-6", "#b91c1c", "#ffffff", "#7f1d1d"),
                purpose: "ترکیب ۶ پروتئین زودجذب و دیرجذب (وی کنسانتره، وی ایزوله، کازئین، آلبومین و پپتید) برای تغذیه ۲۴ ساعته عضلات.",
                usage: "یک پیمانه در آب یا شیر حل شود.",
                timings: [
                    { time: "بعد تمرین یا میان‌وعده", desc: "رهاسازی پیوسته اسیدهای آمینه" }
                ],
                warnings: "در رژیم‌های صفر کربوهیدرات مسابقاتی با احتساب کالری مصرف شود."
            },

            // ۵. پروتئین وی ایزوله، کنسانتره، هیدرولیزه و کازئین
            {
                id: "kalleh-isolate-650",
                department: "supplements",
                image: "images/products/kalleh-isolate-650.svg",
                ingredients: ["whey_isolate", "bcaa_branched", "glutamine_pure"],
                name: "پودر پروتئین وی ایزوله کاله پرو ۹۰٪",
                brand: "کاله پرو (Kalleh Pro)",
                origin: "iran",
                category: "protein",
                subType: "isolate",
                weight: "650 گرم",
                price: 1450000,
                svg: render3DSupplementSVG("iso", "Kalleh", "ISO WHEY 90%", "#0369a1", "#67e8f9", "#082f49"),
                purpose: "وی ایزوله بسیار خالص با چربی و لاکتوز نزدیک به صفر، ایده‌آل برای دوره کات و مسابقات.",
                usage: "یک اسکوپ بعد تمرین و یک اسکوپ صبح در آب خنک حل شود.",
                timings: [
                    { time: "بلافاصله پس از تمرین", desc: "جذب فوق‌العاده سریع بدون هرگونه نفخ گوارشی" }
                ],
                warnings: "در دمای خشک و خنک نگهداری شود."
            },
            {
                id: "kalleh-whey-650",
                department: "supplements",
                image: "images/products/kalleh-whey-650.svg",
                ingredients: ["whey_concentrate", "bcaa_branched"],
                name: "پودر پروتئین وی ۱۰۰٪ کاله پرو (Kalleh Pro)",
                brand: "کاله پرو (Kalleh Pro)",
                origin: "iran",
                category: "protein",
                subType: "concentrate",
                weight: "650 گرم",
                price: 1150000,
                svg: render3DSupplementSVG("whey", "Kalleh", "WHEY 100%", "#0284c7", "#38bdf8", "#0369a1"),
                purpose: "تامین پروتئین خالص با جذب بالا، عضله‌سازی و تسریع ریکاوری بدون قند و چربی مضر.",
                usage: "یک اسکوپ (۳۲ گرم) را با ۲۵۰ میلی‌لیتر آب یا شیر کم‌چرب بعد تمرین مصرف نمایید.",
                timings: [
                    { time: "بلافاصله بعد تمرین", desc: "ترمیم فیبرهای عضلانی و تحریک سنتز پروتئین" }
                ],
                warnings: "افراد دارای حساسیت شدید به پروتئین‌های شیر با احتیاط مصرف کنند."
            },
            {
                id: "dymatize-iso-100-2270",
                department: "supplements",
                image: "images/products/dymatize-iso-100-2270.svg",
                ingredients: ["whey_isolate", "whey_hydrolyzed", "bcaa_branched", "glutamine_pure"],
                name: "ایزو ۱۰۰ هیدرولیزه دایماتیز (Dymatize ISO 100)",
                brand: "Dymatize",
                origin: "foreign",
                category: "protein",
                subType: "hydrolyzed",
                weight: "2270 گرم",
                price: 8200000,
                svg: render3DSupplementSVG("iso", "Dymatize", "ISO 100", "#1e3a8a", "#60a5fa", "#172554"),
                purpose: "لوکس‌ترین پروتئین وی هیدرولیزه جهان با هضم فوری و خلوص بیش از ۹۰ درصد.",
                usage: "یک پیمانه در ۲۰۰ میلی‌لیتر آب خنک بلافاصله حل می‌شود.",
                timings: [
                    { time: "بلافاصله بعد تمرین", desc: "ورود اسیدهای آمینه به خون در کمتر از ۲۰ دقیقه" }
                ],
                warnings: "برای دوران کات و ورزشکاران حرفه‌ای مناسب‌ترین گزینه است."
            },
            {
                id: "on-gold-whey-2270",
                department: "supplements",
                image: "images/products/on-gold-whey-2270.svg",
                ingredients: ["whey_isolate", "whey_concentrate", "whey_hydrolyzed", "bcaa_branched", "glutamine_pure"],
                name: "پروتئین وی ۱۰۰٪ گلد استاندارد اپتیموم (ON Gold Whey)",
                brand: "Optimum Nutrition (ON)",
                origin: "foreign",
                category: "protein",
                subType: "isolate",
                weight: "2270 گرم",
                price: 6400000,
                svg: render3DSupplementSVG("whey", "ON", "GOLD STANDARD", "#0f172a", "#fbbf24", "#d97706"),
                purpose: "پرفروش‌ترین و معتبرترین پروتئین وی جهان، غنی از پپتیدهای هیدرولیزه و ایزوله.",
                usage: "یک پیمانه ۳۰ گرمی در ۲۰۰ الی ۲۵۰ میلی‌لیتر آب سرد حل شده و مصرف شود.",
                timings: [
                    { time: "بلافاصله بعد تمرین", desc: "طلایی‌ترین زمان برای سنتز پروتئین عضلانی" }
                ],
                warnings: "به دلیل وجود نمونه‌های فیک در بازار، حتماً از منابع معتبر تهیه شود."
            },
            {
                id: "on-casein-1800",
                department: "supplements",
                image: "images/products/on-casein-1800.svg",
                ingredients: ["casein_micellar", "bcaa_branched", "glutamine_pure"],
                name: "کازئین ۱۰۰٪ گلد استاندارد اپتیموم (ON Casein)",
                brand: "Optimum Nutrition (ON)",
                origin: "foreign",
                category: "protein",
                subType: "casein",
                weight: "1800 گرم",
                price: 5800000,
                svg: render3DSupplementSVG("casein", "ON", "100% CASEIN", "#1e1b4b", "#818cf8", "#312e81"),
                purpose: "پروتئین دیرجذب شبانه برای تغذیه پیوسته عضلات طی ۷ تا ۸ ساعت خواب شبانه.",
                usage: "یک اسکوپ در آب یا شیر قبل از خواب میل شود.",
                timings: [
                    { time: "قبل از خواب شبانه", desc: "جلوگیری از افت عضله در طول خواب" }
                ],
                warnings: "قوام غلیظ‌تری نسبت به وی دارد."
            },
            {
                id: "pnc-pure-whey-2270",
                department: "supplements",
                image: "images/products/pnc-pure-whey-2270.svg",
                ingredients: ["whey_concentrate", "whey_isolate", "bcaa_branched", "glutamine_pure"],
                name: "پیور وی کارن (PNC Pure Whey)",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "protein",
                subType: "concentrate",
                weight: "2270 گرم",
                price: 3200000,
                svg: render3DSupplementSVG("whey", "PNC", "PURE WHEY", "#b91c1c", "#f87171", "#7f1d1d"),
                purpose: "پروتئین کنسانتره داروسازی کارن به همراه گلوتامین و ویتامین‌ها برای عضله‌سازی خشک.",
                usage: "روزانه ۱ تا ۲ پیمانه (هر پیمانه حدود ۳۰ گرم) همراه با آب مصرف شود.",
                timings: [
                    { time: "بعد از تمرین", desc: "بهترین زمان برای ریکاوری بهینه" }
                ],
                warnings: "حاوی فنیل‌آلانین (برای بیماران فنیل‌کتونوری منع مصرف دارد)."
            },

            // ۶. گینر و کربوهیدرات
            {
                id: "pnc-super-mass-5000",
                department: "supplements",
                image: "images/products/pnc-super-mass-5000.svg",
                ingredients: ["high_calorie_gainer", "complex_carbs", "whey_concentrate", "bcaa_branched"],
                name: "سوپر مس گینر کارن (PNC Super Mass)",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "gainer",
                subType: "mass",
                weight: "5000 گرم",
                price: 2850000,
                svg: render3DSupplementSVG("gainer", "PNC", "SUPER MASS", "#d97706", "#fde047", "#78350f"),
                purpose: "افزایش وزن و حجم سریع برای افراد اکتومورف، تامین کربوهیدرات کمپلکس و پروتئین باکیفیت.",
                usage: "روزانه تا ۴ پیمانه در چند نوبت بین وعده‌ها و بعد از تمرین مصرف شود.",
                timings: [
                    { time: "بعد تمرین", desc: "پر کردن ذخایر گلیکوژن تخلیه شده" }
                ],
                warnings: "افراد دارای اضافه وزن یا دیابت نباید از گینر پرکالری استفاده کنند."
            },
            {
                id: "on-serious-mass-5400",
                department: "supplements",
                image: "images/products/on-serious-mass-5400.svg",
                ingredients: ["high_calorie_gainer", "complex_carbs", "whey_concentrate", "daily_multivitamin", "creatine_mono"],
                name: "سریوس مس گینر اپتیموم نوتریشن (ON Serious Mass)",
                brand: "Optimum Nutrition (ON)",
                origin: "foreign",
                category: "gainer",
                subType: "mass",
                weight: "5400 گرم",
                price: 4950000,
                svg: render3DSupplementSVG("gainer", "ON", "SERIOUS MASS", "#1e293b", "#38bdf8", "#0284c7"),
                purpose: "معروف‌ترین مس گینر جهان با ۱۲۵۰ کالری و ۵۰ گرم پروتئین در هر وعده برای جهش در وزن و سایز عضلات.",
                usage: "روزانه در ۲ یا ۳ نوبت نصف پیمانه‌ای همراه با شیر پرچرب یا آب مصرف شود.",
                timings: [
                    { time: "بین وعده‌های غذایی", desc: "تامین پیوسته کالری مازاد" }
                ],
                warnings: "به دلیل کالری بالا فقط برای افراد لاغر مناسب است."
            },
            {
                id: "pnc-carbo-2000",
                department: "supplements",
                image: "images/products/pnc-carbo-2000.svg",
                ingredients: ["complex_carbs"],
                name: "پودر کربوهیدرات خالص کارن ۲۰۰۰ گرمی",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "gainer",
                subType: "carbo",
                weight: "2000 گرم",
                price: 890000,
                svg: render3DSupplementSVG("carbo", "PNC", "CARBO PURE", "#ca8a04", "#fef08a", "#854d0e"),
                purpose: "تامین ۱۰۰٪ مالتودکسترین خالص بدون چربی و پروتئین برای پر کردن فوری گلیکوژن کبد و عضلات.",
                usage: "قبل یا بعد از تمرین ۲ پیمانه در آب حل شود.",
                timings: [
                    { time: "حین یا بعد تمرین", desc: "تامین انرژی انفجاری و ریکاوری گلیکوژن" }
                ],
                warnings: "افراد دیابتی نباید مصرف کنند."
            },
            {
                id: "levrone-gold-lean-mass-3000",
                department: "supplements",
                image: "images/products/levrone-gold-lean-mass-3000.svg",
                ingredients: ["high_calorie_gainer", "whey_isolate", "whey_concentrate", "tribulus_terrestris", "creatine_mono", "bcaa_branched"],
                name: "گلد لین مس کوین لورون (Kevin Levrone Gold Lean Mass)",
                brand: "Kevin Levrone",
                origin: "foreign",
                category: "gainer",
                subType: "lean",
                weight: "3000 گرم",
                price: 4200000,
                svg: render3DSupplementSVG("gainer", "Levrone", "GOLD LEAN MASS", "#090d16", "#fbbf24", "#b45309"),
                purpose: "گینر حجم خشک لوکس حاوی DAA، عصاره شنبلیله، ال آرژنین و HMB برای افزایش سایز عضلانی تمیز.",
                usage: "۲ پیمانه در طول روز همراه آب.",
                timings: [
                    { time: "بعد تمرین", desc: "ترمیم عضلات و حمایت از بالانس هورمونی" }
                ],
                warnings: "برای افراد زیر ۱۸ سال توصیه نمی‌شود."
            },

            // ۷. کراتین‌ها (مونوهیدرات، میکرونایزد، ترکیبی، کراتین بتاآلانین، کریپیور)
            {
                id: "doobis-creatine-beta-300",
                department: "supplements",
                image: "images/products/doobis-creatine-beta-300.svg",
                ingredients: ["creatine_mono", "beta_alanine_carnosyn"],
                name: "کراتین بتا آلانین دوبیس ۳۰۰ گرمی",
                brand: "دوبیس (Doobis)",
                origin: "iran",
                category: "creatine",
                subType: "beta_creatine",
                weight: "300 گرم",
                price: 780000,
                svg: render3DSupplementSVG("c_beta", "Doobis", "CREA+BETA", "#059669", "#fde047", "#064e3b"),
                purpose: "ترکیب همزمان کراتین مونوهیدرات و بتاآلانین جهت افزایش توان انفجاری و تاخیر خستگی ناشی از اسید لاکتیک.",
                usage: "یک پیمانه قبل یا بعد از تمرین در آب حل شود.",
                timings: [
                    { time: "۳۰ دقیقه قبل تمرین", desc: "افزایش همزمان پمپاژ، توان و مهار اسیدیته عضله" }
                ],
                warnings: "خارش ملایم بتاآلانین طبیعی است."
            },
            {
                id: "pnc-creatine-300",
                department: "supplements",
                image: "images/products/pnc-creatine-300.svg",
                ingredients: ["creatine_mono"],
                name: "کراتین مونوهیدرات میکرونایزد کارن",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "creatine",
                subType: "monohydrate",
                weight: "300 گرم",
                price: 580000,
                svg: render3DSupplementSVG("creatine", "PNC", "CREATINE", "#047857", "#34d399", "#064e3b"),
                purpose: "افزایش توان بی‌هوازی، افزایش قدرت در تکرارهای سنگین و هیدراتاسیون داخل سلولی عضلات.",
                usage: "روزانه ۵ گرم همراه با یک لیوان آب یا آب‌میوه بعد از تمرین.",
                timings: [
                    { time: "بعد از تمرین", desc: "حداکثر بازدهی با شیک پروتئین یا کربوهیدرات" }
                ],
                warnings: "نوشیدن روزانه حداقل ۳ لیتر آب در طول دوره الزامی است."
            },
            {
                id: "muscletech-celltech-2700",
                department: "supplements",
                image: "images/products/muscletech-celltech-2700.svg",
                ingredients: ["creatine_complex", "creatine_mono", "complex_carbs", "bcaa_branched"],
                name: "سل تک کراتین پیشرفته ماسل تک (Cell-Tech)",
                brand: "MuscleTech",
                origin: "foreign",
                category: "creatine",
                subType: "complex",
                weight: "2700 گرم",
                price: 4500000,
                svg: render3DSupplementSVG("creatine", "MuscleTech", "CELL-TECH", "#1e293b", "#f97316", "#c2410c"),
                purpose: "فرمول افسانه‌ای کراتین ترانسپورت با کربوهیدرات‌های اختصاصی برای انفجار حجم و قدرت عضلات.",
                usage: "یک اسکوپ بلافاصله بعد تمرین با آب سرد.",
                timings: [
                    { time: "بلافاصله پس از تمرین", desc: "ترشح انسولین و هل دادن کراتین به درون سلول عضلانی" }
                ],
                warnings: "طعم میوه‌ای و قند دارد."
            },
            {
                id: "myprotein-creapure-500",
                department: "supplements",
                image: "images/products/myprotein-creapure-500.svg",
                ingredients: ["creatine_creapure", "creatine_mono"],
                name: "کراتین خالص کریپیور مای‌پروتئین (Creapure)",
                brand: "MyProtein",
                origin: "foreign",
                category: "creatine",
                subType: "creapure",
                weight: "500 گرم",
                price: 2300000,
                svg: render3DSupplementSVG("creatine", "MyProtein", "CREAPURE", "#0284c7", "#e0f2fe", "#0369a1"),
                purpose: "خالص‌ترین شکل کراتین دنیا (Creapure ساخت آلمان) با خلوص ۹۹.۹۹ درصد، بدون ناخالصی و فلزات سنگین.",
                usage: "روزانه ۵ گرم همراه آب یا شیک بعد تمرین.",
                timings: [
                    { time: "بعد تمرین", desc: "ایده‌آل‌ترین خلوص بدون حتی ذره‌ای ناخالصی" }
                ],
                warnings: "آب فراوان در طول روز مصرف کنید."
            },

            // ۸. آمینواسیدها (آمینو وی، BCAA، گلوتامین، آرژنین، HMB)
            {
                id: "pnc-arginine-1000",
                department: "supplements",
                image: "images/products/pnc-arginine-1000.svg",
                ingredients: ["arginine_hcl"],
                name: "قرص ال آرژنین ۱۰۰۰ میلی‌گرم کارن",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "amino",
                subType: "arginine",
                weight: "100 عدد",
                price: 520000,
                svg: render3DSupplementSVG("arg", "PNC", "L-ARGININE", "#dc2626", "#fca5a5", "#991b1b"),
                purpose: "پیش‌ساز نیتریک اکسید (NO)، گشادکننده عروق خونی، افزایش پمپاژ خون و تحریک ترشح هورمون رشد.",
                usage: "۱ تا ۲ قرص قبل تمرین یا قبل خواب.",
                timings: [
                    { time: "قبل تمرین و قبل خواب", desc: "اتساع عروق و تحریک هورمون رشد شبانه" }
                ],
                warnings: "افراد دارای سابقه تبخال با احتیاط مصرف کنند."
            },
            {
                id: "doobis-amino-whey-300",
                department: "supplements",
                image: "images/products/doobis-amino-whey-300.svg",
                ingredients: ["amino_peptides", "whey_concentrate", "bcaa_branched"],
                name: "قرص آمینو وی دوبیس ۳۰۰ عددی",
                brand: "دوبیس (Doobis)",
                origin: "iran",
                category: "amino",
                subType: "amino_whey",
                weight: "300 عدد",
                price: 980000,
                svg: render3DSupplementSVG("amino_w", "Doobis", "AMINO WHEY", "#7c3aed", "#e9d5ff", "#581c87"),
                purpose: "تامین تمام اسیدهای آمینه شاخه‌دار و ضروری از پروتئین وی فشرده در قالب قرص‌های راحت‌هضم.",
                usage: "۳ عدد قبل تمرین و ۳ عدد بعد تمرین.",
                timings: [
                    { time: "قبل و بعد از تمرین", desc: "تغذیه پیوسته عضلات حین و بعد ورزش" }
                ],
                warnings: "با آب فراوان میل شود."
            },
            {
                id: "pnc-bcaa-300",
                department: "supplements",
                image: "images/products/pnc-bcaa-300.svg",
                ingredients: ["bcaa_branched"],
                name: "پودر بی سی ای ای کارن (PNC BCAA)",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "amino",
                subType: "bcaa",
                weight: "300 گرم",
                price: 890000,
                svg: render3DSupplementSVG("amino", "PNC", "BCAA 2:1:1", "#7c3aed", "#c084fc", "#4c1d95"),
                purpose: "پیشگیری از کاتابولیسم و ریزش عضلات در حین تمرین پرفشار و دوره‌های رژیم کات.",
                usage: "۵ تا ۱۰ گرم در طول جلسه تمرین در بطری آب ورزشی حل شده و نوشیده شود.",
                timings: [
                    { time: "حین تمرین", desc: "تغذیه مداوم عضلات و کاهش خستگی سیستم عصبی" }
                ],
                warnings: "بیش از حد مصرف نشود."
            },
            {
                id: "genestar-pure-glutamine-300",
                department: "supplements",
                image: "images/products/genestar-pure-glutamine-300.svg",
                ingredients: ["glutamine_pure"],
                name: "گلوتامین ۱۰۰٪ خالص ژن استار ۳۰۰ گرمی",
                brand: "ژن استار (Genestar)",
                origin: "iran",
                category: "amino",
                subType: "glutamine",
                weight: "300 گرم",
                price: 820000,
                svg: render3DSupplementSVG("glutamine", "Genestar", "GLUTAMINE", "#0284c7", "#7dd3fc", "#0369a1"),
                purpose: "بازسازی بافت‌های تخلیه شده، حفظ سلامت دستگاه گوارش و روده و پیشگیری از سرماخوردگی و ضعف بدنسازان.",
                usage: "۵ گرم بعد تمرین و ۵ گرم قبل خواب.",
                timings: [
                    { time: "بعد تمرین و قبل خواب", desc: "بهبود ریکاوری شبانه و مهار کورتیزول" }
                ],
                warnings: "افراد دارای مشکلات شدید کلیوی مشورت کنند."
            },
            {
                id: "pnc-hmb-120",
                department: "supplements",
                image: "images/products/pnc-hmb-120.svg",
                ingredients: ["hmb_pure"],
                name: "کپسول اچ ام بی کارن (PNC HMB)",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "amino",
                subType: "hmb",
                weight: "120 عدد",
                price: 950000,
                svg: render3DSupplementSVG("hmb", "PNC", "HMB 1000", "#d97706", "#fde047", "#78350f"),
                purpose: "سپر ضد ریزش عضلات، متابولیت فعال لوسین جهت حفظ بافت عضلانی در رژیم‌های سخت کات.",
                usage: "روزانه ۳ کپسول در وعده‌های مختلف همراه آب.",
                timings: [
                    { time: "قبل تمرین و همراه وعده ناهار", desc: "جلوگیری قطعی از تخریب پروتئین عضلانی" }
                ],
                warnings: "برای دیدن اثرات حداقل ۲ تا ۳ هفته مصرف شود."
            },

            // ۹. قبل تمرین، سیترولین، بتاآلانین و کافئین
            {
                id: "pnc-beta-alanine-300",
                department: "supplements",
                image: "images/products/pnc-beta-alanine-300.svg",
                ingredients: ["beta_alanine_carnosyn"],
                name: "پودر بتا آلانین کارن ۳۰۰ گرمی",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "energy",
                subType: "beta_alanine",
                weight: "300 گرم",
                price: 790000,
                svg: render3DSupplementSVG("beta", "PNC", "BETA-ALANINE", "#dc2626", "#fde047", "#991b1b"),
                purpose: "افزایش سطح کارنوزین عضلات، تاخیر در اسیدی شدن عضله و امکان اجرای تکرارهای بیشتر در ست‌های سنگین.",
                usage: "۳ تا ۵ گرم ۲۰ دقیقه قبل تمرین در آب حل شود.",
                timings: [
                    { time: "۲۰ دقیقه قبل تمرین", desc: "بهبود استقامت عضلانی در ست‌های پرفشار" }
                ],
                warnings: "ایجاد سوزن‌سوزن شدن موقت در پوست بی‌خطر است."
            },
            {
                id: "genestar-citrulline-300",
                department: "supplements",
                image: "images/products/genestar-citrulline-300.svg",
                ingredients: ["citrulline_malate"],
                name: "سیترولین مالات خالص ژن استار ۳۰۰ گرمی",
                brand: "ژن استار (Genestar)",
                origin: "iran",
                category: "energy",
                subType: "citrulline",
                weight: "300 گرم",
                price: 740000,
                svg: render3DSupplementSVG("citrulline", "Genestar", "CITRULLINE", "#0284c7", "#67e8f9", "#0369a1"),
                purpose: "افزایش چشمگیر جریان خون، رگ‌زایی عضلانی (Vascularity) و دفع آمونیاک از بافت‌های عضلانی.",
                usage: "۳ تا ۵ گرم پودر حدود ۳۰ دقیقه قبل تمرین در آب.",
                timings: [
                    { time: "قبل از تمرین", desc: "پمپ عضلانی فوق‌العاده و رگ‌زایی" }
                ],
                warnings: "طعم ترش طبیعی دارد."
            },
            {
                id: "pnc-caffeine-200",
                department: "supplements",
                image: "images/products/pnc-caffeine-200.svg",
                ingredients: ["caffeine_anhydrous"],
                name: "قرص کافئین ۲۰۰ میلی‌گرم کارن",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "energy",
                subType: "caffeine",
                weight: "60 عدد",
                price: 240000,
                svg: render3DSupplementSVG("caff", "PNC", "CAFFEINE 200", "#78350f", "#fde047", "#451a03"),
                purpose: "افزایش فوری هوشیاری، مهار حس خستگی، افزایش انقباضات عضلانی و بالا بردن نرخ کالری‌سوزی.",
                usage: "یک قرص ۴۵ دقیقه قبل تمرین همراه آب.",
                timings: [
                    { time: "۴۵ دقیقه قبل تمرین", desc: "رسیدن کافئین به اوج غلظت خونی" }
                ],
                warnings: "در ساعات پایانی شب مصرف نشود."
            },
            {
                id: "cellucor-c4-180",
                department: "supplements",
                image: "images/products/cellucor-c4-180.svg",
                ingredients: ["preworkout_matrix", "beta_alanine_carnosyn", "citrulline_malate", "caffeine_anhydrous"],
                name: "پمپ سی ۴ اورجینال سلوکور (Cellucor C4)",
                brand: "Cellucor",
                origin: "foreign",
                category: "energy",
                subType: "stim",
                weight: "180 گرم",
                price: 2350000,
                svg: render3DSupplementSVG("pump", "Cellucor", "C4 PRE-WORKOUT", "#090d16", "#facc15", "#ca8a04"),
                purpose: "محبوب‌ترین پیش‌تمرین جهان، ایجاد تمرکز لیزری، انرژی بالا بدون افت ناگهانی و رگ‌زایی عضلات.",
                usage: "یک پیمانه ۲۰ تا ۳۰ دقیقه قبل تمرین در ۲۰۰ میلی‌لیتر آب.",
                timings: [
                    { time: "قبل تمرین", desc: "آماده‌سازی سیستم عصبی برای ست‌های سنگین" }
                ],
                warnings: "قبل خواب مصرف نشود."
            },

            // ۱۰. کاهش وزن، ال‌کارنیتین و CLA
            {
                id: "pnc-l-carnitine-100",
                department: "supplements",
                image: "images/products/pnc-l-carnitine-100.svg",
                ingredients: ["l_carnitine_tartrate"],
                name: "قرص ال کارنیتین ۱۰۰۰ میلی‌گرم کارن",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "fatburn",
                subType: "carnitine",
                weight: "100 عدد",
                price: 480000,
                svg: render3DSupplementSVG("carnitine", "PNC", "L-CARNITINE", "#ea580c", "#fed7aa", "#9a3412"),
                purpose: "انتقال اسیدهای چرب به میتوکندری سلول برای سوزاندن چربی و افزایش توان هوازی.",
                usage: "۱ تا ۲ عدد قبل از فعالیت ورزشی یا تمرینات کاردیو.",
                timings: [
                    { time: "۳۰ دقیقه قبل ورزش هوازی", desc: "بیشترین نرخ تبدیل چربی به انرژی" }
                ],
                warnings: "افراد با سابقه تشنج یا کم‌کاری تیروئید مشورت پزشکی بگیرند."
            },
            {
                id: "genestar-cla-1000",
                department: "supplements",
                image: "images/products/genestar-cla-1000.svg",
                ingredients: ["cla_pure"],
                name: "کپسول سی ال ای ۱۰۰۰ میلی‌گرم ژن استار (CLA)",
                brand: "ژن استار (Genestar)",
                origin: "iran",
                category: "fatburn",
                subType: "cla",
                weight: "90 عدد",
                price: 760000,
                svg: render3DSupplementSVG("cla", "Genestar", "CLA 1000", "#ca8a04", "#fef08a", "#713f12"),
                purpose: "اسید لینولئیک کونژوگه جهت کاهش ذخایر چربی شکمی و پهلوها و مهار آنزیم لیپوپروتئین لیپاز.",
                usage: "۱ کپسول همراه با هر وعده غذایی اصلی (۳ بار در روز).",
                timings: [
                    { time: "همراه با ناهار و شام", desc: "جلوگیری از انباشت چربی غذایی" }
                ],
                warnings: "در دوران بارداری و شیردهی منع مصرف دارد."
            },
            {
                id: "muscletech-hydroxycut-110",
                department: "supplements",
                image: "images/products/muscletech-hydroxycut-110.svg",
                ingredients: ["thermo_extracts", "caffeine_anhydrous", "l_carnitine_tartrate"],
                name: "هیدروکسی‌کات الیت ماسل تک (Hydroxycut Elite)",
                brand: "MuscleTech",
                origin: "foreign",
                category: "fatburn",
                subType: "thermo",
                weight: "110 عدد",
                price: 2400000,
                svg: render3DSupplementSVG("thermo", "MuscleTech", "HYDROXYCUT", "#0f172a", "#ef4444", "#991b1b"),
                purpose: "چربی‌سوز ترموژنیک هاردکور، افزایش دمای درونی بدن، سرکوب اشتهای کاذب و افزایش کالری‌سوزی پایه.",
                usage: "۱ عدد در روز قبل از وعده صبحانه یا تمرین.",
                timings: [
                    { time: "صبح قبل تمرین", desc: "تعریق شدید و افزایش کالری‌سوزی" }
                ],
                warnings: "بسیار قوی است؛ افراد حساس به کافئین نباید مصرف کنند."
            },

            // ۱۱. سلامت، هورمونی، ZMA، تریبولوس و ALA
            {
                id: "pnc-zma-60",
                department: "supplements",
                image: "images/products/pnc-zma-60.svg",
                ingredients: ["zma_complex"],
                name: "کپسول زد ام ای کارن (PNC ZMA)",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "health",
                subType: "zma",
                weight: "60 عدد",
                price: 490000,
                svg: render3DSupplementSVG("zma", "PNC", "ZMA NIGHT", "#4338ca", "#a5b4fc", "#312e81"),
                purpose: "ترکیب ثبت‌شده روی (زینک)، منیزیم و ویتامین B6 جهت بهبود کیفیت خواب عمیق، تقویت ترشح تستوسترون شبانه و کاهش گرفتگی عضلات.",
                usage: "۲ کپسول ۳۰ تا ۶۰ دقیقه قبل از خواب با معده نسبتاً خالی.",
                timings: [
                    { time: "قبل از خواب", desc: "بهبود ریکاوری عصبی و هورمون‌های آنابولیک" }
                ],
                warnings: "همزمان با لبنیات یا کلسیم مصرف نشود (کلسیم مانع جذب زینک است)."
            },
            {
                id: "genestar-tribulus-650",
                department: "supplements",
                image: "images/products/genestar-tribulus-650.svg",
                ingredients: ["tribulus_terrestris"],
                name: "کپسول تریبولوس ۶۵۰ ژن استار (Tribulus)",
                brand: "ژن استار (Genestar)",
                origin: "iran",
                category: "health",
                subType: "tribulus",
                weight: "60 عدد",
                price: 580000,
                svg: render3DSupplementSVG("tribulus", "Genestar", "TRIBULUS 650", "#15803d", "#86efac", "#14532d"),
                purpose: "عصاره استاندارد گیاه خارخاسک با ساپونین بالا جهت پشتیبانی طبیعی از تولید تستوسترون، نشاط و توان عضلانی.",
                usage: "روزانه ۱ تا ۲ کپسول همراه با غذا.",
                timings: [
                    { time: "صبح و قبل تمرین", desc: "افزایش انگیزه و قدرت عضلانی" }
                ],
                warnings: "برای افراد زیر ۱۸ سال توصیه نمی‌شود."
            },
            {
                id: "ala-300-pure",
                department: "supplements",
                image: "images/products/ala-300-pure.svg",
                ingredients: ["ala_antioxidant"],
                name: "کپسول آلفا لیپوئیک اسید ۳۰۰ (ALA 300mg)",
                brand: "کارن (PNC)",
                origin: "iran",
                category: "health",
                subType: "ala",
                weight: "60 عدد",
                price: 460000,
                svg: render3DSupplementSVG("ala", "PNC", "ALA 300", "#7e22ce", "#d8b4fe", "#581c87"),
                purpose: "آنتی‌اکسیدان قوی محلول در آب و چربی، بهبود حساسیت به انسولین و راندن مواد غذایی و کراتین به درون سلول‌های عضلانی.",
                usage: "یک کپسول همراه با وعده کربوهیدراتی یا بعد تمرین.",
                timings: [
                    { time: "همراه وعده کربوهیدراتی", desc: "بهبود جذب گلوکز در عضلات" }
                ],
                warnings: "در صورت افت قند خون با کمی آبمیوه میل شود."
            },
            {
                id: "vitap-daily-multi-60",
                department: "supplements",
                image: "images/products/vitap-daily-multi-60.svg",
                ingredients: ["daily_multivitamin"],
                name: "مولتی ویتامین و مینرال دیلی ویتاپی",
                brand: "ویتاپی (VitaP)",
                origin: "iran",
                category: "health",
                subType: "multi",
                weight: "60 عدد",
                price: 290000,
                svg: render3DSupplementSVG("multi", "VitaP", "DAILY MULTI", "#0284c7", "#bae6fd", "#0369a1"),
                purpose: "تامین تمام ریزمغذی‌ها، زینک، منیزیم، ویتامین C و گروه B برای رفع خستگی ورزشکار.",
                usage: "روزانه یک عدد قرص همراه با وعده غذایی.",
                timings: [
                    { time: "همراه با ناهار", desc: "حداکثر جذب ویتامین‌های محلول در چربی" }
                ],
                warnings: "با معده خالی خورده نشود."
            }
        ];"""
men_code = """[
            {
                        "id": "men-tee-nike-pro",
                        "name": "تیشرت فیتنس درای‌فیت نایک پرو (Nike Pro Combat Fit)",
                        "brand": "Nike",
                        "department": "apparel_men",
                        "category": "tshirt",
                        "subType": "compression",
                        "price": 1280000,
                        "weight": "وزن خالص: ۱۸۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/men-tee-nike-pro.svg",
                        "specs": [
                                    "dryfit",
                                    "breathable",
                                    "anti_odor",
                                    "4way_stretch"
                        ],
                        "sizes": [
                                    "M",
                                    "L",
                                    "XL",
                                    "2XL"
                        ],
                        "material": "۸۸٪ پلی‌استر بازیافتی، ۱۲٪ اسپندکس",
                        "purpose": "پارچه اختصاصی Dri-FIT نایک با تهویه فوق‌العاده در زیر بغل و پشت، مدیریت رطوبت عرق و تناسب فشرده با خطوط عضلات سینه و سرشانه.",
                        "usage": "مناسب تمرینات پرفشار بدنسازی، هوازی و دویدن در سالن.",
                        "warnings": "شستشو با آب سرد و بدون خشک‌کن حرارتی انجام شود."
            },
            {
                        "id": "men-tank-venum",
                        "name": "رکابی فیتنس کات عضلانی ونوم (Venum Giant Tank Top)",
                        "brand": "Venum",
                        "department": "apparel_men",
                        "category": "tanktop",
                        "subType": "stringer",
                        "price": 950000,
                        "weight": "وزن خالص: ۱۴۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/men-tank-venum",
                        "specs": [
                                    "pure_cotton",
                                    "deep_cut",
                                    "breathable",
                                    "reinforced_seams"
                        ],
                        "sizes": [
                                    "L",
                                    "XL"
                        ],
                        "material": "۱۰۰٪ پنبه شانه شده پریمیوم با رنگ ثابت ژاپنی",
                        "purpose": "طراحی استرینگر با برش عمیق زیربغل و پشت قهرمانی Y-Back برای آزادی ۱۰۰٪ دامنه حرکتی در حرکات زیربغل و سرشانه.",
                        "usage": "بهترین گزینه برای روز تمرین سینه، سرشانه و زیربغل.",
                        "warnings": "پشت‌ورو شسته شود تا چاپ لوگوی ونوم آسیب نبیند."
            },
            {
                        "id": "men-shorts-ua",
                        "name": "شلوارک کشسانی ۴ جهته آندرآرمور (Under Armour 7\" Shorts)",
                        "brand": "Under Armour",
                        "department": "apparel_men",
                        "category": "shorts",
                        "subType": "4way",
                        "price": 1450000,
                        "weight": "وزن خالص: ۲۱۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/men-shorts-ua.svg",
                        "specs": [
                                    "4way_stretch",
                                    "zip_pocket",
                                    "breathable",
                                    "quick_dry"
                        ],
                        "sizes": [
                                    "M",
                                    "L",
                                    "XL"
                        ],
                        "material": "پلی‌استر الترا لایت با تکنولوژی HeatGear",
                        "purpose": "دارای جیب مخفی زیپ‌دار ضدآب برای گوشی همراه، بند کشی قابل تنظیم و منافذ لیزری تهویه در دو طرف ران.",
                        "usage": "تمرینات اسکوات، کراسفیت و دویدن استقامتی.",
                        "warnings": "اتوکشی مستقیم روی بند و منافذ لیزری ممنوع است."
            },
            {
                        "id": "men-pants-monsta",
                        "name": "شلوار اسلش تمرینی بدنسازی مونسلو (Monsta Gym Joggers)",
                        "brand": "Monsta",
                        "department": "apparel_men",
                        "category": "pants",
                        "subType": "heavy_cotton",
                        "price": 1850000,
                        "weight": "وزن خالص: ۴۲۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/men-pants-monsta.svg",
                        "specs": [
                                    "pure_cotton",
                                    "heavy_duty",
                                    "deep_pockets",
                                    "ankle_cuff"
                        ],
                        "sizes": [
                                    "L",
                                    "XL",
                                    "2XL"
                        ],
                        "material": "دورس ۳ نخ پنبه خارخورده ضخیم با گرم‌بالا",
                        "purpose": "دمپای کش‌باف مقاوم، فاق ارگونومیک آزاد بدون کشش مزاحم در حرکات پا و گرم نگه داشتن مفاصل زانو حین ست‌های سنگین.",
                        "usage": "تمرین در فصول سرد و گرم کردن اولیه عضلات.",
                        "warnings": "با لباس‌های تیره شسته شود."
            },
            {
                        "id": "men-tee-gymshark",
                        "name": "تیشرت سیملس بدون درز جیم‌شارک (Gymshark Onyx Seamless)",
                        "brand": "Gymshark",
                        "department": "apparel_men",
                        "category": "tshirt",
                        "subType": "seamless",
                        "price": 1650000,
                        "weight": "وزن خالص: ۱۹۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/men-tee-gymshark.svg",
                        "specs": [
                                    "seamless",
                                    "jacquard_mesh",
                                    "anti_odor",
                                    "slim_fit"
                        ],
                        "sizes": [
                                    "M",
                                    "L",
                                    "XL"
                        ],
                        "material": "۶۵٪ نایلون، ۳۰٪ پلی‌استر، ۵٪ الاستین",
                        "purpose": "بافت ژاکارد بدون هیچ‌گونه درز جانبی برای جلوگیری کامل از سایش پوست، با خطوط سایه‌روشن برجسته‌کننده عضلات شکم و بازو.",
                        "usage": "تمرینات حرفه‌ای فیگورگیری و بدنسازی سنگین.",
                        "warnings": "از تماس با چسب‌های زبر مچ‌بند و کمربند محافظت شود."
            },
            {
                        "id": "men-tank-golds",
                        "name": "رکابی کلاه‌دار تمرین بدنسازی گلدز جیم (Gold's Gym Hoodie)",
                        "brand": "Gold's Gym",
                        "department": "apparel_men",
                        "category": "tanktop",
                        "subType": "hoodie",
                        "price": 1100000,
                        "weight": "وزن خالص: ۲۴۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/men-tank-golds.svg",
                        "specs": [
                                    "pure_cotton",
                                    "hooded",
                                    "oversized",
                                    "hardcore_style"
                        ],
                        "sizes": [
                                    "M",
                                    "L",
                                    "XL"
                        ],
                        "material": "پنبه سنگین ۱۰۰٪ نرم با بافت تنفس‌پذیر",
                        "purpose": "دارای کلاه تمرینی شیک برای تمرکز حداکثری حین گوش دادن به موسیقی در باشگاه با لوگوی کلاسیک وزنه بردار گلدز جیم.",
                        "usage": "شروع ست‌های سنگین پرس سینه و ددلیفت.",
                        "warnings": "شستشو با آب حداکثر ۳۰ درجه سانتی‌گراد."
            }
]"""
women_code = """[
            {
                        "id": "women-leg-lulu",
                        "name": "لگینگ ورزشی فاق‌بلند بدون درز لولولمون (Lululemon Align)",
                        "brand": "Lululemon",
                        "department": "apparel_women",
                        "category": "leg",
                        "subType": "high_waist",
                        "price": 2450000,
                        "weight": "وزن خالص: ۲۰۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/women-leg-lulu.svg",
                        "specs": [
                                    "high_waist",
                                    "buttery_soft",
                                    "squat_proof",
                                    "hidden_pocket"
                        ],
                        "sizes": [
                                    "XS",
                                    "S",
                                    "M",
                                    "L"
                        ],
                        "material": "پارچه اختصاصی Nulu™ با لمس ابریشمی بدون وزن",
                        "purpose": "۱۰۰٪ اسکات‌پروف (بدون هیچ دید به داخل حتی در عمیق‌ترین کشش‌ها)، فاق بسیار بلند با جمع‌کنندگی ملایم شکم و پهلو.",
                        "usage": "یوگا، پیلاتس، فیتنس و تمرینات سنگین پا.",
                        "warnings": "با نرم‌کننده لباس شسته نشود."
            },
            {
                        "id": "women-bra-nike",
                        "name": "نیم‌تنه ورزشی کاپ‌دار نایک پرو ساپورت (Nike Pro Sports Bra)",
                        "brand": "Nike",
                        "department": "apparel_women",
                        "category": "nim_tane",
                        "subType": "padded_bra",
                        "price": 1150000,
                        "weight": "وزن خالص: ۱۳۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/women-bra-nike.svg",
                        "specs": [
                                    "medium_support",
                                    "removable_pads",
                                    "dri_fit",
                                    "racerback"
                        ],
                        "sizes": [
                                    "S",
                                    "M",
                                    "L"
                        ],
                        "material": "۸۲٪ پلی‌استر بازیافتی، ۱۸٪ اسپندکس",
                        "purpose": "دارای پدهای اسفنجی ضدتغییرشکل با ساپورت متوسط رو به بالا برای جلوگیری از لرزش حین تمرینات طناب‌زنی و پرش.",
                        "usage": "تمرینات فیتنس، تی‌آرایکس و ایروبیک.",
                        "warnings": "پدها پیش از شستشو خارج و جداگانه شسته شوند."
            },
            {
                        "id": "women-skirt-gymshark",
                        "name": "دامن ورزشی دو تکه شلوارک‌دار جیم‌شارک (Gymshark Skirt)",
                        "brand": "Gymshark",
                        "department": "apparel_women",
                        "category": "daman",
                        "subType": "2in1_skirt",
                        "price": 1350000,
                        "weight": "وزن خالص: ۱۹۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/women-skirt-gymshark.svg",
                        "specs": [
                                    "built_in_shorts",
                                    "lightweight",
                                    "pleated",
                                    "ball_pocket"
                        ],
                        "sizes": [
                                    "S",
                                    "M"
                        ],
                        "material": "پلی‌استر فوق سبک تنفس‌پذیر با لایه داخلی اسپندکس",
                        "purpose": "طراحی مدرن با لایه شلوارک جذب ضدسایش در زیر دامن و جیب معکوس برای حمل وسایل کوچک بدون بیرون‌زدگی.",
                        "usage": "تنیس، بدمینتون، کراسفیت و دویدن در فضای باز.",
                        "warnings": "بدون سفیدکننده شسته شود."
            },
            {
                        "id": "women-top-ua",
                        "name": "بالاتنه آستین‌بلند انگشتی آندرآرمور (Under Armour ColdGear)",
                        "brand": "Under Armour",
                        "department": "apparel_women",
                        "category": "balatane",
                        "subType": "long_sleeve",
                        "price": 1650000,
                        "weight": "وزن خالص: ۲۱۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/women-top-ua.svg",
                        "specs": [
                                    "thumbholes",
                                    "thermal_control",
                                    "anti_microbial",
                                    "slim_fit"
                        ],
                        "sizes": [
                                    "XS",
                                    "S",
                                    "M",
                                    "L"
                        ],
                        "material": "پارچه دولایه با کرک نرم داخلی و سطح صیقلی بیرونی",
                        "purpose": "سرآستین مجهز به سوراخ شست (Thumbholes) برای جلوگیری از بالا رفتن آستین و حفظ کامل دمای دست در طول تمرین.",
                        "usage": "تمرین در فضای باز صبحگاهی و سالن‌های ورزشی خنک.",
                        "warnings": "در دمای ۳۰ درجه شسته شود."
            },
            {
                        "id": "women-crop-puma",
                        "name": "کراپ‌تاپ ورزشی بند متقاطع پوما (Puma Training Crop)",
                        "brand": "Puma",
                        "department": "apparel_women",
                        "category": "nim_tane",
                        "subType": "crop_top",
                        "price": 980000,
                        "weight": "وزن خالص: ۱۱۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/women-crop-puma.svg",
                        "specs": [
                                    "strappy_back",
                                    "elastic_band",
                                    "drycell",
                                    "crop_cut"
                        ],
                        "sizes": [
                                    "S",
                                    "M"
                        ],
                        "material": "۸۹٪ پلی‌استر، ۱۱٪ الاستین با فناوری DryCELL",
                        "purpose": "طراحی بندهای ظریف ضربدری در پشت جهت انتقال حداکثر جریان هوا و جلوگیری از تعریق پشت گردن.",
                        "usage": "تمرینات پیلاتس، بادی‌پامپ و تمرین با وزنه.",
                        "warnings": "خشک‌شویی نشود."
            }
]"""
gear_code = """[
            {
                        "id": "gear-wrist-harbinger",
                        "name": "مچ‌بند چسبی سنگین ۱۸ اینچ هاربینگر (Harbinger Pro Wraps)",
                        "brand": "Harbinger",
                        "department": "gym_gear",
                        "category": "mochband",
                        "subType": "wraps",
                        "price": 850000,
                        "weight": "وزن جفت: ۲۲۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/gear-wrist-harbinger.svg",
                        "specs": [
                                    "heavy_elastic",
                                    "thumb_loop",
                                    "wide_velcro",
                                    "pro_support"
                        ],
                        "sizes": [
                                    "فری سایز ۱۸ اینچ"
                        ],
                        "material": "کش الاستیک فشرده نظامی با بند انگشت شست",
                        "purpose": "تثبیت ۱۰۰٪ استخوان مچ دست در حرکات سنگین پرس سینه، سرشانه هالتر و اورهد بدون قطع جریان خون.",
                        "usage": "پاورلیفتینگ، بدنسازی قدرتی و ست‌های حداکثری.",
                        "warnings": "در پایان ست برای برگشت جریان خون باز شود."
            },
            {
                        "id": "gear-belt-rdx",
                        "name": "کمربند چرم گاوی ۲ لایه پاورلیفتینگ RDX (Leather Belt 4\")",
                        "brand": "RDX",
                        "department": "gym_gear",
                        "category": "belt",
                        "subType": "leather_belt",
                        "price": 3200000,
                        "weight": "وزن خالص: ۱۱۵۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/gear-belt-rdx.svg",
                        "specs": [
                                    "genuine_leather",
                                    "double_prong",
                                    "lumbar_pad",
                                    "heavy_stitching"
                        ],
                        "sizes": [
                                    "M",
                                    "L",
                                    "XL"
                        ],
                        "material": "چرم طبیعی گاوی ضخیم روغن‌خورده با سگک استیل دوتایی",
                        "purpose": "ایجاد حداکثر فشار درون‌شکمی (Intra-abdominal Pressure) برای محافظت از دیسک‌های ستون فقرات در اسکات و ددلیفت سنگین.",
                        "usage": "تمرینات پاورلیفتینگ، رکوردگیری ددلیفت و اسکات بالای ۱۰۰ کیلوگرم.",
                        "warnings": "دور از رطوبت مستقیم و تابش آفتاب نگهداری شود."
            },
            {
                        "id": "gear-shaker-spider",
                        "name": "شیکر استیل دوجداره دکمه‌ای اسپایدر ۹۰۰ میل (Spider Steel)",
                        "brand": "Spider",
                        "department": "gym_gear",
                        "category": "qomqome",
                        "subType": "steel_shaker",
                        "price": 750000,
                        "weight": "ظرفیت: ۹۰۰ میلی‌لیتر",
                        "origin": "foreign",
                        "image": "images/products/gear-shaker-spider.svg",
                        "specs": [
                                    "double_wall_steel",
                                    "odorless",
                                    "leak_proof",
                                    "spring_ball"
                        ],
                        "sizes": [
                                    "۹۰۰ میلی‌لیتر"
                        ],
                        "material": "استیل ضدزنگ ۳۰۴ ضدبو با درب پلی‌پروپیلن فودگرید",
                        "purpose": "حفظ دمای آب سرد تا ۲۴ ساعت، حل کامل غلیظ‌ترین پودرهای وی و گینر بدون گلوله‌شدن با فنر استیل ژاپنی بدون بو گرفتن پس از شستشو.",
                        "usage": "میکسر مکمل‌های پروتئینی، BCAA و نگهداری نوشیدنی یخ در طول تمرین.",
                        "warnings": "در مایکروویو یا ماشین ظرفشویی قرار داده نشود."
            },
            {
                        "id": "gear-jug-hydra",
                        "name": "گالن انگیزشی آب ۲.۲ لیتری هیدراپک (HydraPak 2.2L Jug)",
                        "brand": "HydraPak",
                        "department": "gym_gear",
                        "category": "qomqome",
                        "subType": "water_jug",
                        "price": 620000,
                        "weight": "ظرفیت: ۲۲۰۰ میلی‌لیتر",
                        "origin": "foreign",
                        "image": "images/products/gear-jug-hydra.svg",
                        "specs": [
                                    "bpa_free",
                                    "time_marker",
                                    "sturdy_handle",
                                    "wide_mouth"
                        ],
                        "sizes": [
                                    "۲.۲ لیتر حجم کامل روزانه"
                        ],
                        "material": "پلاستیک پلیمر نشکن ۱۰۰٪ عاری از بیسفنول آ (BPA Free)",
                        "purpose": "خط‌کشی انگیزشی ساعت‌به‌ساعت برای تامین هیدراتاسیون ۲.۲ لیتری روزانه ورزشکاران، دسته ارگونومیک محکم و درب ضدنشت متصل به بند.",
                        "usage": "مصرف روزانه آب در باشگاه و دوره‌های مصرف کراتین.",
                        "warnings": "از ریختن آب جوش بالای ۶۰ درجه خودداری شود."
            },
            {
                        "id": "gear-spray-sanisport",
                        "name": "اسپری تنظیف و ضدعفونی تجهیزات ورزشی (Sanisport Gym Spray)",
                        "brand": "SaniSport",
                        "department": "gym_gear",
                        "category": "spray",
                        "subType": "clean_spray",
                        "price": 280000,
                        "weight": "حجم: ۴۰۰ میلی‌لیتر",
                        "origin": "foreign",
                        "image": "images/products/gear-spray-sanisport.svg",
                        "specs": [
                                    "kills_99_bacteria",
                                    "deodorizer",
                                    "equipment_safe",
                                    "eucalyptus"
                        ],
                        "sizes": [
                                    "۴۰۰ میلی‌لیتر اسپری پمپی"
                        ],
                        "material": "فرمول اتانول زیستی، روغن اوکالیپتوس و ترکیبات بدون آسیب به چرم",
                        "purpose": "ضدعفونی فوری تشک تمرین، دستکش، روکش چرم نیمکت‌های باشگاه و پاکسازی بوی نامطبوع عرق بدون پوساندن رویه تجهیزات.",
                        "usage": "قبل و بعد از استفاده از تجهیزات مشترک باشگاه و کفش ورزشی.",
                        "warnings": "از تماس با چشم یا استنشاق مستقیم پرهیز شود."
            },
            {
                        "id": "gear-straps-schiek",
                        "name": "بند لیفت پنبه‌ای پددار حرفه‌ای شیبا (Schiek Lifting Straps)",
                        "brand": "Schiek",
                        "department": "gym_gear",
                        "category": "mochband",
                        "subType": "straps",
                        "price": 480000,
                        "weight": "وزن جفت: ۱۲۰ گرم",
                        "origin": "foreign",
                        "image": "images/products/gear-straps-schiek.svg",
                        "specs": [
                                    "neoprene_pad",
                                    "heavy_duty_cotton",
                                    "extra_long",
                                    "anti_slip"
                        ],
                        "sizes": [
                                    "طول ۲۱ اینچ"
                        ],
                        "material": "پنبه الیاف تقویت‌شده سنگین با پد نئوپرن نرم محافظ مچ",
                        "purpose": "حذف خستگی ساعد و پنجه در ددلیفت، بارفیکس و شراگ تا وزن بالای ۲۰۰ کیلوگرم بدون لیز خوردن از دور میله هالتر.",
                        "usage": "حرکات کششی سنگین ددلیفت، زیربغل هالتر خم و بارفیکس.",
                        "warnings": "قابل شستشو با دست و صابون مایع."
            }
]"""
render_svg_func = """function render3DSupplementSVG(type, brandName, subText, mainColor, accentColor, capColor = "#1e293b") {
            const safeBrand = brandName.replace(/<[^>]*>?/gm, '').split(' ')[0];
            return `
            <svg viewBox="0 0 160 200" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="tubGrad_${safeBrand}_${type}" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="${mainColor}" stop-opacity="0.8"/>
                        <stop offset="25%" stop-color="#ffffff" stop-opacity="0.35"/>
                        <stop offset="45%" stop-color="${mainColor}"/>
                        <stop offset="80%" stop-color="#0a0f1d"/>
                        <stop offset="100%" stop-color="#04070e"/>
                    </linearGradient>

                    <linearGradient id="capGrad_${safeBrand}_${type}" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="${capColor}"/>
                        <stop offset="35%" stop-color="#cbd5e1" stop-opacity="0.6"/>
                        <stop offset="70%" stop-color="${capColor}"/>
                        <stop offset="100%" stop-color="#090d16"/>
                    </linearGradient>

                    <linearGradient id="shine_${type}" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#ffffff" stop-opacity="0.25"/>
                        <stop offset="50%" stop-color="#ffffff" stop-opacity="0"/>
                        <stop offset="100%" stop-color="#000000" stop-opacity="0.3"/>
                    </linearGradient>
                </defs>

                <ellipse cx="80" cy="188" rx="60" ry="10" fill="#000000" opacity="0.6" filter="blur(4px)"/>
                <rect x="42" y="24" width="76" height="14" rx="3" fill="#1e293b"/>
                <rect x="36" y="10" width="88" height="20" rx="6" fill="url(#capGrad_${safeBrand}_${type})"/>
                <line x1="45" y1="12" x2="45" y2="28" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
                <line x1="60" y1="12" x2="60" y2="28" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
                <line x1="80" y1="12" x2="80" y2="28" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
                <line x1="100" y1="12" x2="100" y2="28" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
                <line x1="115" y1="12" x2="115" y2="28" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>

                <path d="M28 40 L132 40 C140 40 144 48 144 58 L138 174 C138 182 130 186 122 186 L38 186 C30 186 22 182 22 174 L16 58 C16 48 20 40 28 40 Z" fill="url(#tubGrad_${safeBrand}_${type})"/>

                <rect x="23" y="65" width="114" height="95" rx="8" fill="#0c121e" opacity="0.95"/>
                <rect x="23" y="65" width="114" height="95" rx="8" fill="url(#shine_${type})"/>
                <rect x="23" y="68" width="114" height="7" fill="${accentColor}"/>

                <text x="80" y="88" font-size="11" font-weight="900" fill="${accentColor}" text-anchor="middle" font-family="Arial, sans-serif" letter-spacing="1">${safeBrand.toUpperCase()}</text>
                <line x1="38" y1="94" x2="122" y2="94" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
                <text x="80" y="118" font-size="12" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Arial, sans-serif">${subText}</text>
                <text x="80" y="132" font-size="8.5" font-weight="700" fill="${accentColor}" text-anchor="middle" font-family="Arial, sans-serif">100% ORIGINAL</text>

                <circle cx="80" cy="148" r="6" fill="${accentColor}" opacity="0.8"/>
                <text x="80" y="150.5" font-size="6" font-weight="900" fill="#ffffff" text-anchor="middle">✓</text>
            </svg>
            `;
        }

        
        // ساختار دسته‌بندی ترکیبات و مواد مؤثره با قابلیت آکاردئونی (Minimize / Maximize)
        const IngredientGroups = [
            {
                id: "protein_bases",
                name: "پروتئین‌ها و منابع اصلی",
                icon: "🥛",
                items: [
                    { id: "whey_concentrate", name: "پروتئین وی کنسانتره" },
                    { id: "whey_isolate", name: "پروتئین وی ایزوله ۹۰٪" },
                    { id: "whey_hydrolyzed", name: "پروتئین وی هیدرولیزه" },
                    { id: "casein_micellar", name: "کازئین میسلار کندجذب" },
                    { id: "beef_isolate", name: "پروتئین بیف ایزوله گاو" },
                    { id: "egg_albumin", name: "سفیده تخم‌مرغ (آلبومین)" },
                    { id: "plant_pea_soy", name: "پروتئین گیاهی (وگان)" },
                    { id: "protein_blend", name: "ماتریکس پروتئینی ترکیبی" }
                ]
            },
            {
                id: "aminos",
                name: "آمینواسیدهای شاخه‌دار و آنابولیک",
                icon: "🧪",
                items: [
                    { id: "bcaa_branched", name: "بی سی ای ای (BCAA 2:1:1)" },
                    { id: "glutamine_pure", name: "ال-گلوتامین میکرونیزه" },
                    { id: "arginine_hcl", name: "ال-آرژنین ۱۰۰۰ نیتریک اکساید" },
                    { id: "hmb_pure", name: "اچ ام بی خالص (HMB)" },
                    { id: "amino_peptides", name: "پپتیدهای پودر آمینو وی" }
                ]
            },
            {
                id: "creatine_atp",
                name: "کراتین و افزایش قدرت عضلانی",
                icon: "⚡",
                items: [
                    { id: "creatine_mono", name: "کراتین مونوهیدرات دارویی" },
                    { id: "creatine_creapure", name: "کراتین کریپیور خالص آلمان" },
                    { id: "creatine_complex", name: "کمپلکس کراتین پیشرفته سل تک" }
                ]
            },
            {
                id: "energy_pump",
                name: "پمپ عروقی، انرژی و تاخیر خستگی",
                icon: "🔥",
                items: [
                    { id: "beta_alanine_carnosyn", name: "بتا آلانین کارنوسین" },
                    { id: "citrulline_malate", name: "سیترولین مالات ۲:۱" },
                    { id: "caffeine_anhydrous", name: "کافئین خالص ۲۰۰ میلی‌گرم" },
                    { id: "preworkout_matrix", name: "فرمول پمپ انفجاری C4" }
                ]
            },
            {
                id: "carbs_gainer",
                name: "کربوهیدرات و کالری افزایش وزن",
                icon: "🌾",
                items: [
                    { id: "complex_carbs", name: "کربوهیدرات مالتودکسترین خالص" },
                    { id: "high_calorie_gainer", name: "کالری مس گینر حجم سنگین" }
                ]
            },
            {
                id: "fatburn_cut",
                name: "چربی‌سوزی، CLA و کات عضلانی",
                icon: "🎯",
                items: [
                    { id: "l_carnitine_tartrate", name: "ال-کارنیتین تارتارات ۱۰۰۰" },
                    { id: "cla_pure", name: "سی ال ای ۱۰۰۰ خالص" },
                    { id: "thermo_extracts", name: "ترموژنیک هیدروکسی‌کات الیت" },
                    { id: "ala_antioxidant", name: "آلفا لیپوئیک اسید ۳۰۰ (ALA)" }
                ]
            },
            {
                id: "health_hormonal",
                name: "تستوسترون، ریکاوری خواب و مولتی",
                icon: "⭐",
                items: [
                    { id: "zma_complex", name: "زد ام ای (روی، منیزیم، B6)" },
                    { id: "tribulus_terrestris", name: "تریبولوس ترستریس ۶۵۰ ساپونین" },
                    { id: "daily_multivitamin", name: "مولتی‌ویتامین و مینرال ورزشی" }
                ]
            }
        ];

        // مپ جامع برای استخراج نام سریع هر ترکیب
        const allIngredientsMap = {};
        IngredientGroups.forEach(g => {
            g.items.forEach(it => {
                allIngredientsMap[it.id] = { ...it, group: g.id, groupName: g.name, groupIcon: g.icon };
            });
        });

        // مپ ارتباط هوشمند بین کلیک روی سر‌دسته‌ها/زیردسته‌ها و تیک‌خوردن خودکار چک‌باکس‌ها
        const CategoryToIngredientsMap = {
            "protein": ["whey_concentrate", "whey_isolate", "whey_hydrolyzed", "casein_micellar", "beef_isolate", "egg_albumin", "plant_pea_soy", "protein_blend"],
            "gainer": ["high_calorie_gainer", "complex_carbs"],
            "creatine": ["creatine_mono", "creatine_creapure", "creatine_complex"],
            "amino": ["bcaa_branched", "glutamine_pure", "arginine_hcl", "hmb_pure", "amino_peptides"],
            "energy": ["beta_alanine_carnosyn", "citrulline_malate", "caffeine_anhydrous", "preworkout_matrix"],
            "fatburn": ["l_carnitine_tartrate", "cla_pure", "thermo_extracts", "ala_antioxidant"],
            "health": ["zma_complex", "tribulus_terrestris", "ala_antioxidant", "daily_multivitamin"],

            "protein_concentrate": ["whey_concentrate"],
            "protein_isolate": ["whey_isolate"],
            "protein_hydrolyzed": ["whey_hydrolyzed"],
            "protein_casein": ["casein_micellar"],
            "protein_blend": ["protein_blend", "whey_concentrate"],
            "protein_beef": ["beef_isolate"],
            "protein_egg": ["egg_albumin"],
            "protein_plant": ["plant_pea_soy"],

            "gainer_mass": ["high_calorie_gainer"],
            "gainer_lean": ["high_calorie_gainer", "whey_isolate"],
            "gainer_carbo": ["complex_carbs"],

            "creatine_monohydrate": ["creatine_mono"],
            "creatine_micronized": ["creatine_mono"],
            "creatine_complex": ["creatine_complex"],
            "creatine_beta_creatine": ["creatine_mono", "beta_alanine_carnosyn"],
            "creatine_creapure": ["creatine_creapure"],

            "amino_amino_whey": ["amino_peptides"],
            "amino_bcaa": ["bcaa_branched"],
            "amino_glutamine": ["glutamine_pure"],
            "amino_arginine": ["arginine_hcl"],
            "amino_hmb": ["hmb_pure"],
            "amino_amino_energy": ["bcaa_branched", "caffeine_anhydrous"],

            "energy_stim": ["preworkout_matrix", "caffeine_anhydrous"],
            "energy_citrulline": ["citrulline_malate"],
            "energy_beta_alanine": ["beta_alanine_carnosyn"],
            "energy_caffeine": ["caffeine_anhydrous"],

            "fatburn_carnitine": ["l_carnitine_tartrate"],
            "fatburn_cla": ["cla_pure"],
            "fatburn_thermo": ["thermo_extracts", "caffeine_anhydrous"],

            "health_zma": ["zma_complex"],
            "health_tribulus": ["tribulus_terrestris"],
            "health_ala": ["ala_antioxidant"],
            "health_multi": ["daily_multivitamin"]
        };

        // لیست ترکیبات تیک‌خورده فعلی (خالی = همه ترکیبات مجاز)
        let selectedIngredients = [];
        let openGroupsSet = new Set(["protein_bases"]); // پیش‌فرض اولین گروه باز باشد

        // دیتابیس فوق‌العاده غنی شامل تمام مدل‌های دقیق پروتئین (بیف، سفیده تخم‌مرغ، وگان، ایزوله، کنسانتره، هیدرولیزه، کازئین و ترکیبی) و سایر دسته‌ها"""

print("Data packed ready for write.")
