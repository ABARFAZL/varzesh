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
-- درج یا به‌روزرسانی تمام ۸۰ محصول کاتالوگ فروشگاه
-- درج یا به‌روزرسانی تمام ۸۰ محصول کاتالوگ فروشگاه
-- درج یا به‌روزرسانی تمام ۸۰ محصول کاتالوگ فروشگاه
-- درج یا به‌روزرسانی تمام ۸۰ محصول کاتالوگ فروشگاه
-- درج یا به‌روزرسانی تمام ۸۰ محصول کاتالوگ فروشگاه
INSERT INTO store_products (
    id, name, brand, department, category, sub_type, origin, weight, price, stock, sold_count, ingredients, purpose, usage, image_url, warnings
) VALUES
('carnivor-beef-2000', 'پروتئین بیف ایزوله کارنیور ماسکوپولیس (Carnivor Beef)', 'MuscleMeds (Carnivor)', 'supplements', 'protein', 'beef', 'foreign', '2000 گرم', 6800000, 10, 0, ARRAY['beef_isolate', 'bcaa_branched', 'creatine_mono']::TEXT[], 'پروتئین خالص گوشت گاو هیدرولیزه شده با ۳۵۰٪ تراکم آمینو بیشتر از استیک، ۳۵۰ میلی‌گرم کراتین طبیعی، بدون لاکتوز و چربی صفر.', 'یک اسکوپ بعد از تمرین در آب سرد مصرف شود.', 'images/products/carnivor-beef-2000.svg', 'افراد حساس به ترکیبات گوشت قرمز با احتیاط مصرف کنند.'),
('genestar-egg-albumin-2000', 'پودر سفیده تخم مرغ آلبومین ژن استار (Egg Albumin)', 'ژن استار (Genestar)', 'supplements', 'protein', 'egg', 'iran', '2000 گرم', 2450000, 10, 0, ARRAY['egg_albumin', 'bcaa_branched']::TEXT[], 'پروتئین خالص سفیده تخم‌مرغ با ارزش بیولوژیکی ۱۰۰ (کامل‌ترین پروفایل آمینواسید)، هضم متوسط و مناسب رشد پایدار عضلانی.', 'یک اسکوپ صبح و یک اسکوپ بعد تمرین با آب یا شیر کم‌چرب مخلوط و میل شود.', 'images/products/genestar-egg-albumin-2000.svg', 'برای افراد دارای حساسیت به آلبومین یا تخم‌مرغ منع مصرف دارد.'),
('doobis-egg-albumin-1000', 'پودر پروتئین سفیده تخم مرغ دوبیس ۱۰۰۰ گرمی', 'دوبیس (Doobis)', 'supplements', 'protein', 'egg', 'iran', '1000 گرم', 1350000, 10, 0, ARRAY['egg_albumin', 'bcaa_branched']::TEXT[], 'تامین پروتئین استاندارد از سفیده تخم‌مرغ پاستوریزه بدون کلسترول و چربی زرده.', 'یک پیمانه در آب خنک حل شده و میل شود.', 'images/products/doobis-egg-albumin-1000.svg', 'در افراد با ناراحتی‌های گوارشی خاص با مشورت مصرف شود.'),
('vitap-vegan-protein-1000', 'پروتئین گیاهی فیت وگان ویتاپی (Plant Protein)', 'ویتاپی (VitaP)', 'supplements', 'protein', 'plant', 'iran', '1000 گرم', 980000, 10, 0, ARRAY['plant_pea_soy', 'bcaa_branched']::TEXT[], 'ترکیب پروتئین نخود، سویا و برنج قهوه‌ای، بدون لاکتوز و بدون چربی اشباع، مناسب ورزشکاران گیاه‌خوار و حساس به لبنیات.', 'یک پیمانه ۳۰ گرمی همراه با آب یا شیر بادام.', 'images/products/vitap-vegan-protein-1000.svg', 'به دلیل بافت فیبری، با آب بیشتری مخلوط شود.'),
('bsn-syntha6-2270', 'پروتئین ترکیبی سینتا ۶ بی اس ان (BSN Syntha-6)', 'BSN', 'supplements', 'protein', 'blend', 'foreign', '2270 گرم', 5200000, 10, 0, ARRAY['protein_blend', 'whey_concentrate', 'casein_micellar', 'egg_albumin', 'bcaa_branched']::TEXT[], 'ترکیب ۶ پروتئین زودجذب و دیرجذب (وی کنسانتره، وی ایزوله، کازئین، آلبومین و پپتید) برای تغذیه ۲۴ ساعته عضلات.', 'یک پیمانه در آب یا شیر حل شود.', 'images/products/bsn-syntha6-2270.svg', 'در رژیم‌های صفر کربوهیدرات مسابقاتی با احتساب کالری مصرف شود.'),
('kalleh-isolate-650', 'پودر پروتئین وی ایزوله کاله پرو ۹۰٪', 'کاله پرو (Kalleh Pro)', 'supplements', 'protein', 'isolate', 'iran', '650 گرم', 1450000, 10, 0, ARRAY['whey_isolate', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'وی ایزوله بسیار خالص با چربی و لاکتوز نزدیک به صفر، ایده‌آل برای دوره کات و مسابقات.', 'یک اسکوپ بعد تمرین و یک اسکوپ صبح در آب خنک حل شود.', 'images/products/kalleh-isolate-650.svg', 'در دمای خشک و خنک نگهداری شود.'),
('kalleh-whey-650', 'پودر پروتئین وی ۱۰۰٪ کاله پرو (Kalleh Pro)', 'کاله پرو (Kalleh Pro)', 'supplements', 'protein', 'concentrate', 'iran', '650 گرم', 1150000, 10, 0, ARRAY['whey_concentrate', 'bcaa_branched']::TEXT[], 'تامین پروتئین خالص با جذب بالا، عضله‌سازی و تسریع ریکاوری بدون قند و چربی مضر.', 'یک اسکوپ (۳۲ گرم) را با ۲۵۰ میلی‌لیتر آب یا شیر کم‌چرب بعد تمرین مصرف نمایید.', 'images/products/kalleh-whey-650.svg', 'افراد دارای حساسیت شدید به پروتئین‌های شیر با احتیاط مصرف کنند.'),
('dymatize-iso-100-2270', 'ایزو ۱۰۰ هیدرولیزه دایماتیز (Dymatize ISO 100)', 'Dymatize', 'supplements', 'protein', 'hydrolyzed', 'foreign', '2270 گرم', 8200000, 10, 0, ARRAY['whey_isolate', 'whey_hydrolyzed', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'لوکس‌ترین پروتئین وی هیدرولیزه جهان با هضم فوری و خلوص بیش از ۹۰ درصد.', 'یک پیمانه در ۲۰۰ میلی‌لیتر آب خنک بلافاصله حل می‌شود.', 'images/products/dymatize-iso-100-2270.svg', 'برای دوران کات و ورزشکاران حرفه‌ای مناسب‌ترین گزینه است.'),
('on-gold-whey-2270', 'پروتئین وی ۱۰۰٪ گلد استاندارد اپتیموم (ON Gold Whey)', 'Optimum Nutrition (ON)', 'supplements', 'protein', 'isolate', 'foreign', '2270 گرم', 6400000, 10, 0, ARRAY['whey_isolate', 'whey_concentrate', 'whey_hydrolyzed', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'پرفروش‌ترین و معتبرترین پروتئین وی جهان، غنی از پپتیدهای هیدرولیزه و ایزوله.', 'یک پیمانه ۳۰ گرمی در ۲۰۰ الی ۲۵۰ میلی‌لیتر آب سرد حل شده و مصرف شود.', 'images/products/on-gold-whey-2270.svg', 'به دلیل وجود نمونه‌های فیک در بازار، حتماً از منابع معتبر تهیه شود.'),
('on-casein-1800', 'کازئین ۱۰۰٪ گلد استاندارد اپتیموم (ON Casein)', 'Optimum Nutrition (ON)', 'supplements', 'protein', 'casein', 'foreign', '1800 گرم', 5800000, 10, 0, ARRAY['casein_micellar', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'پروتئین دیرجذب شبانه برای تغذیه پیوسته عضلات طی ۷ تا ۸ ساعت خواب شبانه.', 'یک اسکوپ در آب یا شیر قبل از خواب میل شود.', 'images/products/on-casein-1800.svg', 'قوام غلیظ‌تری نسبت به وی دارد.'),
('pnc-pure-whey-2270', 'پیور وی کارن (PNC Pure Whey)', 'کارن (PNC)', 'supplements', 'protein', 'concentrate', 'iran', '2270 گرم', 3200000, 10, 0, ARRAY['whey_concentrate', 'whey_isolate', 'bcaa_branched', 'glutamine_pure']::TEXT[], 'پروتئین کنسانتره داروسازی کارن به همراه گلوتامین و ویتامین‌ها برای عضله‌سازی خشک.', 'روزانه ۱ تا ۲ پیمانه (هر پیمانه حدود ۳۰ گرم) همراه با آب مصرف شود.', 'images/products/pnc-pure-whey-2270.svg', 'حاوی فنیل‌آلانین (برای بیماران فنیل‌کتونوری منع مصرف دارد).'),
('pnc-super-mass-5000', 'سوپر مس گینر کارن (PNC Super Mass)', 'کارن (PNC)', 'supplements', 'gainer', 'mass', 'iran', '5000 گرم', 2850000, 10, 0, ARRAY['high_calorie_gainer', 'complex_carbs', 'whey_concentrate', 'bcaa_branched']::TEXT[], 'افزایش وزن و حجم سریع برای افراد اکتومورف، تامین کربوهیدرات کمپلکس و پروتئین باکیفیت.', 'روزانه تا ۴ پیمانه در چند نوبت بین وعده‌ها و بعد از تمرین مصرف شود.', 'images/products/pnc-super-mass-5000.svg', 'افراد دارای اضافه وزن یا دیابت نباید از گینر پرکالری استفاده کنند.'),
('on-serious-mass-5400', 'سریوس مس گینر اپتیموم نوتریشن (ON Serious Mass)', 'Optimum Nutrition (ON)', 'supplements', 'gainer', 'mass', 'foreign', '5400 گرم', 4950000, 10, 0, ARRAY['high_calorie_gainer', 'complex_carbs', 'whey_concentrate', 'daily_multivitamin', 'creatine_mono']::TEXT[], 'معروف‌ترین مس گینر جهان با ۱۲۵۰ کالری و ۵۰ گرم پروتئین در هر وعده برای جهش در وزن و سایز عضلات.', 'روزانه در ۲ یا ۳ نوبت نصف پیمانه‌ای همراه با شیر پرچرب یا آب مصرف شود.', 'images/products/on-serious-mass-5400.svg', 'به دلیل کالری بالا فقط برای افراد لاغر مناسب است.'),
('pnc-carbo-2000', 'پودر کربوهیدرات خالص کارن ۲۰۰۰ گرمی', 'کارن (PNC)', 'supplements', 'gainer', 'carbo', 'iran', '2000 گرم', 890000, 10, 0, ARRAY['complex_carbs']::TEXT[], 'تامین ۱۰۰٪ مالتودکسترین خالص بدون چربی و پروتئین برای پر کردن فوری گلیکوژن کبد و عضلات.', 'قبل یا بعد از تمرین ۲ پیمانه در آب حل شود.', 'images/products/pnc-carbo-2000.svg', 'افراد دیابتی نباید مصرف کنند.'),
('applied-waxy-maize-2000', 'کربوهیدرات ذرت مومی ووکسی مایز اپلاید نوتریشن ۲۰۰۰ گرمی', 'Applied Nutrition', 'supplements', 'gainer', 'carbo', 'foreign', '2000 گرم', 2850000, 3, 168, ARRAY['waxy_maize', 'complex_carbs']::TEXT[], 'کربوهیدرات با وزن مولکولی بالا و اسمولاریته پایین برای تخلیه فوق‌سریع از معده بدون نفخ.', 'یک اسکوپ حین تمرین یا بلافاصله پس از تمرین مصرف شود.', 'images/products/applied-waxy-maize-2000.svg', 'در جای خشک و خنک نگهداری شود.'),
('vitargo-pure-carbs-1000', 'کربوهیدرات تخصصی ویتارگو خالص ۱۰۰۰ گرمی (Vitargo Pure)', 'Universal Nutrition', 'supplements', 'gainer', 'carbo', 'foreign', '1000 گرم', 3600000, 10, 246, ARRAY['vitargo_carb', 'complex_carbs']::TEXT[], 'ثبت اختراع جهانی سریع‌ترین کربوهیدرات ورزشی جهان برای پرسازی فوری عضلات بدون افت قند خون.', 'یک پیمانه بلافاصله بعد از تمرین با ۵۰۰ میلی‌لیتر آب مخلوط شود.', 'images/products/vitargo-pure-carbs-1000.svg', 'افراد دارای قند خون با پزشک مشورت نمایند.'),
('levrone-gold-lean-mass-3000', 'گلد لین مس کوین لورون (Kevin Levrone Gold Lean Mass)', 'Kevin Levrone', 'supplements', 'gainer', 'lean', 'foreign', '3000 گرم', 4200000, 10, 0, ARRAY['high_calorie_gainer', 'whey_isolate', 'whey_concentrate', 'tribulus_terrestris', 'creatine_mono', 'bcaa_branched']::TEXT[], 'گینر حجم خشک لوکس حاوی DAA، عصاره شنبلیله، ال آرژنین و HMB برای افزایش سایز عضلانی تمیز.', '۲ پیمانه در طول روز همراه آب.', 'images/products/levrone-gold-lean-mass-3000.svg', 'برای افراد زیر ۱۸ سال توصیه نمی‌شود.'),
('doobis-creatine-beta-300', 'کراتین بتا آلانین دوبیس ۳۰۰ گرمی', 'دوبیس (Doobis)', 'supplements', 'creatine', 'beta_creatine', 'iran', '300 گرم', 780000, 10, 0, ARRAY['creatine_mono', 'beta_alanine_carnosyn']::TEXT[], 'ترکیب همزمان کراتین مونوهیدرات و بتاآلانین جهت افزایش توان انفجاری و تاخیر خستگی ناشی از اسید لاکتیک.', 'یک پیمانه قبل یا بعد از تمرین در آب حل شود.', 'images/products/doobis-creatine-beta-300.svg', 'خارش ملایم بتاآلانین طبیعی است.'),
('pnc-creatine-300', 'کراتین مونوهیدرات میکرونایزد کارن', 'کارن (PNC)', 'supplements', 'creatine', 'monohydrate', 'iran', '300 گرم', 580000, 10, 0, ARRAY['creatine_mono']::TEXT[], 'افزایش توان بی‌هوازی، افزایش قدرت در تکرارهای سنگین و هیدراتاسیون داخل سلولی عضلات.', 'روزانه ۵ گرم همراه با یک لیوان آب یا آب‌میوه بعد از تمرین.', 'images/products/pnc-creatine-300.svg', 'نوشیدن روزانه حداقل ۳ لیتر آب در طول دوره الزامی است.'),
('muscletech-celltech-2700', 'سل تک کراتین پیشرفته ماسل تک (Cell-Tech)', 'MuscleTech', 'supplements', 'creatine', 'complex', 'foreign', '2700 گرم', 4500000, 10, 0, ARRAY['creatine_complex', 'creatine_mono', 'complex_carbs', 'bcaa_branched']::TEXT[], 'فرمول افسانه‌ای کراتین ترانسپورت با کربوهیدرات‌های اختصاصی برای انفجار حجم و قدرت عضلات.', 'یک اسکوپ بلافاصله بعد تمرین با آب سرد.', 'images/products/muscletech-celltech-2700.svg', 'طعم میوه‌ای و قند دارد.'),
('myprotein-creapure-500', 'کراتین خالص کریپیور مای‌پروتئین (Creapure)', 'MyProtein', 'supplements', 'creatine', 'creapure', 'foreign', '500 گرم', 2300000, 10, 0, ARRAY['creatine_creapure', 'creatine_mono']::TEXT[], 'خالص‌ترین شکل کراتین دنیا (Creapure ساخت آلمان) با خلوص ۹۹.۹۹ درصد، بدون ناخالصی و فلزات سنگین.', 'روزانه ۵ گرم همراه آب یا شیک بعد تمرین.', 'images/products/myprotein-creapure-500.svg', 'آب فراوان در طول روز مصرف کنید.'),
('pnc-arginine-1000', 'قرص ال آرژنین ۱۰۰۰ میلی‌گرم کارن', 'کارن (PNC)', 'supplements', 'amino', 'arginine', 'iran', '100 عدد', 520000, 10, 0, ARRAY['arginine_hcl']::TEXT[], 'پیش‌ساز نیتریک اکسید (NO)، گشادکننده عروق خونی، افزایش پمپاژ خون و تحریک ترشح هورمون رشد.', '۱ تا ۲ قرص قبل تمرین یا قبل خواب.', 'images/products/pnc-arginine-1000.svg', 'افراد دارای سابقه تبخال با احتیاط مصرف کنند.'),
('doobis-amino-whey-300', 'قرص آمینو وی دوبیس ۳۰۰ عددی', 'دوبیس (Doobis)', 'supplements', 'amino', 'amino_whey', 'iran', '300 عدد', 980000, 10, 0, ARRAY['amino_peptides', 'whey_concentrate', 'bcaa_branched']::TEXT[], 'تامین تمام اسیدهای آمینه شاخه‌دار و ضروری از پروتئین وی فشرده در قالب قرص‌های راحت‌هضم.', '۳ عدد قبل تمرین و ۳ عدد بعد تمرین.', 'images/products/doobis-amino-whey-300.svg', 'با آب فراوان میل شود.'),
('pnc-bcaa-300', 'پودر بی سی ای ای کارن (PNC BCAA)', 'کارن (PNC)', 'supplements', 'amino', 'bcaa', 'iran', '300 گرم', 890000, 10, 0, ARRAY['bcaa_branched']::TEXT[], 'پیشگیری از کاتابولیسم و ریزش عضلات در حین تمرین پرفشار و دوره‌های رژیم کات.', '۵ تا ۱۰ گرم در طول جلسه تمرین در بطری آب ورزشی حل شده و نوشیده شود.', 'images/products/pnc-bcaa-300.svg', 'بیش از حد مصرف نشود.'),
('genestar-pure-glutamine-300', 'گلوتامین ۱۰۰٪ خالص ژن استار ۳۰۰ گرمی', 'ژن استار (Genestar)', 'supplements', 'amino', 'glutamine', 'iran', '300 گرم', 820000, 10, 0, ARRAY['glutamine_pure']::TEXT[], 'بازسازی بافت‌های تخلیه شده، حفظ سلامت دستگاه گوارش و روده و پیشگیری از سرماخوردگی و ضعف بدنسازان.', '۵ گرم بعد تمرین و ۵ گرم قبل خواب.', 'images/products/genestar-pure-glutamine-300.svg', 'افراد دارای مشکلات شدید کلیوی مشورت کنند.'),
('pnc-hmb-120', 'کپسول اچ ام بی کارن (PNC HMB)', 'کارن (PNC)', 'supplements', 'amino', 'hmb', 'iran', '120 عدد', 950000, 10, 0, ARRAY['hmb_pure']::TEXT[], 'سپر ضد ریزش عضلات، متابولیت فعال لوسین جهت حفظ بافت عضلانی در رژیم‌های سخت کات.', 'روزانه ۳ کپسول در وعده‌های مختلف همراه آب.', 'images/products/pnc-hmb-120.svg', 'برای دیدن اثرات حداقل ۲ تا ۳ هفته مصرف شود.'),
('pnc-beta-alanine-300', 'پودر بتا آلانین کارن ۳۰۰ گرمی', 'کارن (PNC)', 'supplements', 'energy', 'beta_alanine', 'iran', '300 گرم', 790000, 10, 0, ARRAY['beta_alanine_carnosyn']::TEXT[], 'افزایش سطح کارنوزین عضلات، تاخیر در اسیدی شدن عضله و امکان اجرای تکرارهای بیشتر در ست‌های سنگین.', '۳ تا ۵ گرم ۲۰ دقیقه قبل تمرین در آب حل شود.', 'images/products/pnc-beta-alanine-300.svg', 'ایجاد سوزن‌سوزن شدن موقت در پوست بی‌خطر است.'),
('genestar-citrulline-300', 'سیترولین مالات خالص ژن استار ۳۰۰ گرمی', 'ژن استار (Genestar)', 'supplements', 'energy', 'citrulline', 'iran', '300 گرم', 740000, 10, 0, ARRAY['citrulline_malate']::TEXT[], 'افزایش چشمگیر جریان خون، رگ‌زایی عضلانی (Vascularity) و دفع آمونیاک از بافت‌های عضلانی.', '۳ تا ۵ گرم پودر حدود ۳۰ دقیقه قبل تمرین در آب.', 'images/products/genestar-citrulline-300.svg', 'طعم ترش طبیعی دارد.'),
('pnc-glucosamine-chondroitin', 'کپسول گلوکزامین و کندروئیتین پلاس ام‌اس‌ام کارن (PNC)', 'کارن (PNC)', 'supplements', 'health', 'joint', 'iran', '۶۰ عدد', 680000, 5, 184, ARRAY['joint_glucosamine', 'joint_msm']::TEXT[], 'بازسازی و ترمیم غضروف‌های ساییده‌شده، کاهش درد مفاصل و افزایش روانکاری تاندون‌ها در تمرین سنگین.', 'روزانه ۲ کپسول همراه با وعده غذایی و یک لیوان آب میل شود.', 'images/products/pnc-glucosamine-chondroitin.svg', 'افراد دارای حساسیت به سخت‌پوستان دریایی با احتیاط مصرف کنند.'),
('pnc-collagen-pure-300', 'پودر کلاژن پپتید هیدرولیزه کارن ۳۰۰ گرمی', 'کارن (PNC)', 'supplements', 'health', 'joint', 'iran', '۳۰۰ گرم', 1150000, 8, 230, ARRAY['joint_collagen']::TEXT[], 'تقویت تاندون‌ها و رباط‌های عضلانی، بهبود خاصیت ارتجاعی مفاصل و پیشگیری از آسیب‌دیدگی‌های سنگین.', 'روزانه یک پیمانه در آب یا آبمیوه مخلوط و ناشتا یا بعد تمرین میل شود.', 'images/products/pnc-collagen-pure-300.svg', 'در جای خشک و دور از نور نگهداری شود.'),
('pnc-omega3-1000', 'کپسول نرم امگا ۳ کارن ۱۰۰۰ میلی‌گرم (بدون جیوه)', 'کارن (PNC)', 'supplements', 'health', 'joint', 'iran', '۵۰ عدد', 490000, 6, 315, ARRAY['omega3_pure']::TEXT[], 'کاهش التهابات مفاصل و عضلات پس از تمرین، پشتیبانی از سلامت قلب، عروق و تمرکز مغزی.', 'روزانه ۱ تا ۲ عدد همراه با ناهار یا شام مصرف شود.', 'images/products/pnc-omega3-1000.svg', 'افراد مصرف‌کننده داروهای ضدانعقاد با پزشک مشورت کنند.'),
('pnc-caffeine-200', 'قرص کافئین ۲۰۰ میلی‌گرم کارن', 'کارن (PNC)', 'supplements', 'energy', 'caffeine', 'iran', '60 عدد', 240000, 10, 0, ARRAY['caffeine_anhydrous']::TEXT[], 'افزایش فوری هوشیاری، مهار حس خستگی، افزایش انقباضات عضلانی و بالا بردن نرخ کالری‌سوزی.', 'یک قرص ۴۵ دقیقه قبل تمرین همراه آب.', 'images/products/pnc-caffeine-200.svg', 'در ساعات پایانی شب مصرف نشود.'),
('cellucor-c4-180', 'پمپ سی ۴ اورجینال سلوکور (Cellucor C4)', 'Cellucor', 'supplements', 'energy', 'stim', 'foreign', '180 گرم', 2350000, 10, 0, ARRAY['preworkout_matrix', 'beta_alanine_carnosyn', 'citrulline_malate', 'caffeine_anhydrous']::TEXT[], 'محبوب‌ترین پیش‌تمرین جهان، ایجاد تمرکز لیزری، انرژی بالا بدون افت ناگهانی و رگ‌زایی عضلات.', 'یک پیمانه ۲۰ تا ۳۰ دقیقه قبل تمرین در ۲۰۰ میلی‌لیتر آب.', 'images/products/cellucor-c4-180.svg', 'قبل خواب مصرف نشود.'),
('pnc-l-carnitine-100', 'قرص ال کارنیتین ۱۰۰۰ میلی‌گرم کارن', 'کارن (PNC)', 'supplements', 'fatburn', 'carnitine', 'iran', '100 عدد', 480000, 10, 0, ARRAY['l_carnitine_tartrate']::TEXT[], 'انتقال اسیدهای چرب به میتوکندری سلول برای سوزاندن چربی و افزایش توان هوازی.', '۱ تا ۲ عدد قبل از فعالیت ورزشی یا تمرینات کاردیو.', 'images/products/pnc-l-carnitine-100.svg', 'افراد با سابقه تشنج یا کم‌کاری تیروئید مشورت پزشکی بگیرند.'),
('genestar-cla-1000', 'کپسول سی ال ای ۱۰۰۰ میلی‌گرم ژن استار (CLA)', 'ژن استار (Genestar)', 'supplements', 'fatburn', 'cla', 'iran', '90 عدد', 760000, 10, 0, ARRAY['cla_pure']::TEXT[], 'اسید لینولئیک کونژوگه جهت کاهش ذخایر چربی شکمی و پهلوها و مهار آنزیم لیپوپروتئین لیپاز.', '۱ کپسول همراه با هر وعده غذایی اصلی (۳ بار در روز).', 'images/products/genestar-cla-1000.svg', 'در دوران بارداری و شیردهی منع مصرف دارد.'),
('muscletech-hydroxycut-110', 'هیدروکسی‌کات الیت ماسل تک (Hydroxycut Elite)', 'MuscleTech', 'supplements', 'fatburn', 'thermo', 'foreign', '110 عدد', 2400000, 10, 0, ARRAY['thermo_extracts', 'caffeine_anhydrous', 'l_carnitine_tartrate']::TEXT[], 'چربی‌سوز ترموژنیک هاردکور، افزایش دمای درونی بدن، سرکوب اشتهای کاذب و افزایش کالری‌سوزی پایه.', '۱ عدد در روز قبل از وعده صبحانه یا تمرین.', 'images/products/muscletech-hydroxycut-110.svg', 'بسیار قوی است؛ افراد حساس به کافئین نباید مصرف کنند.'),
('pnc-zma-60', 'کپسول زد ام ای کارن (PNC ZMA)', 'کارن (PNC)', 'supplements', 'health', 'zma', 'iran', '60 عدد', 490000, 10, 0, ARRAY['zma_complex']::TEXT[], 'ترکیب ثبت‌شده روی (زینک)، منیزیم و ویتامین B6 جهت بهبود کیفیت خواب عمیق، تقویت ترشح تستوسترون شبانه و کاهش گرفتگی عضلات.', '۲ کپسول ۳۰ تا ۶۰ دقیقه قبل از خواب با معده نسبتاً خالی.', 'images/products/pnc-zma-60.svg', 'همزمان با لبنیات یا کلسیم مصرف نشود (کلسیم مانع جذب زینک است).'),
('genestar-tribulus-650', 'کپسول تریبولوس ۶۵۰ ژن استار (Tribulus)', 'ژن استار (Genestar)', 'supplements', 'health', 'tribulus', 'iran', '60 عدد', 580000, 10, 0, ARRAY['tribulus_terrestris']::TEXT[], 'عصاره استاندارد گیاه خارخاسک با ساپونین بالا جهت پشتیبانی طبیعی از تولید تستوسترون، نشاط و توان عضلانی.', 'روزانه ۱ تا ۲ کپسول همراه با غذا.', 'images/products/genestar-tribulus-650.svg', 'برای افراد زیر ۱۸ سال توصیه نمی‌شود.'),
('ala-300-pure', 'کپسول آلفا لیپوئیک اسید ۳۰۰ (ALA 300mg)', 'کارن (PNC)', 'supplements', 'health', 'ala', 'iran', '60 عدد', 460000, 10, 0, ARRAY['ala_antioxidant']::TEXT[], 'آنتی‌اکسیدان قوی محلول در آب و چربی، بهبود حساسیت به انسولین و راندن مواد غذایی و کراتین به درون سلول‌های عضلانی.', 'یک کپسول همراه با وعده کربوهیدراتی یا بعد تمرین.', 'images/products/ala-300-pure.svg', 'در صورت افت قند خون با کمی آبمیوه میل شود.'),
('vitap-daily-multi-60', 'مولتی ویتامین و مینرال دیلی ویتاپی', 'ویتاپی (VitaP)', 'supplements', 'health', 'multi', 'iran', '60 عدد', 290000, 10, 0, ARRAY['daily_multivitamin']::TEXT[], 'تامین تمام ریزمغذی‌ها، زینک، منیزیم، ویتامین C و گروه B برای رفع خستگی ورزشکار.', 'روزانه یک عدد قرص همراه با وعده غذایی.', 'images/products/vitap-daily-multi-60.svg', 'با معده خالی خورده نشود.'),
('men-tee-nike-pro', 'تیشرت فیتنس درای‌فیت نایک پرو (Nike Pro Combat Fit)', 'Nike', 'apparel_men', 'tshirt', 'fitted', 'foreign', 'وزن خالص: ۱۸۰ گرم', 1280000, 14, 42, ARRAY['تنفس‌پذیر', 'کشسانی ۴ طرفه', 'ضد عرق سریع‌خشک']::TEXT[], 'مناسب تمرینات شدید بدنسازی، کراسفیت و تمرینات وزنه جهت جلوگیری از سایش پوست و تبادل حرارت مطلوب.', 'شستشو با آب سرد حداکثر ۳۰ درجه سانتی‌گراد، بدون استفاده از مایع نرم‌کننده غلیظ.', 'images/products/men-tee-nike-pro.svg', 'از اتوکشی مستقیم با حرارت بالا خودداری شود.'),
('men-tank-venum', 'رکابی بدنسازی برش باز ونوم کلاسیک (Venum Giant Tank)', 'Venum', 'apparel_men', 'tanktop', 'stringer', 'foreign', 'وزن خالص: ۱۳۰ گرم', 950000, 8, 29, ARRAY['برش حرفه‌ای عضلات زیربغل', 'پنبه شسته‌شده ضدحساسیت', 'دوخت تخت']::TEXT[], 'آزادی کامل دامنه حرکتی در حرکات سرشانه و زیربغل، مناسب فیگورگیری و دید واضح عضلات حین تمرین.', 'قابل شستشو در ماشین لباسشویی با دور متوسط.', 'images/products/men-tank-venum.svg', 'از خشک‌کن با حرارت مستقیم استفاده نشود.'),
('men-shorts-ua', 'شلوارک تمرین کشسان آندر آرمور (Under Armour Raid 2.0)', 'Under Armour', 'apparel_men', 'shorts', 'running', 'foreign', 'وزن خالص: ۲۱۰ گرم', 1450000, 12, 35, ARRAY['جیب زیپ‌دار جانبی', 'کش کمر پهن حمایتی', 'سبک و ضد رطوبت']::TEXT[], 'طراحی شده برای اسکات عمیق، دوی سرعت و تمرینات هوازی بدون ایجاد مزاحمت یا پارگی در درزها.', 'شستشو با لباس‌های هم‌رنگ در دمای ملایم.', 'images/products/men-shorts-ua.svg', 'استفاده از سفیدکننده ممنوع است.'),
('men-pants-monsta', 'اسلش نخی فیتنس بدنسازی منستا (Monsta Classic Jogger)', 'Monsta', 'apparel_men', 'pants', 'jogger', 'foreign', 'وزن خالص: ۳۹۰ گرم', 1850000, 5, 18, ARRAY['کشبافت ضخیم مچ پا', 'فاق تقویت‌شده اسکات', 'جیب‌های عمیق']::TEXT[], 'گرم نگه داشتن عضلات و مفاصل زانو و ران حین ست‌های سنگین تمرینی و رفت‌وآمد باشگاه.', 'پشت‌ورو کردن پیش از شستشو جهت دوام چاپ لوگو.', 'images/products/men-pants-monsta.svg', 'در معرض حرارت مستقیم بخاری خشک نشود.'),
('men-tee-gymshark', 'تیشرت تخصصی جذب جیم شارک (Gymshark Critical Tee)', 'Gymshark', 'apparel_men', 'tshirt', 'fitted', 'foreign', 'وزن خالص: ۱۷۰ گرم', 1350000, 19, 54, ARRAY['برش باریک شانه و سینه', 'دوخت مقاوم پنبه‌ای', 'لوگوی حرارتی مقاوم']::TEXT[], 'برجسته نشان دادن فرم عضلانی بالاتنه همراه با حس نرمی و سازگاری بالا با پوست.', 'شستشو با آب سرد و مایع لباسشویی بدون آنزیم قوی.', 'images/products/men-tee-gymshark.svg', 'اتوکشی فقط از پشت لباس انجام شود.'),
('men-tank-golds', 'رکابی اورجینال گلدز جیم آمریکا (Gold''s Gym Muscle Tank)', 'Gold''s Gym', 'apparel_men', 'tanktop', 'muscle_tank', 'foreign', 'وزن خالص: ۱۴۰ گرم', 1100000, 7, 31, ARRAY['یقه گرد کلاسیک', 'برش زیربغل پهن', 'لوگوی جاودانه جو گلد']::TEXT[], 'نماد اصالت ورزش بدنسازی و الهام‌بخش جلسات تمرینی پرفشار و سنگین.', 'شستشوی عادی در ماشین لباسشویی.', 'images/products/men-tank-golds.svg', 'چاپ اصلی با اتوی مستقیم تماس پیدا نکند.'),
('men-tee-oversize-nike', 'تیشرت اوورسایز استریت‌ویر نایک (Nike Heavyweight Oversize Tee)', 'Nike', 'apparel_men', 'tshirt', 'oversize', 'foreign', 'وزن خالص: ۲۶۰ گرم', 1580000, 15, 38, ARRAY['قواره لش استریت‌ویر', 'پارچه گرم‌بالا سنگین ۲۶۰gsm', 'یقه کشباف مقاوم']::TEXT[], 'استایل مدرن باشگاهی و خیابانی، فوق‌العاده راحت برای بعد از تمرین و روزهای ریکاوری.', 'شستشو با آب سرد، ترجیحاً آویزان روی چوب‌لباسی جهت حفظ فرم افتادگی سرشانه.', 'images/products/men-tee-oversize-nike.svg', 'از چلاندن شدید و خشک‌کن چرخان پرسرعت اجتناب شود.'),
('men-rashguard-venum', 'راشگارد فشرده مبارزه و بدنسازی ونوم (Venum Giant Rashguard)', 'Venum', 'apparel_men', 'tshirt', 'fitted', 'foreign', 'وزن خالص: ۱۹۰ گرم', 1790000, 11, 26, ARRAY['سیستم فشرده‌سازی عضلانی', 'باند ژله‌ای ضدبالا رفتن دور کمر', 'محافظت در برابر سایش']::TEXT[], 'تسریع جریان خون و اکسیژن‌رسانی به عضلات سینه و پشت، ایده‌آل برای بدنسازی سنگین و MMA.', 'شستشوی دستی یا شستشوی ظریف ماشین با دور آرام.', 'images/products/men-rashguard-venum.svg', 'از قرار دادن روی لبه‌های زبر و چسب‌های ولکرو خودداری شود.'),
('men-stringer-monsta', 'استرینگر قهرمانی بند باریک منستا (Monsta Y-Back Stringer)', 'Monsta', 'apparel_men', 'tanktop', 'stringer', 'foreign', 'وزن خالص: ۱۱۵ گرم', 980000, 9, 22, ARRAY['بند نازک Y شکل پشت کمر', 'برش زیربغل ماکسیمم', 'حس سبکی مطلق']::TEXT[], 'نمایش کامل پمپ عضلانی سرشانه، کول و زیربغل بدون کوچک‌ترین ممانعت در کشش‌ها.', 'شستشو با آب ولرم.', 'images/products/men-stringer-monsta.svg', 'از آویزان کردن سنگین در حالت خیس خودداری شود تا فرم کش نیاید.'),
('men-shorts-nike-flex', 'شلوارک دوجداره رانینگ و تمرین نایک فلکس (Nike Flex Stride 2-in-1)', 'Nike', 'apparel_men', 'shorts', 'running', 'foreign', 'وزن خالص: ۲۳۰ گرم', 1690000, 16, 47, ARRAY['لایه شرت داخلی کامپرشن', 'جیب عرق‌گیر مخصوص گوشی', 'شب‌نما بازتابی ۳۶۰']::TEXT[], 'جلوگیری کامل از عرق‌سوز شدن ران‌ها حین دویدن طولانی، طناب‌زدن و تمرینات پا.', 'شستشو با ماشین در دور معمولی.', 'images/products/men-shorts-nike-flex.svg', 'بدون اتو.'),
('men-shorts-gymshark-apex', 'شلوارک بدنسازی بدون درز جیم شارک اپکس (Gymshark Apex 5" Seamless)', 'Gymshark', 'apparel_men', 'shorts', 'compression', 'foreign', 'وزن خالص: ۱۹۵ گرم', 1520000, 13, 39, ARRAY['طول ۵ اینچ بالای زانو', 'سوراخ‌های تهویه لیزری', 'کمر بدون کش مزاحم']::TEXT[], 'آزادی مطلق زانوها در حرکات اسکوات و پرس پا، متمرکز بر عملکرد ورزشکاران حرفه‌ای.', 'شستشو با کیسه شستشو در دمای ۳۰ درجه.', 'images/products/men-shorts-gymshark-apex.svg', 'از نرم‌کننده استفاده نکنید تا منافذ لیزری بسته نشوند.'),
('men-pants-nike-tech', 'شلوار اسلش نایک تک فلیس ارجینال (Nike Tech Fleece Joggers)', 'Nike', 'apparel_men', 'pants', 'jogger', 'foreign', 'وزن خالص: ۴۵۰ گرم', 2850000, 8, 34, ARRAY['جیب بزرگ چسبی زیپ‌دار فنی', 'برش مخروطی شیک پاچه', 'عایق حرارتی سبک']::TEXT[], 'لوکس‌ترین اسلش ورزشی دنیا با گرمابخشی بالا بدون ایجاد وزن اضافی یا حس خفگی.', 'شستشو در ماشین با آب سرد و خشک‌کردن افقی.', 'images/products/men-pants-nike-tech.svg', 'از شستشو با لباس‌های زبر و قلاب‌دار خودداری شود.'),
('men-pants-gymshark-rest', 'شلوار ورزشی درای‌فیت رست‌دی جیم شارک (Gymshark Rest Day Pants)', 'Gymshark', 'apparel_men', 'pants', 'dryfit', 'foreign', 'وزن خالص: ۳۴۰ گرم', 2150000, 10, 27, ARRAY['پارچه کشسان چهارطرفه', 'دفع رطوبت سریع', 'کمر بنددار تنظیمی محکم']::TEXT[], 'ایده‌آل برای گرم‌کردن پیش از تمرین، کشش‌های یوگا و استراحت عضلانی در روزهای تعطیل باشگاه.', 'شستشوی ساده در ماشین لباسشویی.', 'images/products/men-pants-gymshark-rest.svg', 'اتوکشی با حرارت کم.'),
('women-leg-lulu', 'لگینگ ورزشی فاق‌بلند بدون درز لولولمون (Lululemon Align)', 'Lululemon', 'apparel_women', 'leg', 'seamless', 'foreign', 'وزن خالص: ۲۰۰ گرم', 2450000, 9, 63, ARRAY['حس پوست دوم کره مانند', 'کمر گنی ۱۰ سانتی ضدلغزش', 'اسکات‌پروف ۱۰۰٪ بدون دید']::TEXT[], 'انعطاف بی‌نهایت در حرکات یوگا، پیلاتس و اسکوات سنگین بدون هیچ‌گونه افتادگی یا پیچ‌خوردگی فاق.', 'شستشوی ظریف در کیسه محافظ با آب سرد.', 'images/products/women-leg-lulu.svg', 'همراه با حوله یا پارچه‌های زبر پرزدار شسته نشود.'),
('women-bra-nike', 'نیم‌تنه ورزشی ضربه‌گیر متوسط نایک پرو (Nike Swoosh Medium Support)', 'Nike', 'apparel_women', 'sports_bra', 'high_impact', 'foreign', 'وزن خالص: ۱۱۰ گرم', 1390000, 14, 48, ARRAY['پد سینه یک‌تکه جداشونده', 'پشت قهرمانی با تهویه بالا', 'کش زیرسینه محکم و نرم']::TEXT[], 'مهار لرزش و پرش‌های حرکتی در ایروبیک، دویدن روی تردمیل، اسپینینگ و طناب‌زدن.', 'پد پیش از شستشو خارج و دستی شسته شود.', 'images/products/women-bra-nike.svg', 'از نرم‌کننده استفاده نشود تا کشسانی آن پایدار بماند.'),
('women-skirt-gymshark', 'دامن ورزشی پلیسه تنیس و فیتنس جیم‌شارک (Gymshark Court Skirt)', 'Gymshark', 'apparel_women', 'skirt', 'pleated', 'foreign', 'وزن خالص: ۱۸۵ گرم', 1650000, 8, 24, ARRAY['شلوارک کامپرشن داخلی مخفی', 'جیب مخصوص توپ تنیس و موبایل', 'پلیسه‌های شناور سبک']::TEXT[], 'طراحی جذاب و شیک برای تنیس، بدمینتون، پدل و جلسات هوازی و فیتنس پرتحرک.', 'شستشو با آب خنک جهت ماندگاری خطوط پلیسه.', 'images/products/women-skirt-gymshark.svg', 'از اتوی سنگین روی لبه پلیسه‌ها خودداری شود.'),
('women-top-ua', 'کراپ تاپ آستین‌بلند انگشتی آندر آرمور (Under Armour HeatGear Crop)', 'Under Armour', 'apparel_women', 'top_body', 'crop_top', 'foreign', 'وزن خالص: ۱۵۰ گرم', 1480000, 11, 36, ARRAY['حلقه شست نگه‌دارنده آستین', 'پنل توری توری پشت کمر', 'خنک‌کنندگی فعال پوست']::TEXT[], 'پوشش کامل بازوها و محافظت در برابر سرما حین تمرین با تجهیزات فلزی خنک باشگاه.', 'شستشو با دور ملایم ماشین لباسشویی.', 'images/products/women-top-ua.svg', 'از تماس با فلزات تیز دستگاه‌ها پیشگیری شود.'),
('women-crop-puma', 'نیم‌تنه ورزشی با پد متحرک پوما (Puma 4Keeps Mid Impact Bra)', 'Puma', 'apparel_women', 'sports_bra', 'high_impact', 'foreign', 'وزن خالص: ۱۰۵ گرم', 1150000, 16, 41, ARRAY['بندهای شانه ارگونومیک عریض', 'جذب عالی تعریق', 'کاپ فوم تنفسی']::TEXT[], 'حمایت یکنواخت از بالاتنه حین کراسفیت و تمرینات استقامتی روزانه.', 'شستشوی ساده در آب ۳۰ درجه.', 'images/products/women-crop-puma.svg', 'پدها چلانده نشوند تا دفرمه نگردند.'),
('women-leg-gymshark-adapt', 'لگینگ ورزشی بدون درز آداپت جیم‌شارک (Gymshark Adapt Seamless Leggings)', 'Gymshark', 'apparel_women', 'leg', 'seamless', 'foreign', 'وزن خالص: ۲۱۰ گرم', 2250000, 18, 57, ARRAY['الگوی سایه‌روشن برجسته‌کننده عضلات ران', 'کمر گنی فشرده محکم', 'بافت بدون درز ژاکارد']::TEXT[], 'ایده‌آل‌ترین لگینگ تخصصی برای روز تمرین پا و باسن با تضمین عدم دید در عمق اسکات.', 'شستشو با آب خنک بدون استفاده از شوینده‌های سفیدکننده.', 'images/products/women-leg-gymshark-adapt.svg', 'از سطوح زبر هالتر عاج‌دار مراقبت شود.'),
('women-leg-alo-scrunch', 'لگینگ اسکرانچ لیفت باسن آلو یوگا (Alo Yoga Booty Lift Leggings)', 'Alo Yoga', 'apparel_women', 'leg', 'scrunch', 'foreign', 'وزن خالص: ۱۹۵ گرم', 2750000, 12, 44, ARRAY['دوخت اسکرانچ مخفی فرم‌دهنده باسن', 'فاق بلند ضدچرخش کمر', 'بافت مخمل مات']::TEXT[], 'خلق زیباترین استایل ورزشی زنانه در استودیوهای پیلاتس، تی‌آرایکس و فیتنس.', 'پشت و رو کرده و در آب سرد شسته شود.', 'images/products/women-leg-alo-scrunch.svg', 'در خشک‌کن حرارتی قرار نگیرد.'),
('women-bra-lulu-energy', 'نیم‌تنه ورزشی پرتحرک لولولمون انرژی (Lululemon Energy High Support Bra)', 'Lululemon', 'apparel_women', 'sports_bra', 'high_impact', 'foreign', 'وزن خالص: ۱۲۵ گرم', 2100000, 10, 37, ARRAY['بندهای چندگانه متقاطع پشت', 'کاپ‌های فوم قالب‌گیری شده داخلی', 'ثبات بی‌نقص سینه حین پرش']::TEXT[], 'کاهش ۹۰ درصدی تکان‌های ناخوشایند در تمرینات HIIT، کراسفیت و دوی نیمه‌ماراتن.', 'شستشو با برنامه لباس‌های ورزشی ماشین لباسشویی.', 'images/products/women-bra-lulu-energy.svg', 'از مواد سفیدکننده استفاده نشود.'),
('women-bra-gymshark-crunch', 'نیم‌تنه کراس‌بک بند ضربدری جیم‌شارک (Gymshark Cross-Back Sports Bra)', 'Gymshark', 'apparel_women', 'sports_bra', 'high_impact', 'foreign', 'وزن خالص: ۱۱۵ گرم', 1450000, 15, 33, ARRAY['بندهای باریک ضربدری برای زیبایی پشت', 'پد قابل تعویض ضدعرق', 'کش زیرسینه ژاکارد']::TEXT[], 'آزادی کامل عضلات فیله و کول در حرکات بدنسازی بالاتنه و سرشانه بانوان.', 'شستشوی سریع در آب سرد.', 'images/products/women-bra-gymshark-crunch.svg', 'پدها در سایه خشک شوند.'),
('women-skirt-nike-court', 'دامن ورزشی تنیس و پدل نایک کورت با شلوارک داخلی (NikeCourt Victory Tennis Skirt)', 'Nike', 'apparel_women', 'skirt', 'pleated', 'foreign', 'وزن خالص: ۱۷۵ گرم', 1890000, 13, 29, ARRAY['پلیسه‌های کلاسیک تنیس', 'شلوارک زیرین چسبان با جیب توپ', 'کمر کشباف منعطف']::TEXT[], 'بازی حرفه‌ای در زمین تنیس خاکی و هاردکورت و ورزش‌های راکتی با بیشترین سرعت حرکت.', 'شستشو با آب خنک بدون اتوکشی مستقیم.', 'images/products/women-skirt-nike-court.svg', 'از آویختن سنگین با گیره فلزی اجتناب شود.'),
('women-skirt-lulu-rival', 'دامن تنیس کورت ریوال لولولمون (Lululemon Court Rival High-Rise Skirt)', 'Lululemon', 'apparel_women', 'skirt', 'pleated', 'foreign', 'وزن خالص: ۱۶۵ گرم', 2600000, 6, 21, ARRAY['فاق فوق‌العاده بلند گنی', 'جریان هوای ۳۶۰ درجه زیر دامن', 'جیب زیپ‌دار کوچک کلید و کارت']::TEXT[], 'بهترین دامن ورزشی دنیا از نظر سبکی، شیک‌پوشی و عملکرد ورزشی پرسرعت.', 'شستشوی ویژه لباس‌های حساس.', 'images/products/women-skirt-lulu-rival.svg', 'اتوکشی نشود.'),
('women-crop-gymshark-long', 'کراپ تاپ بافت یکپارچه سیملس جیم شارک (Gymshark Vital Seamless Long Sleeve Crop)', 'Gymshark', 'apparel_women', 'top_body', 'crop_top', 'foreign', 'وزن خالص: ۱۶۰ گرم', 1680000, 14, 42, ARRAY['سوراخ شست روی مچ آستین', 'طراحی خطوط کانتورینگ بالاتنه', 'کش زیرسینه بدون درز']::TEXT[], 'گرم نگه داشتن مفاصل دست و بازو حین تمرینات بالاتنه همراه با استایل سوپرفیت.', 'شستشو با آب سرد و مایع ملایم.', 'images/products/women-crop-gymshark-long.svg', 'از چلاندن زیاد خودداری شود.'),
('women-tee-lulu-swiftly', 'تیشرت فیتنس ضدبو لولولمون سوئیفتلی تک (Lululemon Swiftly Tech Short Sleeve)', 'Lululemon', 'apparel_women', 'top_body', 'crop_top', 'foreign', 'وزن خالص: ۱۲۰ گرم', 2200000, 9, 35, ARRAY['فناوری ضدبوی نقره Silverescent', 'بافت توری مش در پهلوها', 'دوخت تخت بدون سایش']::TEXT[], 'دویدن‌های سرعتی و تمرینات پرتعریق بدون بو گرفتن لباس حتی پس از ساعت‌ها تمرین سنگین.', 'شستشو با دور آرام در آب سرد.', 'images/products/women-tee-lulu-swiftly.svg', 'از مایع نرم‌کننده استفاده نشود تا ذرات نقره فعال بمانند.'),
('gear-wrist-harbinger', 'مچ‌بند چسبی سنگین ۱۸ اینچ هاربینگر (Harbinger Pro Wraps)', 'Harbinger', 'gym_gear', 'mochband', 'wrist_wrap', 'foreign', 'وزن جفت: ۲۲۰ گرم', 850000, 19, 68, ARRAY['کش الاستیک سنگین نظامی', 'بند شست مقاوم جهت فیکس کردن', 'چسب ولکرو با طول عمر بالا']::TEXT[], 'تثبیت زاویه مچ دست حین پرس سینه سنگین، سرشانه و حرکات فشاری جهت پیشگیری از آسیب تاندون.', 'بند شست را رد کرده و به دور مچ کشیده و چسب بزنید؛ حین ست‌های استراحت چسب را کمی شل کنید.', 'images/products/gear-wrist-harbinger.svg', 'از شستشوی مداوم با شوینده شیمیایی قوی پرهیز کنید تا خاصیت کشسانی حفظ شود.'),
('gear-belt-rdx', 'کمربند بدنسازی چرم طبیعی ۴ اینچ ۲ خار RDX (RDX 4" 2-Prong Leather Belt)', 'RDX', 'gym_gear', 'belt', 'leather_belt', 'foreign', 'وزن خالص: ۸۵۰ گرم', 2890000, 6, 27, ARRAY['چرم گاوی فشرده دولایه', 'سگک فولادی دوقلو ضدخمیدگی', 'پد محافظ گودی کمر از داخل']::TEXT[], 'ایجاد فشار داخل شکمی (Intra-Abdominal Pressure) برای محافظت از مهره‌های کمری در ددلیفت و اسکوات سنگین.', 'پیش از شروع ست اصلی کمربند را یک سوراخ محکم‌تر ببندید و پس از پایان ست بلافاصله باز نمایید.', 'images/products/gear-belt-rdx.svg', 'از نگهداری در محیط‌های مرطوب یا زیر نور مستقیم خورشید خودداری فرمایید.'),
('gear-shaker-spider', 'شیکر سه تکه مخزن‌دار اسپایدر (Spider Shaker 500ml Pro)', 'Spider', 'gym_gear', 'shaker', 'pro_shaker', 'foreign', 'گنجایش: ۵۰۰ میلی‌لیتر + ۲ مخزن', 380000, 28, 115, ARRAY['مخزن پودر پروتئین و قرص مجزا', 'فنر فلزی حل‌کننده توده‌های پودر', 'درب پیچی ۱۰۰٪ ضدچکه']::TEXT[], 'میکس روان و یکدست انواع مکمل‌های پودری (وی، گینر، کراتین) در باشگاه بدون گلوله شدن پودر.', 'ابتدا آب یا شیر را داخل شیکر ریخته و سپس پودر را اضافه نمایید، درب را محکم کرده و به مدت ۱۵ ثانیه شیک کنید.', 'images/products/gear-shaker-spider.svg', 'از ریختن آب جوش و جوشانده‌های بسیار داغ به دلیل تولید گاز پرفشار خودداری نمایید.'),
('gear-jug-hydra', 'جاگ آب ورزشی ۲.۲ لیتری هایدراپک ضد ضربه (HydraPak 2.2L Gym Jug)', 'HydraPak', 'gym_gear', 'shaker', 'pro_shaker', 'foreign', 'گنجایش: ۲۲۰۰ میلی‌لیتر (یک گالن)', 590000, 17, 52, ARRAY['دسته ارگونومیک محکم', 'درب استیل پیچی متصل به بند نایلونی', 'نشانگر حجم آب روی بدنه']::TEXT[], 'تامین هیدراتاسیون کامل ورزشکار حین تمرینات سنگین و فصول گرم سال بدون نیاز به پر کردن مکرر بطری.', 'شستشو با آب ولرم و برس مخصوص بطری.', 'images/products/gear-jug-hydra.svg', 'در فریزر قرار ندهید تا از تغییر حجم و ترکیدگی ناشی از انجماد پیشگیری شود.'),
('gear-spray-sanisport', 'اسپری ضد باکتری و خوشبوکننده کفش و دستکش سانی‌اسپرت (SaniSport Nano Spray)', 'SaniSport', 'gym_gear', 'spray', 'anti_bacterial', 'foreign', 'حجم: ۲۵۰ میلی‌لیتر', 285000, 22, 79, ARRAY['نابودکننده ۹۹.۹٪ قارچ و باکتری', 'رایحه خنک اقیانوسی', 'خشک شدن سریع بدون لکه']::TEXT[], 'رفع بوی نامطبوع عرق از کفش، دستکش بوکس، ساک ورزشی، کمربند چرمی و مچ‌بند و ضدعفونی عمقی.', 'پس از اتمام تمرین از فاصله ۱۵ سانتی‌متری داخل کفش یا دستکش اسپری کرده و اجازه دهید ۵ دقیقه در هوای آزاد خشک شود.', 'images/products/gear-spray-sanisport.svg', 'دور از شعله مستقیم و دسترس کودکان نگهداری شود. از اسپری به سمت چشم بپرهیزید.'),
('gear-straps-schiek', 'بندلیفت پنبه‌ای سنگین مچ‌دار شیک (Schiek 1000-PLS Heavy Lifting Straps)', 'Schiek', 'gym_gear', 'mochband', 'lifting_straps', 'foreign', 'وزن جفت: ۱۸۰ گرم', 680000, 15, 44, ARRAY['پد نئوپرن ضخیم دور مچ دست', 'نوار کتان ضدلغزش بر روی میله', 'طول بلند ۵۰ سانتی‌متری']::TEXT[], 'حذف خستگی پنجه و ساعد در ددلیفت، بارفیکس، زیربغل سیم‌کش و هالتر خم جهت تمرکز ۱۰۰٪ روی عضله هدف.', 'حلقه مچ‌بند را دور مچ انداخته و انتهای تسمه را ۲ دور محکم دور میله هالتر یا دمبل بپیچید و با کف دست مهار کنید.', 'images/products/gear-straps-schiek.svg', 'در حرکات یک‌ضرب وزنه‌برداری المپیکی که نیاز به رهاسازی سریع میله دارد استفاده نشود.'),
('gear-belt-sbd-lever', 'کمربند اهرمی پاورلیفتینگ ۱۳ میلی‌متری SBD انگلستان (SBD 13mm Lever Powerlifting Belt)', 'SBD Apparel', 'gym_gear', 'belt', 'leather_belt', 'foreign', 'وزن خالص: ۱۴۵۰ گرم', 6850000, 4, 16, ARRAY['ضخامت رسمی مسابقاتی ۱۳ میلی‌متر', 'مکانیزم اهرمی قفل سریع فولادی', 'مورد تایید رسمی فدراسیون جهانی IPF']::TEXT[], 'حداکثر پایداری ستون فقرات در رکوردهای جهانی اسکوات و ددلیفت سنگین بالای ۲۵۰ کیلوگرم.', 'اهرم فولادی را در کسری از ثانیه با فشار دست قفل کرده و پس از اتمام رکوردگیری با یک ضربه آزاد نمایید.', 'images/products/gear-belt-sbd-lever.svg', 'از پرتاب سگک اهرمی روی سطوح بتنی خودداری شود.'),
('gear-belt-harbinger-nylon', 'کمربند ارگونومیک نایلونی ۴ اینچ هاربینگر (Harbinger 4" Nylon Weightlifting Belt)', 'Harbinger', 'gym_gear', 'belt', 'leather_belt', 'foreign', 'وزن خالص: ۳۶۰ گرم', 1750000, 14, 39, ARRAY['سبک و منعطف برای حرکات کراسفیت', 'سگک غلطکی استیل ضدزنگ', 'چسب ولکرو با چسبندگی فوق‌العاده']::TEXT[], 'محافظت همه‌جانبه از گودی کمر بدون ایجاد محدودیت در حرکات پرتحرک مانند پرش جعبه، تراستر و کلین اند جرک.', 'تسمه را از سگک رد کرده و به اندازه دلخواه تنظیم نموده و چسب بزنید.', 'images/products/gear-belt-harbinger-nylon.svg', 'از تماس لبه‌های چسب با لباس‌های کشی بافتنی پرهیز فرمایید.'),
('gear-wraps-sbd-heavy', 'مچ‌بند مسابقه‌ای سنگین ۶۰ سانتی‌متری SBD (SBD Heavy Wrist Wraps)', 'SBD Apparel', 'gym_gear', 'mochband', 'wrist_wrap', 'foreign', 'وزن جفت: ۲۸۰ گرم', 1950000, 8, 23, ARRAY['سفتی و استحکام گچی ماکسیمم', 'حلقه شست پهن تقویت‌شده', 'تاییدیه IPF جهت مسابقات بین‌المللی']::TEXT[], 'قفل کردن کامل مفصل مچ دست در بنچ‌پرس سنگین، اسکوات سنگین بار رو و پرس‌های سرشانه رکوردشکن.', 'به صورت محکم به دور مچ پیچیده و چسب ولکروی عریض را محکم بچسبانید.', 'images/products/gear-wraps-sbd-heavy.svg', 'به دلیل ترمز خونی بالا فقط حین اجرای ست بسته شود و بین ست‌ها حتماً باز گردد.'),
('gear-sleeves-sbd-7mm', 'زانوبند نئوپرن ۷ میلی‌متری اسکات SBD (SBD 7mm Neoprene Knee Sleeves)', 'SBD Apparel', 'gym_gear', 'mochband', 'wrist_wrap', 'foreign', 'وزن جفت: ۴۶۰ گرم', 4200000, 5, 19, ARRAY['ضخامت ۷ میلی‌متر نئوپرن با تراکم بالا', 'دوخت چهارلایه‌ای زرهی ضدپارگی', 'کمک فنری به بالا آمدن در عمق اسکات']::TEXT[], 'گرم نگه داشتن کامل مفصل زانو، افزایش جریان مایع سینوویال و محافظت در برابر آسیب مینیسک و رباط صلیبی.', 'پایین زانوبند را تا نصفه برگردانده و از مچ پا به سمت بالا بکشید تا روی کشکک زانو قرار گیرد.', 'images/products/gear-sleeves-sbd-7mm.svg', 'شستشو منحصراً با دست در آب ولرم، بدون فشار دادن و چلاندن شدید.'),
('gear-shaker-blender-strada', 'شیکر استیل دوجداره ضدچکه بلندر باتل استرادا (BlenderBottle Strada Steel 710ml)', 'BlenderBottle', 'gym_gear', 'shaker', 'steel_shaker', 'foreign', 'حجم: ۷۱۰ میلی‌لیتر (۲۴oz)', 1490000, 16, 46, ARRAY['استیل ۳۰۴ دوجداره با عایق خلأ', 'سرد نگه داشتن نوشیدنی تا ۲۴ ساعت', 'درب دکمه‌ای قفل‌دار ضدبازشدن تصادفی']::TEXT[], 'نوشیدن شیک پروتئینی خنک و دلچسب حتی ساعت‌ها پس از خروج از منزل در گرم‌ترین روزهای تابستان.', 'همراه با توپ استیل ویسک بلندر باتل برای میکس فوق‌العاده نرم و یکدست.', 'images/products/gear-shaker-blender-strada.svg', 'در مایکروویو قرار نگیرد.'),
('gear-shaker-vortex-electric', 'شیکر برقی شارژی پروتئین ولترکس ورتکس (Voltrx Electric Protein Shaker 600ml)', 'Voltrx', 'gym_gear', 'shaker', 'pro_shaker', 'foreign', 'حجم: ۶۰۰ میلی‌لیتر', 1850000, 11, 38, ARRAY['موتور توربینی قدرتمند با سرعت ۵۰۰۰ دور بر دقیقه', 'شارژر مگنتی تایپ سی Type-C', 'بدنه شفاف تریتان نشکن']::TEXT[], 'حل کردن آنی سرسخت‌ترین پودرهای گینر، کازئین و تخم‌مرغ با فشار یک دکمه بدون نیاز به تکان دادن دست.', 'مایع را ریخته، دکمه را بزنید تا گرداب تشکیل شود، سپس پودر را از بالا اضافه کنید.', 'images/products/gear-shaker-vortex-electric.svg', 'پایه موتور را در آب غوطه‌ور نسازید؛ فقط با دستمال مرطوب تمیز شود.'),
('gear-chalk-liquid-250', 'گچ و پودر منیزیم مایع بدنسازی بیست گیر (Beast Gear Liquid Chalk 250ml)', 'Beast Gear', 'gym_gear', 'spray', 'anti_bacterial', 'foreign', 'حجم: ۲۵۰ میلی‌لیتر', 420000, 25, 83, ARRAY['خشک شدن در کمتر از ۱۰ ثانیه', 'بدون ایجاد گردوغبار و ریخت‌وپاش در باشگاه', 'چسبندگی بی‌نظیر به میله هالتر']::TEXT[], 'جلوگیری کامل از لیز خوردن میله هالتر و دمبل از دست به دلیل عرق کف دست در حرکات سنگین ددلیفت و بارفیکس.', 'چند قطره کف دست ریخته، به هم بمالید و ۱۰ ثانیه در هوا تکان دهید تا لایه سفید گچی ضدلغزش تشکیل شود.', 'images/products/gear-chalk-liquid-250.svg', 'روی پوست‌های دارای زخم باز مالیده نشود. پس از تمرین دست‌ها را با آب و صابون بشویید.'),
('gear-spray-adidas-nano', 'اسپری نانو ضدعفونی تجهیزات و دستکش آدیداس کامبت (Adidas Combat Equipment Spray 300ml)', 'Adidas Combat', 'gym_gear', 'spray', 'anti_bacterial', 'foreign', 'حجم: ۳۰۰ میلی‌لیتر', 340000, 20, 61, ARRAY['مهار ۹۹.۹٪ باکتری‌های مقاوم استافیلوکوک', 'محافظ بافت چرم و پارچه‌های ورزشی', 'افشانه مه ریز ارگونومیک']::TEXT[], 'ضدعفونی کردن سریع تشک تمرین، مت یوگا، دستکش‌های چرمی، کلاه و ساق‌بند بدون خیس کردن بافت داخلی.', 'روی سطح مورد نظر اسپری کرده و اجازه دهید ۲ دقیقه بماند.', 'images/products/gear-spray-adidas-nano.svg', 'از تابش مستقیم نور خورشید و دمای بالای ۵۰ درجه سانتی‌گراد دور نگه داشته شود.')
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
