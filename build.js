const fs = require('fs');
const path = require('path');

// خواندن متغیرهای محیطی از .env (در صورت وجود در محیط لوکال)
const envPath = path.join(__dirname, '.env');
if (fs.existsSync(envPath)) {
    const lines = fs.readFileSync(envPath, 'utf8').split(/\r?\n/);
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) continue;
        const eqIdx = trimmed.indexOf('=');
        if (eqIdx !== -1) {
            const key = trimmed.slice(0, eqIdx).trim();
            const val = trimmed.slice(eqIdx + 1).trim().replace(/^['"]|['"]$/g, '');
            if (!process.env[key]) {
                process.env[key] = val;
            }
        }
    }
}

// پشتیبانی از نام‌گذاری‌های استاندارد Vercel و Supabase Integration
const supabaseUrl =
    process.env.SUPABASE_URL ||
    process.env.NEXT_PUBLIC_SUPABASE_URL ||
    process.env.VITE_SUPABASE_URL ||
    '';

const supabaseAnonKey =
    process.env.SUPABASE_ANON_KEY ||
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
    process.env.VITE_SUPABASE_ANON_KEY ||
    '';

const configContent = `// فایل تولید شده خودکار توسط build.js برای اتصال ایمن به Supabase
window.SUPABASE_CONFIG = {
    url: ${JSON.stringify(supabaseUrl || 'https://YOUR_PROJECT_ID.supabase.co')},
    anonKey: ${JSON.stringify(supabaseAnonKey || 'YOUR_SUPABASE_ANON_KEY')}
};
`;

const targetPath = path.join(__dirname, 'mokamel', 'supabase-config.js');
fs.writeFileSync(targetPath, configContent, 'utf8');

if (supabaseUrl && supabaseAnonKey && !supabaseUrl.includes('YOUR_PROJECT_ID')) {
    console.log('✅ پیکربندی زنده Supabase با موفقیت در mokamel/supabase-config.js ایجاد شد.');
} else {
    console.log('ℹ️ متغیرهای محیطی Supabase هنوز تنظیم نشده‌اند؛ حالت آفلاین پیش‌فرض فعال است.');
}
