-- =========================================================================
-- دیتابیس جامع فروشگاه مکمل، پوشاک و تجهیزات ورزشی (Supabase PostgreSQL)
-- شامل جداول، قوانین امنیتی (RLS)، تابع کسر انبار و کل ۵۷ محصول کاتالوگ
-- =========================================================================

-- فعال‌سازی افزونه UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ۱. جدول محصولات فروشگاه (Store Products)
CREATE TABLE IF NOT EXISTS store_products (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    department VARCHAR(50) DEFAULT 'supplements',
    category VARCHAR(50) NOT NULL,
    sub_type VARCHAR(50),
    origin VARCHAR(20) DEFAULT 'iran',
    weight VARCHAR(100),
    price BIGINT NOT NULL,
    stock INT DEFAULT 10,
    sold_count INT DEFAULT 0,
    ingredients TEXT[] DEFAULT '{}',
    purpose TEXT,
    usage TEXT,
    image_url TEXT,
    warnings TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_store_products_dept ON store_products(department);
CREATE INDEX IF NOT EXISTS idx_store_products_cat ON store_products(category);
CREATE INDEX IF NOT EXISTS idx_store_products_sold ON store_products(sold_count DESC);
CREATE INDEX IF NOT EXISTS idx_store_products_price ON store_products(price ASC);

-- ۲. جدول سفارشات مشتریان (Store Orders)
CREATE TABLE IF NOT EXISTS store_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_name VARCHAR(150) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    customer_province VARCHAR(50),
    customer_city VARCHAR(50),
    shipping_address TEXT NOT NULL,
    postal_code VARCHAR(20),
    total_amount BIGINT NOT NULL,
    discount_amount BIGINT DEFAULT 0,
    shipping_method VARCHAR(30) DEFAULT 'express',
    payment_method VARCHAR(30) DEFAULT 'online',
    notes TEXT,
    payment_status VARCHAR(30) DEFAULT 'pending',
    order_status VARCHAR(30) DEFAULT 'registered',
    tracking_code VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- در صورت وجود قبلی جدول، ستون‌های جدید به شکل ایمن اضافه شوند
ALTER TABLE store_orders ADD COLUMN IF NOT EXISTS discount_amount BIGINT DEFAULT 0;
ALTER TABLE store_orders ADD COLUMN IF NOT EXISTS shipping_method VARCHAR(30) DEFAULT 'express';
ALTER TABLE store_orders ADD COLUMN IF NOT EXISTS payment_method VARCHAR(30) DEFAULT 'online';
ALTER TABLE store_orders ADD COLUMN IF NOT EXISTS notes TEXT;

-- ۳. جدول اقلام درون هر سفارش (Store Order Items)
CREATE TABLE IF NOT EXISTS store_order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES store_orders(id) ON DELETE CASCADE NOT NULL,
    product_id VARCHAR(100) REFERENCES store_products(id) ON DELETE RESTRICT NOT NULL,
    quantity INT DEFAULT 1 NOT NULL,
    unit_price BIGINT NOT NULL,
    total_price BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ۴. تابع امن PostgreSQL جهت کاهش موجودی انبار و افزایش آمار فروش هنگام ثبت سفارش
CREATE OR REPLACE FUNCTION process_store_purchase(
    p_product_id VARCHAR,
    p_quantity INT
) RETURNS JSON AS $$
DECLARE
    v_current_stock INT;
    v_sold_count INT;
BEGIN
    SELECT stock, sold_count INTO v_current_stock, v_sold_count
    FROM store_products
    WHERE id = p_product_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RETURN json_build_object('success', false, 'message', 'محصول یافت نشد');
    END IF;

    IF v_current_stock < p_quantity THEN
        RETURN json_build_object('success', false, 'message', 'موجودی انبار برای این کالا کافی نیست');
    END IF;

    UPDATE store_products
    SET 
        stock = stock - p_quantity,
        sold_count = sold_count + p_quantity
    WHERE id = p_product_id;

    RETURN json_build_object(
        'success', true, 
        'remaining_stock', v_current_stock - p_quantity,
        'new_sold_count', v_sold_count + p_quantity
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ۵. فعال‌سازی قوانین امنیتی سطحی (Row Level Security - RLS)
ALTER TABLE store_products ENABLE ROW LEVEL SECURITY;
ALTER TABLE store_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE store_order_items ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public products viewable by everyone" ON store_products;
CREATE POLICY "Public products viewable by everyone" 
ON store_products FOR SELECT USING (is_active = TRUE);

DROP POLICY IF EXISTS "Public can insert orders" ON store_orders;
CREATE POLICY "Public can insert orders" 
ON store_orders FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Public can insert order items" ON store_order_items;
CREATE POLICY "Public can insert order items" 
ON store_order_items FOR INSERT WITH CHECK (true);

-- ۶. درج و همگام‌سازی تمام 57 محصول فروشگاه با موجودی و قیمت‌های واقعی
INSERT INTO store_products (id, name, brand, department, category, sub_type, origin, weight, price, stock, sold_count, ingredients, purpose, usage, image_url, warnings)
VALUES
('carnivor-beef-2000', 'پروتئین بیف ایزوله کارنیور ماسکوپولیس (Carnivor Beef)', 'MuscleMeds (Carnivor)', 'supplements', 'protein', 'beef', 'foreign', '2000 گرم', 6800000, 3, 129, ARRAY['beef_isolate', 'bcaa_branched', 'creatine_mono']::TEXT[], 'پروتئین خالص گوشت گاو هیدرولیزه شده با ۳۵۰٪ تراکم آمینو بیشتر از استیک، ۳۵۰ میلی‌گرم کراتین طبیعی، بدون لاکتوز و چربی صفر.', 'یک اسکوپ بعد از تمرین در آب سرد مصرف شود.', 'images/products/carnivor-beef-2000.svg', 'افراد حساس به ترکیبات گوشت قرمز با احتیاط مصرف کنند.'),
('genestar-egg-albumin-2000', 'پودر سفیده تخم مرغ آلبومین ژن استار (Egg Albumin)', 'ژن استار (Genestar)', 'supplements', 'protein', 'egg', 'iran', '2000 گرم', 2450000, 6, 432, ARRAY['egg_albumin', 'bcaa_branched']::TEXT[], 'پروتئین خالص سفیده تخم‌مرغ با ارزش بیولوژیکی ۱۰۰ (کامل‌ترین پروفایل آمینواسید)، هضم متوسط و مناسب رشد پایدار عضلانی.', 'یک اسکوپ صبح و یک اسکوپ بعد تمرین با آب یا شیر کم‌چرب مخلوط و میل شود.', 'images/products/genestar-egg-albumin-2000.svg', 'برای افراد دارای حساسیت به آلبومین یا تخم‌مرغ منع مصرف دارد.'),
('doobis-egg-albumin-1000', 'پودر پروتئین سفیده تخم مرغ دوبیس ۱۰۰۰ گرمی', 'دوبیس (Doobis)', 'supplements', 'protein', 'egg', 'iran', '1000 گرم', 1350000, 4, 214, ARRAY['egg_albumin', 'bcaa_branched']::TEXT[], 'تامین پروتئین استاندارد از سفیده تخم‌مرغ پاستوریزه بدون کلسترول و چربی زرده.', 'یک پیمانه در آب خنک حل شده و میل شود.', 'images/products/doobis-egg-albumin-1000.svg', 'در افراد با ناراحتی‌های گوارشی خاص با مشورت مصرف شود.'),
('vitap-vegan-protein-1000', 'پروتئین گیاهی فیت وگان ویتاپی (Plant Protein)', 'ویتاپی (VitaP)', 'supplements', 'protein', 'plant', 'iran', '1000 گرم', 980000, 7, 369, ARRAY['plant_pea_soy', 'bcaa_branched']::TEXT[], 'ترکیب پروتئین نخود، سویا و برنج قهوه‌ای، بدون لاکتوز و بدون چربی اشباع، مناسب ورزشکاران گیاه‌خوار و حساس به لبنیات.', 'یک پیمانه ۳۰ گرمی همراه با آب یا شیر بادام.', 'images/products/vitap-vegan-protein-1000.svg', 'به دلیل بافت فیبری، با آب بیشتری مخلوط شود.'),
('bsn-syntha6-2270', 'پروتئین ترکیبی سینتا ۶ بی اس ان (BSN Syntha-6)', 'BSN', 'supplements', 'protein', 'blend', 'foreign', '2270 گرم', 5200000, 6, 288, ARRAY['protein_blend', 'whey_concentrate', 'casein_micellar', 'egg_albumin', 'bcaa_branched']::TEXT[], 'ترکیب ۶ پروتئین زودجذب و دیرجذب (وی کنسانتره، وی ایزوله، کازئین، آلبومین و پپتید) برای تغذیه ۲۴ ساعته عضلات.', 'یک پیمانه در آب یا شیر حل شود.', 'images/products/bsn-syntha6-2270.svg', 'در رژیم‌های صفر کربوهیدرات مسابقاتی با احتساب کالری مصرف شود.'),
('kalleh-isolate-650', 'پودر پروتئین وی ایزوله کاله پرو ۹۰٪', 'کاله پرو (Kalleh Pro)', 'supplements', 'protein', 'isolate', 'iran', '650 گرم', 1450000, 8, 198, ARRAY['whey_isolate', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'وی ایزوله بسیار خالص با چربی و لاکتوز نزدیک به صفر، ایده‌آل برای دوره کات و مسابقات.', 'یک اسکوپ بعد تمرین و یک اسکوپ صبح در آب خنک حل شود.', 'images/products/kalleh-isolate-650.svg', 'در دمای خشک و خنک نگهداری شود.'),
('kalleh-whey-650', 'پودر پروتئین وی ۱۰۰٪ کاله پرو (Kalleh Pro)', 'کاله پرو (Kalleh Pro)', 'supplements', 'protein', 'concentrate', 'iran', '650 گرم', 1150000, 4, 270, ARRAY['whey_concentrate', 'bcaa_branched']::TEXT[], 'تامین پروتئین خالص با جذب بالا، عضله‌سازی و تسریع ریکاوری بدون قند و چربی مضر.', 'یک اسکوپ (۳۲ گرم) را با ۲۵۰ میلی‌لیتر آب یا شیر کم‌چرب بعد تمرین مصرف نمایید.', 'images/products/kalleh-whey-650.svg', 'افراد دارای حساسیت شدید به پروتئین‌های شیر با احتیاط مصرف کنند.'),
('dymatize-iso-100-2270', 'ایزو ۱۰۰ هیدرولیزه دایماتیز (Dymatize ISO 100)', 'Dymatize', 'supplements', 'protein', 'hydrolyzed', 'foreign', '2270 گرم', 8200000, 6, 260, ARRAY['whey_isolate', 'whey_hydrolyzed', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'لوکس‌ترین پروتئین وی هیدرولیزه جهان با هضم فوری و خلوص بیش از ۹۰ درصد.', 'یک پیمانه در ۲۰۰ میلی‌لیتر آب خنک بلافاصله حل می‌شود.', 'images/products/dymatize-iso-100-2270.svg', 'برای دوران کات و ورزشکاران حرفه‌ای مناسب‌ترین گزینه است.'),
('on-gold-whey-2270', 'پروتئین وی ۱۰۰٪ گلد استاندارد اپتیموم (ON Gold Whey)', 'Optimum Nutrition (ON)', 'supplements', 'protein', 'isolate', 'foreign', '2270 گرم', 6400000, 3, 381, ARRAY['whey_isolate', 'whey_concentrate', 'whey_hydrolyzed', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'پرفروش‌ترین و معتبرترین پروتئین وی جهان، غنی از پپتیدهای هیدرولیزه و ایزوله.', 'یک پیمانه ۳۰ گرمی در ۲۰۰ الی ۲۵۰ میلی‌لیتر آب سرد حل شده و مصرف شود.', 'images/products/on-gold-whey-2270.svg', 'به دلیل وجود نمونه‌های فیک در بازار، حتماً از منابع معتبر تهیه شود.'),
('on-casein-1800', 'کازئین ۱۰۰٪ گلد استاندارد اپتیموم (ON Casein)', 'Optimum Nutrition (ON)', 'supplements', 'protein', 'casein', 'foreign', '1800 گرم', 5800000, 4, 474, ARRAY['casein_micellar', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'پروتئین دیرجذب شبانه برای تغذیه پیوسته عضلات طی ۷ تا ۸ ساعت خواب شبانه.', 'یک اسکوپ در آب یا شیر قبل از خواب میل شود.', 'images/products/on-casein-1800.svg', 'قوام غلیظ‌تری نسبت به وی دارد.'),
('pnc-pure-whey-2270', 'پیور وی کارن (PNC Pure Whey)', 'کارن (PNC)', 'supplements', 'protein', 'concentrate', 'iran', '2270 گرم', 3200000, 5, 123, ARRAY['whey_concentrate', 'whey_isolate', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'پروتئین کنسانتره داروسازی کارن به همراه گلوتامین و ویتامین‌ها برای عضله‌سازی خشک.', 'روزانه ۱ تا ۲ پیمانه (هر پیمانه حدود ۳۰ گرم) همراه با آب مصرف شود.', 'images/products/pnc-pure-whey-2270.svg', 'حاوی فنیل‌آلانین (برای بیماران فنیل‌کتونوری منع مصرف دارد).'),
('pnc-super-mass-5000', 'سوپر مس گینر کارن (PNC Super Mass)', 'کارن (PNC)', 'supplements', 'gainer', 'mass', 'iran', '5000 گرم', 2850000, 1, 223, ARRAY['high_calorie_gainer', 'complex_carbs', 'whey_concentrate', 'bcaa_branched']::TEXT[], 'افزایش وزن و حجم سریع برای افراد اکتومورف، تامین کربوهیدرات کمپلکس و پروتئین باکیفیت.', 'روزانه تا ۴ پیمانه در چند نوبت بین وعده‌ها و بعد از تمرین مصرف شود.', 'images/products/pnc-super-mass-5000.svg', 'افراد دارای اضافه وزن یا دیابت نباید از گینر پرکالری استفاده کنند.'),
('on-serious-mass-5400', 'سریوس مس گینر اپتیموم نوتریشن (ON Serious Mass)', 'Optimum Nutrition (ON)', 'supplements', 'gainer', 'mass', 'foreign', '5400 گرم', 4950000, 0, 346, ARRAY['high_calorie_gainer', 'complex_carbs', 'whey_concentrate', 'daily_multivitamin', 'creatine_mono']::TEXT[], 'معروف‌ترین مس گینر جهان با ۱۲۵۰ کالری و ۵۰ گرم پروتئین در هر وعده برای جهش در وزن و سایز عضلات.', 'روزانه در ۲ یا ۳ نوبت نصف پیمانه‌ای همراه با شیر پرچرب یا آب مصرف شود.', 'images/products/on-serious-mass-5400.svg', 'به دلیل کالری بالا فقط برای افراد لاغر مناسب است.'),
('pnc-carbo-2000', 'پودر کربوهیدرات خالص کارن ۲۰۰۰ گرمی', 'کارن (PNC)', 'supplements', 'gainer', 'carbo', 'iran', '2000 گرم', 890000, 5, 459, ARRAY['complex_carbs']::TEXT[], 'تامین ۱۰۰٪ مالتودکسترین خالص بدون چربی و پروتئین برای پر کردن فوری گلیکوژن کبد و عضلات.', 'قبل یا بعد از تمرین ۲ پیمانه در آب حل شود.', 'images/products/pnc-carbo-2000.svg', 'افراد دیابتی نباید مصرف کنند.'),
('applied-waxy-maize-2000', 'کربوهیدرات ذرت مومی ووکسی مایز اپلاید نوتریشن ۲۰۰۰ گرمی', 'Applied Nutrition', 'supplements', 'gainer', 'carbo', 'foreign', '2000 گرم', 2850000, 3, 168, ARRAY['waxy_maize', 'complex_carbs']::TEXT[], 'کربوهیدرات با وزن مولکولی بالا و اسمولاریته پایین برای تخلیه فوق‌سریع از معده بدون نفخ.', 'یک اسکوپ حین تمرین یا بلافاصله پس از تمرین مصرف شود.', 'images/products/applied-waxy-maize-2000.svg', 'در جای خشک و خنک نگهداری شود.'),
('vitargo-pure-carbs-1000', 'کربوهیدرات تخصصی ویتارگو خالص ۱۰۰۰ گرمی (Vitargo Pure)', 'Universal Nutrition', 'supplements', 'gainer', 'carbo', 'foreign', '1000 گرم', 3600000, 0, 246, ARRAY['vitargo_carb', 'complex_carbs']::TEXT[], 'ثبت اختراع جهانی سریع‌ترین کربوهیدرات ورزشی جهان برای پرسازی فوری عضلات بدون افت قند خون.', 'یک پیمانه بلافاصله بعد از تمرین با ۵۰۰ میلی‌لیتر آب مخلوط شود.', 'images/products/vitargo-pure-carbs-1000.svg', 'افراد دارای قند خون با پزشک مشورت نمایند.'),
('levrone-gold-lean-mass-3000', 'گلد لین مس کوین لورون (Kevin Levrone Gold Lean Mass)', 'Kevin Levrone', 'supplements', 'gainer', 'lean', 'foreign', '3000 گرم', 4200000, 5, 227, ARRAY['high_calorie_gainer', 'whey_isolate', 'whey_concentrate', 'tribulus_terrestris', 'creatine_mono', 'bcaa_branched']::TEXT[], 'گینر حجم خشک لوکس حاوی DAA، عصاره شنبلیله، ال آرژنین و HMB برای افزایش سایز عضلانی تمیز.', '۲ پیمانه در طول روز همراه آب.', 'images/products/levrone-gold-lean-mass-3000.svg', 'برای افراد زیر ۱۸ سال توصیه نمی‌شود.'),
('doobis-creatine-beta-300', 'کراتین بتا آلانین دوبیس ۳۰۰ گرمی', 'دوبیس (Doobis)', 'supplements', 'creatine', 'beta_creatine', 'iran', '300 گرم', 780000, 2, 372, ARRAY['creatine_mono', 'beta_alanine_carnosyn']::TEXT[], 'ترکیب همزمان کراتین مونوهیدرات و بتاآلانین جهت افزایش توان انفجاری و تاخیر خستگی ناشی از اسید لاکتیک.', 'یک پیمانه قبل یا بعد از تمرین در آب حل شود.', 'images/products/doobis-creatine-beta-300.svg', 'خارش ملایم بتاآلانین طبیعی است.'),
('pnc-creatine-300', 'کراتین مونوهیدرات میکرونایزد کارن', 'کارن (PNC)', 'supplements', 'creatine', 'monohydrate', 'iran', '300 گرم', 580000, 2, 356, ARRAY['creatine_mono']::TEXT[], 'افزایش توان بی‌هوازی، افزایش قدرت در تکرارهای سنگین و هیدراتاسیون داخل سلولی عضلات.', 'روزانه ۵ گرم همراه با یک لیوان آب یا آب‌میوه بعد از تمرین.', 'images/products/pnc-creatine-300.svg', 'نوشیدن روزانه حداقل ۳ لیتر آب در طول دوره الزامی است.'),
('muscletech-celltech-2700', 'سل تک کراتین پیشرفته ماسل تک (Cell-Tech)', 'MuscleTech', 'supplements', 'creatine', 'complex', 'foreign', '2700 گرم', 4500000, 5, 391, ARRAY['creatine_complex', 'creatine_mono', 'complex_carbs', 'bcaa_branched']::TEXT[], 'فرمول افسانه‌ای کراتین ترانسپورت با کربوهیدرات‌های اختصاصی برای انفجار حجم و قدرت عضلات.', 'یک اسکوپ بلافاصله بعد تمرین با آب سرد.', 'images/products/muscletech-celltech-2700.svg', 'طعم میوه‌ای و قند دارد.'),
('myprotein-creapure-500', 'کراتین خالص کریپیور مای‌پروتئین (Creapure)', 'MyProtein', 'supplements', 'creatine', 'creapure', 'foreign', '500 گرم', 2300000, 6, 288, ARRAY['creatine_creapure', 'creatine_mono']::TEXT[], 'خالص‌ترین شکل کراتین دنیا (Creapure ساخت آلمان) با خلوص ۹۹.۹۹ درصد، بدون ناخالصی و فلزات سنگین.', 'روزانه ۵ گرم همراه آب یا شیک بعد تمرین.', 'images/products/myprotein-creapure-500.svg', 'آب فراوان در طول روز مصرف کنید.'),
('pnc-arginine-1000', 'قرص ال آرژنین ۱۰۰۰ میلی‌گرم کارن', 'کارن (PNC)', 'supplements', 'amino', 'arginine', 'iran', '100 عدد', 520000, 2, 404, ARRAY['arginine_hcl']::TEXT[], 'پیش‌ساز نیتریک اکسید (NO)، گشادکننده عروق خونی، افزایش پمپاژ خون و تحریک ترشح هورمون رشد.', '۱ تا ۲ قرص قبل تمرین یا قبل خواب.', 'images/products/pnc-arginine-1000.svg', 'افراد دارای سابقه تبخال با احتیاط مصرف کنند.'),
('doobis-amino-whey-300', 'قرص آمینو وی دوبیس ۳۰۰ عددی', 'دوبیس (Doobis)', 'supplements', 'amino', 'amino_whey', 'iran', '300 عدد', 980000, 4, 474, ARRAY['amino_peptides', 'whey_concentrate', 'bcaa_branched']::TEXT[], 'تامین تمام اسیدهای آمینه شاخه‌دار و ضروری از پروتئین وی فشرده در قالب قرص‌های راحت‌هضم.', '۳ عدد قبل تمرین و ۳ عدد بعد تمرین.', 'images/products/doobis-amino-whey-300.svg', 'با آب فراوان میل شود.'),
('pnc-bcaa-300', 'پودر بی سی ای ای کارن (PNC BCAA)', 'کارن (PNC)', 'supplements', 'amino', 'bcaa', 'iran', '300 گرم', 890000, 6, 284, ARRAY['bcaa_branched']::TEXT[], 'پیشگیری از کاتابولیسم و ریزش عضلات در حین تمرین پرفشار و دوره‌های رژیم کات.', '۵ تا ۱۰ گرم در طول جلسه تمرین در بطری آب ورزشی حل شده و نوشیده شود.', 'images/products/pnc-bcaa-300.svg', 'بیش از حد مصرف نشود.'),
('genestar-pure-glutamine-300', 'گلوتامین ۱۰۰٪ خالص ژن استار ۳۰۰ گرمی', 'ژن استار (Genestar)', 'supplements', 'amino', 'glutamine', 'iran', '300 گرم', 820000, 6, 364, ARRAY['glutamine_pure']::TEXT[], 'بازسازی بافت‌های تخلیه شده، حفظ سلامت دستگاه گوارش و روده و پیشگیری از سرماخوردگی و ضعف بدنسازان.', '۵ گرم بعد تمرین و ۵ گرم قبل خواب.', 'images/products/genestar-pure-glutamine-300.svg', 'افراد دارای مشکلات شدید کلیوی مشورت کنند.'),
('pnc-hmb-120', 'کپسول اچ ام بی کارن (PNC HMB)', 'کارن (PNC)', 'supplements', 'amino', 'hmb', 'iran', '120 عدد', 950000, 6, 204, ARRAY['hmb_pure']::TEXT[], 'سپر ضد ریزش عضلات، متابولیت فعال لوسین جهت حفظ بافت عضلانی در رژیم‌های سخت کات.', 'روزانه ۳ کپسول در وعده‌های مختلف همراه آب.', 'images/products/pnc-hmb-120.svg', 'برای دیدن اثرات حداقل ۲ تا ۳ هفته مصرف شود.'),
('pnc-beta-alanine-300', 'پودر بتا آلانین کارن ۳۰۰ گرمی', 'کارن (PNC)', 'supplements', 'energy', 'beta_alanine', 'iran', '300 گرم', 790000, 8, 318, ARRAY['beta_alanine_carnosyn']::TEXT[], 'افزایش سطح کارنوزین عضلات، تاخیر در اسیدی شدن عضله و امکان اجرای تکرارهای بیشتر در ست‌های سنگین.', '۳ تا ۵ گرم ۲۰ دقیقه قبل تمرین در آب حل شود.', 'images/products/pnc-beta-alanine-300.svg', 'ایجاد سوزن‌سوزن شدن موقت در پوست بی‌خطر است.'),
('genestar-citrulline-300', 'سیترولین مالات خالص ژن استار ۳۰۰ گرمی', 'ژن استار (Genestar)', 'supplements', 'energy', 'citrulline', 'iran', '300 گرم', 740000, 2, 372, ARRAY['citrulline_malate']::TEXT[], 'افزایش چشمگیر جریان خون، رگ‌زایی عضلانی (Vascularity) و دفع آمونیاک از بافت‌های عضلانی.', '۳ تا ۵ گرم پودر حدود ۳۰ دقیقه قبل تمرین در آب.', 'images/products/genestar-citrulline-300.svg', 'طعم ترش طبیعی دارد.'),
('pnc-glucosamine-chondroitin', 'کپسول گلوکزامین و کندروئیتین پلاس ام‌اس‌ام کارن (PNC)', 'کارن (PNC)', 'supplements', 'health', 'joint', 'iran', '۶۰ عدد', 680000, 5, 184, ARRAY['joint_glucosamine', 'joint_msm']::TEXT[], 'بازسازی و ترمیم غضروف‌های ساییده‌شده، کاهش درد مفاصل و افزایش روانکاری تاندون‌ها در تمرین سنگین.', 'روزانه ۲ کپسول همراه با وعده غذایی و یک لیوان آب میل شود.', 'images/products/pnc-glucosamine-chondroitin.svg', 'افراد دارای حساسیت به سخت‌پوستان دریایی با احتیاط مصرف کنند.'),
('pnc-collagen-pure-300', 'پودر کلاژن پپتید هیدرولیزه کارن ۳۰۰ گرمی', 'کارن (PNC)', 'supplements', 'health', 'joint', 'iran', '۳۰۰ گرم', 1150000, 8, 230, ARRAY['joint_collagen']::TEXT[], 'تقویت تاندون‌ها و رباط‌های عضلانی، بهبود خاصیت ارتجاعی مفاصل و پیشگیری از آسیب‌دیدگی‌های سنگین.', 'روزانه یک پیمانه در آب یا آبمیوه مخلوط و ناشتا یا بعد تمرین میل شود.', 'images/products/pnc-collagen-pure-300.svg', 'در جای خشک و دور از نور نگهداری شود.'),
('pnc-omega3-1000', 'کپسول نرم امگا ۳ کارن ۱۰۰۰ میلی‌گرم (بدون جیوه)', 'کارن (PNC)', 'supplements', 'health', 'joint', 'iran', '۵۰ عدد', 490000, 6, 315, ARRAY['omega3_pure']::TEXT[], 'کاهش التهابات مفاصل و عضلات پس از تمرین، پشتیبانی از سلامت قلب، عروق و تمرکز مغزی.', 'روزانه ۱ تا ۲ عدد همراه با ناهار یا شام مصرف شود.', 'images/products/pnc-omega3-1000.svg', 'افراد مصرف‌کننده داروهای ضدانعقاد با پزشک مشورت کنند.'),
('pnc-caffeine-200', 'قرص کافئین ۲۰۰ میلی‌گرم کارن', 'کارن (PNC)', 'supplements', 'energy', 'caffeine', 'iran', '60 عدد', 240000, 7, 329, ARRAY['caffeine_anhydrous']::TEXT[], 'افزایش فوری هوشیاری، مهار حس خستگی، افزایش انقباضات عضلانی و بالا بردن نرخ کالری‌سوزی.', 'یک قرص ۴۵ دقیقه قبل تمرین همراه آب.', 'images/products/pnc-caffeine-200.svg', 'در ساعات پایانی شب مصرف نشود.'),
('cellucor-c4-180', 'پمپ سی ۴ اورجینال سلوکور (Cellucor C4)', 'Cellucor', 'supplements', 'energy', 'stim', 'foreign', '180 گرم', 2350000, 4, 206, ARRAY['preworkout_matrix', 'beta_alanine_carnosyn', 'citrulline_malate', 'caffeine_anhydrous']::TEXT[], 'محبوب‌ترین پیش‌تمرین جهان، ایجاد تمرکز لیزری، انرژی بالا بدون افت ناگهانی و رگ‌زایی عضلات.', 'یک پیمانه ۲۰ تا ۳۰ دقیقه قبل تمرین در ۲۰۰ میلی‌لیتر آب.', 'images/products/cellucor-c4-180.svg', 'قبل خواب مصرف نشود.'),
('pnc-l-carnitine-100', 'قرص ال کارنیتین ۱۰۰۰ میلی‌گرم کارن', 'کارن (PNC)', 'supplements', 'fatburn', 'carnitine', 'iran', '100 عدد', 480000, 3, 241, ARRAY['l_carnitine_tartrate']::TEXT[], 'انتقال اسیدهای چرب به میتوکندری سلول برای سوزاندن چربی و افزایش توان هوازی.', '۱ تا ۲ عدد قبل از فعالیت ورزشی یا تمرینات کاردیو.', 'images/products/pnc-l-carnitine-100.svg', 'افراد با سابقه تشنج یا کم‌کاری تیروئید مشورت پزشکی بگیرند.'),
('genestar-cla-1000', 'کپسول سی ال ای ۱۰۰۰ میلی‌گرم ژن استار (CLA)', 'ژن استار (Genestar)', 'supplements', 'fatburn', 'cla', 'iran', '90 عدد', 760000, 5, 399, ARRAY['cla_pure']::TEXT[], 'اسید لینولئیک کونژوگه جهت کاهش ذخایر چربی شکمی و پهلوها و مهار آنزیم لیپوپروتئین لیپاز.', '۱ کپسول همراه با هر وعده غذایی اصلی (۳ بار در روز).', 'images/products/genestar-cla-1000.svg', 'در دوران بارداری و شیردهی منع مصرف دارد.'),
('muscletech-hydroxycut-110', 'هیدروکسی‌کات الیت ماسل تک (Hydroxycut Elite)', 'MuscleTech', 'supplements', 'fatburn', 'thermo', 'foreign', '110 عدد', 2400000, 5, 243, ARRAY['thermo_extracts', 'caffeine_anhydrous', 'l_carnitine_tartrate']::TEXT[], 'چربی‌سوز ترموژنیک هاردکور، افزایش دمای درونی بدن، سرکوب اشتهای کاذب و افزایش کالری‌سوزی پایه.', '۱ عدد در روز قبل از وعده صبحانه یا تمرین.', 'images/products/muscletech-hydroxycut-110.svg', 'بسیار قوی است؛ افراد حساس به کافئین نباید مصرف کنند.'),
('pnc-zma-60', 'کپسول زد ام ای کارن (PNC ZMA)', 'کارن (PNC)', 'supplements', 'health', 'zma', 'iran', '60 عدد', 490000, 2, 176, ARRAY['zma_complex']::TEXT[], 'ترکیب ثبت‌شده روی (زینک)، منیزیم و ویتامین B6 جهت بهبود کیفیت خواب عمیق، تقویت ترشح تستوسترون شبانه و کاهش گرفتگی عضلات.', '۲ کپسول ۳۰ تا ۶۰ دقیقه قبل از خواب با معده نسبتاً خالی.', 'images/products/pnc-zma-60.svg', 'همزمان با لبنیات یا کلسیم مصرف نشود (کلسیم مانع جذب زینک است).'),
('genestar-tribulus-650', 'کپسول تریبولوس ۶۵۰ ژن استار (Tribulus)', 'ژن استار (Genestar)', 'supplements', 'health', 'tribulus', 'iran', '60 عدد', 580000, 1, 187, ARRAY['tribulus_terrestris']::TEXT[], 'عصاره استاندارد گیاه خارخاسک با ساپونین بالا جهت پشتیبانی طبیعی از تولید تستوسترون، نشاط و توان عضلانی.', 'روزانه ۱ تا ۲ کپسول همراه با غذا.', 'images/products/genestar-tribulus-650.svg', 'برای افراد زیر ۱۸ سال توصیه نمی‌شود.'),
('ala-300-pure', 'کپسول آلفا لیپوئیک اسید ۳۰۰ (ALA 300mg)', 'کارن (PNC)', 'supplements', 'health', 'ala', 'iran', '60 عدد', 460000, 8, 318, ARRAY['ala_antioxidant']::TEXT[], 'آنتی‌اکسیدان قوی محلول در آب و چربی، بهبود حساسیت به انسولین و راندن مواد غذایی و کراتین به درون سلول‌های عضلانی.', 'یک کپسول همراه با وعده کربوهیدراتی یا بعد تمرین.', 'images/products/ala-300-pure.svg', 'در صورت افت قند خون با کمی آبمیوه میل شود.'),
('vitap-daily-multi-60', 'مولتی ویتامین و مینرال دیلی ویتاپی', 'ویتاپی (VitaP)', 'supplements', 'health', 'multi', 'iran', '60 عدد', 290000, 8, 446, ARRAY['daily_multivitamin']::TEXT[], 'تامین تمام ریزمغذی‌ها، زینک، منیزیم، ویتامین C و گروه B برای رفع خستگی ورزشکار.', 'روزانه یک عدد قرص همراه با وعده غذایی.', 'images/products/vitap-daily-multi-60.svg', 'با معده خالی خورده نشود.'),
('men-tee-nike-pro', 'تیشرت فیتنس درای‌فیت نایک پرو (Nike Pro Combat Fit)', 'Nike', 'apparel_men', 'tshirt', 'compression', 'foreign', 'وزن خالص: ۱۸۰ گرم', 1280000, 6, 108, ARRAY['dryfit', 'breathable', 'anti_odor', '4way_stretch']::TEXT[], 'پارچه اختصاصی Dri-FIT نایک با تهویه فوق‌العاده در زیر بغل و پشت، مدیریت رطوبت عرق و تناسب فشرده با خطوط عضلات سینه و سرشانه.', 'مناسب تمرینات پرفشار بدنسازی، هوازی و دویدن در سالن.', 'images/products/men-tee-nike-pro.svg', 'شستشو با آب سرد و بدون خشک‌کن حرارتی انجام شود.'),
('men-tank-venum', 'رکابی فیتنس کات عضلانی ونوم (Venum Giant Tank Top)', 'Venum', 'apparel_men', 'tanktop', 'stringer', 'foreign', 'وزن خالص: ۱۴۰ گرم', 950000, 4, 350, ARRAY['pure_cotton', 'deep_cut', 'breathable', 'reinforced_seams']::TEXT[], 'طراحی استرینگر با برش عمیق زیربغل و پشت قهرمانی Y-Back برای آزادی ۱۰۰٪ دامنه حرکتی در حرکات زیربغل و سرشانه.', 'بهترین گزینه برای روز تمرین سینه، سرشانه و زیربغل.', 'images/products/men-tank-venum', 'پشت‌ورو شسته شود تا چاپ لوگوی ونوم آسیب نبیند.'),
('men-shorts-ua', 'شلوارک کشسانی ۴ جهته آندرآرمور (Under Armour 7" Shorts)', 'Under Armour', 'apparel_men', 'shorts', '4way', 'foreign', 'وزن خالص: ۲۱۰ گرم', 1450000, 4, 254, ARRAY['4way_stretch', 'zip_pocket', 'breathable', 'quick_dry']::TEXT[], 'دارای جیب مخفی زیپ‌دار ضدآب برای گوشی همراه، بند کشی قابل تنظیم و منافذ لیزری تهویه در دو طرف ران.', 'تمرینات اسکوات، کراسفیت و دویدن استقامتی.', 'images/products/men-shorts-ua.svg', 'اتوکشی مستقیم روی بند و منافذ لیزری ممنوع است.'),
('men-pants-monsta', 'شلوار اسلش تمرینی بدنسازی مونسلو (Monsta Gym Joggers)', 'Monsta', 'apparel_men', 'pants', 'heavy_cotton', 'foreign', 'وزن خالص: ۴۲۰ گرم', 1850000, 3, 193, ARRAY['pure_cotton', 'heavy_duty', 'deep_pockets', 'ankle_cuff']::TEXT[], 'دمپای کش‌باف مقاوم، فاق ارگونومیک آزاد بدون کشش مزاحم در حرکات پا و گرم نگه داشتن مفاصل زانو حین ست‌های سنگین.', 'تمرین در فصول سرد و گرم کردن اولیه عضلات.', 'images/products/men-pants-monsta.svg', 'با لباس‌های تیره شسته شود.'),
('men-tee-gymshark', 'تیشرت سیملس بدون درز جیم‌شارک (Gymshark Onyx Seamless)', 'Gymshark', 'apparel_men', 'tshirt', 'seamless', 'foreign', 'وزن خالص: ۱۹۰ گرم', 1650000, 7, 173, ARRAY['seamless', 'jacquard_mesh', 'anti_odor', 'slim_fit']::TEXT[], 'بافت ژاکارد بدون هیچ‌گونه درز جانبی برای جلوگیری کامل از سایش پوست، با خطوط سایه‌روشن برجسته‌کننده عضلات شکم و بازو.', 'تمرینات حرفه‌ای فیگورگیری و بدنسازی سنگین.', 'images/products/men-tee-gymshark.svg', 'از تماس با چسب‌های زبر مچ‌بند و کمربند محافظت شود.'),
('men-tank-golds', 'رکابی کلاه‌دار تمرین بدنسازی گلدز جیم (Gold''s Gym Hoodie)', 'Gold''s Gym', 'apparel_men', 'tanktop', 'hoodie', 'foreign', 'وزن خالص: ۲۴۰ گرم', 1100000, 2, 332, ARRAY['pure_cotton', 'hooded', 'oversized', 'hardcore_style']::TEXT[], 'دارای کلاه تمرینی شیک برای تمرکز حداکثری حین گوش دادن به موسیقی در باشگاه با لوگوی کلاسیک وزنه بردار گلدز جیم.', 'شروع ست‌های سنگین پرس سینه و ددلیفت.', 'images/products/men-tank-golds.svg', 'شستشو با آب حداکثر ۳۰ درجه سانتی‌گراد.'),
('women-leg-lulu', 'لگینگ ورزشی فاق‌بلند بدون درز لولولمون (Lululemon Align)', 'Lululemon', 'apparel_women', 'leg', 'high_waist', 'foreign', 'وزن خالص: ۲۰۰ گرم', 2450000, 3, 357, ARRAY['high_waist', 'buttery_soft', 'squat_proof', 'hidden_pocket']::TEXT[], '۱۰۰٪ اسکات‌پروف (بدون هیچ دید به داخل حتی در عمیق‌ترین کشش‌ها)، فاق بسیار بلند با جمع‌کنندگی ملایم شکم و پهلو.', 'یوگا، پیلاتس، فیتنس و تمرینات سنگین پا.', 'images/products/women-leg-lulu.svg', 'با نرم‌کننده لباس شسته نشود.'),
('women-bra-nike', 'نیم‌تنه ورزشی کاپ‌دار نایک پرو ساپورت (Nike Pro Sports Bra)', 'Nike', 'apparel_women', 'nim_tane', 'padded_bra', 'foreign', 'وزن خالص: ۱۳۰ گرم', 1150000, 5, 327, ARRAY['medium_support', 'removable_pads', 'dri_fit', 'racerback']::TEXT[], 'دارای پدهای اسفنجی ضدتغییرشکل با ساپورت متوسط رو به بالا برای جلوگیری از لرزش حین تمرینات طناب‌زنی و پرش.', 'تمرینات فیتنس، تی‌آرایکس و ایروبیک.', 'images/products/women-bra-nike.svg', 'پدها پیش از شستشو خارج و جداگانه شسته شوند.'),
('women-skirt-gymshark', 'دامن ورزشی دو تکه شلوارک‌دار جیم‌شارک (Gymshark Skirt)', 'Gymshark', 'apparel_women', 'daman', '2in1_skirt', 'foreign', 'وزن خالص: ۱۹۰ گرم', 1350000, 4, 262, ARRAY['built_in_shorts', 'lightweight', 'pleated', 'ball_pocket']::TEXT[], 'طراحی مدرن با لایه شلوارک جذب ضدسایش در زیر دامن و جیب معکوس برای حمل وسایل کوچک بدون بیرون‌زدگی.', 'تنیس، بدمینتون، کراسفیت و دویدن در فضای باز.', 'images/products/women-skirt-gymshark.svg', 'بدون سفیدکننده شسته شود.'),
('women-top-ua', 'بالاتنه آستین‌بلند انگشتی آندرآرمور (Under Armour ColdGear)', 'Under Armour', 'apparel_women', 'balatane', 'long_sleeve', 'foreign', 'وزن خالص: ۲۱۰ گرم', 1650000, 2, 148, ARRAY['thumbholes', 'thermal_control', 'anti_microbial', 'slim_fit']::TEXT[], 'سرآستین مجهز به سوراخ شست (Thumbholes) برای جلوگیری از بالا رفتن آستین و حفظ کامل دمای دست در طول تمرین.', 'تمرین در فضای باز صبحگاهی و سالن‌های ورزشی خنک.', 'images/products/women-top-ua.svg', 'در دمای ۳۰ درجه شسته شود.'),
('women-crop-puma', 'کراپ‌تاپ ورزشی بند متقاطع پوما (Puma Training Crop)', 'Puma', 'apparel_women', 'nim_tane', 'crop_top', 'foreign', 'وزن خالص: ۱۱۰ گرم', 980000, 8, 466, ARRAY['strappy_back', 'elastic_band', 'drycell', 'crop_cut']::TEXT[], 'طراحی بندهای ظریف ضربدری در پشت جهت انتقال حداکثر جریان هوا و جلوگیری از تعریق پشت گردن.', 'تمرینات پیلاتس، بادی‌پامپ و تمرین با وزنه.', 'images/products/women-crop-puma.svg', 'خشک‌شویی نشود.'),
('gear-wrist-harbinger', 'مچ‌بند چسبی سنگین ۱۸ اینچ هاربینگر (Harbinger Pro Wraps)', 'Harbinger', 'gym_gear', 'mochband', 'wraps', 'foreign', 'وزن جفت: ۲۲۰ گرم', 850000, 5, 215, ARRAY['heavy_elastic', 'thumb_loop', 'wide_velcro', 'pro_support']::TEXT[], 'تثبیت ۱۰۰٪ استخوان مچ دست در حرکات سنگین پرس سینه، سرشانه هالتر و اورهد بدون قطع جریان خون.', 'پاورلیفتینگ، بدنسازی قدرتی و ست‌های حداکثری.', 'images/products/gear-wrist-harbinger.svg', 'در پایان ست برای برگشت جریان خون باز شود.'),
('gear-belt-rdx', 'کمربند چرم گاوی ۲ لایه پاورلیفتینگ RDX (Leather Belt 4")', 'RDX', 'gym_gear', 'belt', 'leather_belt', 'foreign', 'وزن خالص: ۱۱۵۰ گرم', 3200000, 7, 217, ARRAY['genuine_leather', 'double_prong', 'lumbar_pad', 'heavy_stitching']::TEXT[], 'ایجاد حداکثر فشار درون‌شکمی (Intra-abdominal Pressure) برای محافظت از دیسک‌های ستون فقرات در اسکات و ددلیفت سنگین.', 'تمرینات پاورلیفتینگ، رکوردگیری ددلیفت و اسکات بالای ۱۰۰ کیلوگرم.', 'images/products/gear-belt-rdx.svg', 'دور از رطوبت مستقیم و تابش آفتاب نگهداری شود.'),
('gear-shaker-spider', 'شیکر استیل دوجداره دکمه‌ای اسپایدر ۹۰۰ میل (Spider Steel)', 'Spider', 'gym_gear', 'qomqome', 'steel_shaker', 'foreign', 'ظرفیت: ۹۰۰ میلی‌لیتر', 750000, 7, 365, ARRAY['double_wall_steel', 'odorless', 'leak_proof', 'spring_ball']::TEXT[], 'حفظ دمای آب سرد تا ۲۴ ساعت، حل کامل غلیظ‌ترین پودرهای وی و گینر بدون گلوله‌شدن با فنر استیل ژاپنی بدون بو گرفتن پس از شستشو.', 'میکسر مکمل‌های پروتئینی، BCAA و نگهداری نوشیدنی یخ در طول تمرین.', 'images/products/gear-shaker-spider.svg', 'در مایکروویو یا ماشین ظرفشویی قرار داده نشود.'),
('gear-jug-hydra', 'گالن انگیزشی آب ۲.۲ لیتری هیدراپک (HydraPak 2.2L Jug)', 'HydraPak', 'gym_gear', 'qomqome', 'water_jug', 'foreign', 'ظرفیت: ۲۲۰۰ میلی‌لیتر', 620000, 8, 322, ARRAY['bpa_free', 'time_marker', 'sturdy_handle', 'wide_mouth']::TEXT[], 'خط‌کشی انگیزشی ساعت‌به‌ساعت برای تامین هیدراتاسیون ۲.۲ لیتری روزانه ورزشکاران، دسته ارگونومیک محکم و درب ضدنشت متصل به بند.', 'مصرف روزانه آب در باشگاه و دوره‌های مصرف کراتین.', 'images/products/gear-jug-hydra.svg', 'از ریختن آب جوش بالای ۶۰ درجه خودداری شود.'),
('gear-spray-sanisport', 'اسپری تنظیف و ضدعفونی تجهیزات ورزشی (Sanisport Gym Spray)', 'SaniSport', 'gym_gear', 'spray', 'clean_spray', 'foreign', 'حجم: ۴۰۰ میلی‌لیتر', 280000, 4, 254, ARRAY['kills_99_bacteria', 'deodorizer', 'equipment_safe', 'eucalyptus']::TEXT[], 'ضدعفونی فوری تشک تمرین، دستکش، روکش چرم نیمکت‌های باشگاه و پاکسازی بوی نامطبوع عرق بدون پوساندن رویه تجهیزات.', 'قبل و بعد از استفاده از تجهیزات مشترک باشگاه و کفش ورزشی.', 'images/products/gear-spray-sanisport.svg', 'از تماس با چشم یا استنشاق مستقیم پرهیز شود.'),
('gear-straps-schiek', 'بند لیفت پنبه‌ای پددار حرفه‌ای شیبا (Schiek Lifting Straps)', 'Schiek', 'gym_gear', 'mochband', 'straps', 'foreign', 'وزن جفت: ۱۲۰ گرم', 480000, 6, 380, ARRAY['neoprene_pad', 'heavy_duty_cotton', 'extra_long', 'anti_slip']::TEXT[], 'حذف خستگی ساعد و پنجه در ددلیفت، بارفیکس و شراگ تا وزن بالای ۲۰۰ کیلوگرم بدون لیز خوردن از دور میله هالتر.', 'حرکات کششی سنگین ددلیفت، زیربغل هالتر خم و بارفیکس.', 'images/products/gear-straps-schiek.svg', 'قابل شستشو با دست و صابون مایع.')
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    brand = EXCLUDED.brand,
    department = EXCLUDED.department,
    category = EXCLUDED.category,
    sub_type = EXCLUDED.sub_type,
    origin = EXCLUDED.origin,
    weight = EXCLUDED.weight,
    price = EXCLUDED.price,
    stock = EXCLUDED.stock,
    sold_count = EXCLUDED.sold_count,
    ingredients = EXCLUDED.ingredients,
    purpose = EXCLUDED.purpose,
    usage = EXCLUDED.usage,
    image_url = EXCLUDED.image_url,
    warnings = EXCLUDED.warnings;
