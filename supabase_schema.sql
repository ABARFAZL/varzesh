-- ========================================================
-- پلتفرم مدیریت مربیان و شاگردان بدنسازی (Fitness Platform Schema)
-- طراحی شده برای Supabase / PostgreSQL
-- ========================================================

-- فعال‌سازی افزونه UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ۱. جدول مربیان (Coaches)
CREATE TABLE IF NOT EXISTS coaches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    bio TEXT,
    specialty VARCHAR(100) DEFAULT 'بدنسازی و هایپرتروفی',
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ۲. جدول شاگردان (Trainees)
CREATE TABLE IF NOT EXISTS trainees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID REFERENCES coaches(id) ON DELETE CASCADE NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    gender VARCHAR(10) DEFAULT 'آقا',
    birth_date DATE,
    height_cm NUMERIC(5,2),
    weight_kg NUMERIC(5,2),
    target_goal VARCHAR(150) DEFAULT 'عضله‌سازی و فرم‌دهی',
    injuries_or_limitations TEXT, -- آسیب‌ها یا محدودیت‌ها (مثلاً شکستگی پای چپ)
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ۳. جدول برنامه‌های تمرینی (Workout Plans)
CREATE TABLE IF NOT EXISTS workout_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID REFERENCES coaches(id) ON DELETE CASCADE NOT NULL,
    trainee_id UUID REFERENCES trainees(id) ON DELETE CASCADE NOT NULL,
    title VARCHAR(200) NOT NULL, -- عنوان برنامه (مثلاً برنامه ۵ روزه تفکیکی)
    days_per_week INT DEFAULT 5 NOT NULL, -- تعداد روزهای تمرین در هفته (۳ تا ۶ روز)
    split_type VARCHAR(100) DEFAULT 'Upper / Lower', -- سیستم تمرینی
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    coach_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ۴. جدول روزهای برنامه (Workout Days)
CREATE TABLE IF NOT EXISTS workout_days (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    plan_id UUID REFERENCES workout_plans(id) ON DELETE CASCADE NOT NULL,
    day_number INT NOT NULL, -- ۱ تا ۷
    day_name VARCHAR(50) NOT NULL, -- شنبه، یکشنبه و...
    focus_muscles VARCHAR(200) NOT NULL, -- سینه، پشت، سرشانه و...
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ۵. جدول حرکات هر روز (Day Exercises)
CREATE TABLE IF NOT EXISTS day_exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    day_id UUID REFERENCES workout_days(id) ON DELETE CASCADE NOT NULL,
    order_index INT NOT NULL, -- شماره ردیف حرکت
    name_fa VARCHAR(150) NOT NULL, -- نام فارسی حرکت
    name_en VARCHAR(150), -- نام بین‌المللی انگلیسی
    sets INT NOT NULL DEFAULT 4,
    reps VARCHAR(50) NOT NULL DEFAULT '۱۲',
    tempo VARCHAR(30) DEFAULT '۱-۱-۳-۱', -- تمپوی بیومکانیک
    equipment VARCHAR(200), -- تجهیزات (دمبل، سیم‌کش و...)
    grip_and_wrist_technique TEXT, -- بیومکانیک دست و مچ
    target_muscles TEXT, -- عضلات هدف با درصد
    rest_seconds INT DEFAULT 60, -- زمان استراحت بین ست‌ها
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ۶. جدول سوابق تمرین و ثبت وزنه‌ها توسط شاگرد (Workout Logs)
CREATE TABLE IF NOT EXISTS workout_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trainee_id UUID REFERENCES trainees(id) ON DELETE CASCADE NOT NULL,
    exercise_id UUID REFERENCES day_exercises(id) ON DELETE CASCADE NOT NULL,
    logged_date DATE DEFAULT CURRENT_DATE NOT NULL,
    set_number INT NOT NULL,
    weight_kg NUMERIC(6,2),
    reps_performed INT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- فعال‌سازی دسترسی‌های امنیتی سطح ردیف (Row Level Security - RLS)
ALTER TABLE coaches ENABLE ROW LEVEL SECURITY;
ALTER TABLE trainees ENABLE ROW LEVEL SECURITY;
ALTER TABLE workout_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE workout_days ENABLE ROW LEVEL SECURITY;
ALTER TABLE day_exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE workout_logs ENABLE ROW LEVEL SECURITY;

-- سیاست امنیتی ساده: مربیان به داده‌های شاگردان خود دسترسی کامل دارند
CREATE POLICY "مربیان می‌توانند شاگردان خود را مدیریت کنند" 
ON trainees FOR ALL 
USING (coach_id IN (SELECT id FROM coaches WHERE user_id = auth.uid()));

CREATE POLICY "مربیان می‌توانند برنامه‌های شاگردان خود را مدیریت کنند" 
ON workout_plans FOR ALL 
USING (coach_id IN (SELECT id FROM coaches WHERE user_id = auth.uid()));
