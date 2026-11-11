// =========================================================================
// کلاینت اتصال اختصاصی فروشگاه به Supabase (Supabase Cloud Sync)
// =========================================================================

// خواندن کلیدها از فایل supabase-config.js (تولید شده توسط build.js یا تنظیمات مستقیم)
const SUPABASE_PROJECT_URL = window.SUPABASE_CONFIG?.url || "https://YOUR_PROJECT_ID.supabase.co";
const SUPABASE_ANON_KEY = window.SUPABASE_CONFIG?.anonKey || "YOUR_SUPABASE_ANON_KEY";

let supabaseClient = null;
let isSupabaseConnected = false;

// راه‌اندازی اولیه کلاینت
function initSupabaseClient() {
    if (
        window.supabase &&
        SUPABASE_PROJECT_URL &&
        SUPABASE_ANON_KEY &&
        !SUPABASE_PROJECT_URL.includes("YOUR_PROJECT_ID") &&
        !SUPABASE_ANON_KEY.includes("YOUR_SUPABASE_ANON_KEY")
    ) {
        try {
            supabaseClient = window.supabase.createClient(SUPABASE_PROJECT_URL, SUPABASE_ANON_KEY);
            isSupabaseConnected = true;
            window.isSupabaseConnected = true;
            console.log("✅ اتصال به سرور ابری Supabase با موفقیت برقرار شد.");
            syncProductsFromSupabase();
        } catch (err) {
            console.warn("⚠️ خطا در اتصال به Supabase، استفاده از دیتابیس محلی:", err);
            isSupabaseConnected = false;
            window.isSupabaseConnected = false;
        }
    } else {
        window.isSupabaseConnected = false;
        console.log("ℹ️ فروشگاه در حالت مستقل (Local Storage) آماده کار است.");
    }
}

// خواندن محصولات زنده از جدول store_products در سوپابیس
async function syncProductsFromSupabase() {
    if (!isSupabaseConnected || !supabaseClient) return;
    try {
        const { data, error } = await supabaseClient
            .from("store_products")
            .select("*")
            .eq("is_active", true);

        if (error) throw error;

        if (data && data.length > 0 && typeof fullStoreDB !== "undefined") {
            console.log(`📦 تعداد ${data.length} محصول از دیتابیس Supabase دریافت شد.`);
            data.forEach(dbProd => {
                const localProd = fullStoreDB.find(p => p.id === dbProd.id);
                if (localProd) {
                    if (typeof dbProd.stock === "number") localProd.stock = dbProd.stock;
                    if (typeof dbProd.sold_count === "number") localProd.soldCount = dbProd.sold_count;
                    if (typeof dbProd.price === "number" && dbProd.price > 0) localProd.price = dbProd.price;
                }
            });
            if (typeof renderAll === "function") renderAll();
        }
    } catch (e) {
        console.warn("عدم امکان دریافت دیتا از Supabase:", e.message);
    }
}

// ثبت سفارش جدید در جدول store_orders و اقلام در store_order_items در سوپابیس
async function submitOrderToSupabase(orderData) {
    // ذخیره نسخه پشتیبان سفارش در حافظه مرورگر کاربر برای تاریخچه
    try {
        const history = JSON.parse(localStorage.getItem("abarstore_order_history") || "[]");
        history.unshift({ ...orderData, createdAt: new Date().toISOString() });
        localStorage.setItem("abarstore_order_history", JSON.stringify(history.slice(0, 20)));
    } catch (_) {}

    if (!isSupabaseConnected || !supabaseClient) {
        return { success: true, localOnly: true };
    }

    try {
        const { data: order, error: orderErr } = await supabaseClient
            .from("store_orders")
            .insert([{
                customer_name: orderData.name,
                customer_phone: orderData.phone,
                customer_province: orderData.province || null,
                customer_city: orderData.city || null,
                shipping_address: orderData.address,
                total_amount: orderData.totalAmount,
                discount_amount: orderData.discountAmount || 0,
                shipping_method: orderData.shippingMethod || "express",
                payment_method: orderData.paymentMethod || "online",
                notes: orderData.notes || null,
                tracking_code: orderData.trackingCode || null,
                payment_status: orderData.paymentMethod === "cod" ? "pending" : "paid",
                order_status: "registered"
            }])
            .select()
            .single();

        if (orderErr) throw orderErr;

        // ثبت ریز اقلام سفارش و کسر موجودی انبار
        if (order && orderData.items && orderData.items.length > 0) {
            for (const it of orderData.items) {
                try {
                    await supabaseClient.from("store_order_items").insert([{
                        order_id: order.id,
                        product_id: it.id,
                        quantity: it.qty || 1,
                        unit_price: it.unitPrice || 0,
                        total_price: (it.unitPrice || 0) * (it.qty || 1)
                    }]);

                    await supabaseClient.rpc("process_store_purchase", {
                        p_product_id: it.id,
                        p_quantity: it.qty || 1
                    });
                } catch (itemErr) {
                    console.warn("یادداشت همگام‌سازی قلم سفارش:", it.id, itemErr.message);
                }
            }
        }

        return { success: true, orderId: order.id, localOnly: false };
    } catch (err) {
        console.error("خطا در ثبت سفارش در Supabase:", err);
        return { success: false, error: err.message, localOnly: true };
    }
}

window.submitOrderToSupabase = submitOrderToSupabase;
window.syncProductsFromSupabase = syncProductsFromSupabase;

// اجرای اولیه پس از لود صفحه
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSupabaseClient);
} else {
    initSupabaseClient();
}
