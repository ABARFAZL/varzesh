/**
 * سامانه ویژگی‌های تعاملی و پیشرفته فروشگاه مگااستور ورزشی
 * نگارش: 2.0 (Innovations Engine & Developer Lab)
 */

(function () {
    "use strict";

    // کلیدهای ذخیره‌سازی در حافظه مرورگر
    const DEV_MODE_KEY = "developer_mode_enabled";
    const SETTINGS_KEY = "innovations_settings";

    // وضعیت پیش‌فرض تمام ۸ نوآوری درخواستی
    const defaultSettings = {
        bottomSheet: true,   // ایده ۱: برگه کشویی از پایین در موبایل
        quickPeek: true,     // ایده ۲: پیش‌نمایش لمس طولانی در موبایل
        smartBadges: true,   // ایده ۳: حباب‌های هوشمند فیلترهای فعال
        glassDock: true,     // ایده ۴: نوار شیشه‌ای شناور پایین موبایل
        cardFlip: true,      // ایده ۵: ورق زدن سه‌بعدی کارت و گالری چند عکسی
        compareMode: true,   // ایده ۷: مقایسه با قفل شدن سطر بالای صفحه
        flyToCart: true,     // ایده ۹: انیمیشن پرتاب کالا به سبد خرید
        edgeTabs: true       // ایده ۱۰: دستگیره‌های باریک لبه صفحه
    };

    function getSettings() {
        try {
            const saved = localStorage.getItem(SETTINGS_KEY);
            return saved ? Object.assign({}, defaultSettings, JSON.parse(saved)) : Object.assign({}, defaultSettings);
        } catch (e) {
            return Object.assign({}, defaultSettings);
        }
    }

    function saveSettings(settings) {
        try {
            localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
        } catch (e) {}
    }

    let currentSettings = getSettings();

    // بررسی فعال بودن حالت دولوپر (مخفی روی ورسل برای کاربران عادی)
    function isDevModeActive() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get("dev") === "1" || urlParams.get("dev") === "true" || urlParams.get("test") === "1") {
            return true;
        }
        return localStorage.getItem(DEV_MODE_KEY) === "true";
    }

    function setDevMode(active) {
        localStorage.setItem(DEV_MODE_KEY, active ? "true" : "false");
        const bar = document.getElementById("devControlBar");
        if (bar) {
            bar.classList.toggle("dev-bar-visible", active);
        }
    }

    // --------------------------------------------------------------------------
    // ۰. ساخت و راه‌اندازی نوار تست توسعه‌دهنده (Developer Test Bar)
    // --------------------------------------------------------------------------
    function createDeveloperBar() {
        if (document.getElementById("devControlBar")) return;

        const bar = document.createElement("div");
        bar.id = "devControlBar";
        bar.innerHTML = `
            <div class="dev-bar-header">
                <span>🛠️ آزمایشگاه توسعه</span>
            </div>
            <div class="dev-switches-group">
                <button type="button" class="dev-toggle-chip ${currentSettings.bottomSheet ? 'active' : ''}" data-key="bottomSheet">
                    <span>📱 برگه کشویی پایین (ایده ۱)</span>
                </button>
                <button type="button" class="dev-toggle-chip ${currentSettings.quickPeek ? 'active' : ''}" data-key="quickPeek">
                    <span>🔍 پیش‌نمایش لمس طولانی (ایده ۲)</span>
                </button>
                <button type="button" class="dev-toggle-chip ${currentSettings.smartBadges ? 'active' : ''}" data-key="smartBadges">
                    <span>💡 حباب فیلترهای فعال (ایده ۳)</span>
                </button>
                <button type="button" class="dev-toggle-chip ${currentSettings.glassDock ? 'active' : ''}" data-key="glassDock">
                    <span>🪟 نوار شیشه‌ای موبایل (ایده ۴)</span>
                </button>
                <button type="button" class="dev-toggle-chip ${currentSettings.cardFlip ? 'active' : ''}" data-key="cardFlip">
                    <span>🔄 ورق زدن و گالری (ایده ۵)</span>
                </button>
                <button type="button" class="dev-toggle-chip ${currentSettings.compareMode ? 'active' : ''}" data-key="compareMode">
                    <span>⚖️ مقایسه با قفل سطر بالا (ایده ۷)</span>
                </button>
                <button type="button" class="dev-toggle-chip ${currentSettings.flyToCart ? 'active' : ''}" data-key="flyToCart">
                    <span>🚀 پرواز به سبد خرید (ایده ۹)</span>
                </button>
                <button type="button" class="dev-toggle-chip ${currentSettings.edgeTabs ? 'active' : ''}" data-key="edgeTabs">
                    <span>📑 زبانه‌های لبه صفحه (ایده ۱۰)</span>
                </button>
            </div>
            <button type="button" class="dev-close-btn" id="btnDevCloseBar" title="مخفی کردن نوار تست">✕</button>
        `;
        document.body.appendChild(bar);

        bar.querySelectorAll(".dev-toggle-chip").forEach(chip => {
            chip.addEventListener("click", () => {
                const key = chip.getAttribute("data-key");
                currentSettings[key] = !currentSettings[key];
                chip.classList.toggle("active", currentSettings[key]);
                saveSettings(currentSettings);
                applyAllFeatures();
            });
        });

        const closeBtn = document.getElementById("btnDevCloseBar");
        if (closeBtn) {
            closeBtn.addEventListener("click", () => {
                setDevMode(false);
            });
        }

        if (isDevModeActive()) {
            bar.classList.add("dev-bar-visible");
        }
    }

    // تریگرهای مخفی ورود به پنل توسعه‌دهنده
    function setupDevActivationTriggers() {
        const brandBox = document.querySelector(".brand-title-box");
        let clickCount = 0;
        let lastClickTime = 0;

        if (brandBox) {
            brandBox.addEventListener("click", () => {
                const now = Date.now();
                if (now - lastClickTime < 650) {
                    clickCount++;
                } else {
                    clickCount = 1;
                }
                lastClickTime = now;

                if (clickCount >= 3) {
                    const current = isDevModeActive();
                    setDevMode(!current);
                    clickCount = 0;
                }
            });
        }

        window.addEventListener("keydown", (e) => {
            if (e.ctrlKey && e.shiftKey && (e.key === "D" || e.key === "d")) {
                const current = isDevModeActive();
                setDevMode(!current);
            }
        });
    }

    // --------------------------------------------------------------------------
    // ۱. ایده ۱: برگه کشویی پایین در موبایل (Bottom Sheet Modal)
    // --------------------------------------------------------------------------
    function applyBottomSheetFeature() {
        const isMobile = window.innerWidth <= 1024;
        if (currentSettings.bottomSheet && isMobile) {
            document.body.classList.add("bottom-sheet-mode");

            ["filterSidebar", "ingredientsSidebar"].forEach(id => {
                const sb = document.getElementById(id);
                if (sb && !sb.querySelector(".bottom-sheet-handle")) {
                    const handle = document.createElement("div");
                    handle.className = "bottom-sheet-handle";
                    handle.title = "لمس یا کشیدن برای بستن منو";
                    handle.addEventListener("click", () => {
                        if (typeof window.closeAllSidebars === 'function') {
                            window.closeAllSidebars();
                        }
                    });
                    sb.insertBefore(handle, sb.firstChild);
                }
            });
        } else {
            document.body.classList.remove("bottom-sheet-mode");
            document.querySelectorAll(".bottom-sheet-handle").forEach(h => h.remove());
        }
    }

    // --------------------------------------------------------------------------
    // ۲. ایده ۲: پیش‌نمایش سریع لمس طولانی در موبایل (Quick Peek on Long Press)
    // --------------------------------------------------------------------------
    let peekOverlay = null;

    function createQuickPeekOverlay() {
        if (document.getElementById("quickPeekOverlay")) return;

        peekOverlay = document.createElement("div");
        peekOverlay.id = "quickPeekOverlay";
        peekOverlay.className = "quick-peek-overlay";
        peekOverlay.innerHTML = `
            <div class="quick-peek-card" id="quickPeekCard" onclick="event.stopPropagation()">
                <div class="quick-peek-img-box" id="peekImgBox"></div>
                <h3 class="quick-peek-title" id="peekTitle">نام محصول</h3>
                <div class="quick-peek-specs" id="peekSpecs"></div>
                <div class="quick-peek-footer">
                    <span class="quick-peek-price" id="peekPrice">۰ تومان</span>
                    <button type="button" class="quick-peek-btn-buy" id="peekBuyBtn">افزودن سریع به سبد</button>
                </div>
            </div>
        `;
        document.body.appendChild(peekOverlay);
        peekOverlay.addEventListener("click", closeQuickPeek);
    }

    function showQuickPeek(item) {
        if (!currentSettings.quickPeek || !item) return;
        createQuickPeekOverlay();

        const imgBox = document.getElementById("peekImgBox");
        const title = document.getElementById("peekTitle");
        const specs = document.getElementById("peekSpecs");
        const price = document.getElementById("peekPrice");
        const buyBtn = document.getElementById("peekBuyBtn");

        if (imgBox) {
            imgBox.innerHTML = item.image ? 
                `<img src="${item.image}" alt="${item.name}">` : 
                (item.svg || '');
        }
        if (title) title.textContent = item.name;
        if (price) price.textContent = (item.price || 0).toLocaleString('fa-IR') + ' تومان';

        if (specs) {
            const tags = item.ingredients || item.specs || [];
            specs.innerHTML = tags.slice(0, 4).map(t => 
                `<span class="quick-peek-spec-chip">✓ ${t.replace(/_/g, ' ')}</span>`
            ).join('') + `<span class="quick-peek-spec-chip" style="color:#22c55e;">وزن: ${item.weight || 'استاندارد'}</span>`;
        }

        if (buyBtn) {
            buyBtn.onclick = (e) => {
                if (typeof window.handleAddToCart === 'function') {
                    window.handleAddToCart(item.id, e);
                }
                closeQuickPeek();
            };
        }

        peekOverlay.classList.add("open");
        if (navigator.vibrate) {
            try { navigator.vibrate(35); } catch(e){}
        }
    }

    function closeQuickPeek() {
        if (peekOverlay) {
            peekOverlay.classList.remove("open");
        }
    }

    function bindQuickPeekEvents() {
        const cards = document.querySelectorAll(".product-card");
        cards.forEach(card => {
            if (card._peekBound) return;
            card._peekBound = true;

            let pressTimer = null;
            let startX = 0, startY = 0;

            card.addEventListener("touchstart", (e) => {
                if (!currentSettings.quickPeek) return;
                const touch = e.touches[0];
                startX = touch.clientX;
                startY = touch.clientY;

                pressTimer = setTimeout(() => {
                    const prodId = card.id ? card.id.replace("prodCard_", "") : null;
                    if (prodId && window.fullStoreDB) {
                        const item = window.fullStoreDB.find(p => p.id === prodId);
                        if (item) showQuickPeek(item);
                    }
                }, 480);
            }, { passive: true });

            card.addEventListener("touchmove", (e) => {
                const touch = e.touches[0];
                if (Math.abs(touch.clientX - startX) > 10 || Math.abs(touch.clientY - startY) > 10) {
                    clearTimeout(pressTimer);
                }
            }, { passive: true });

            card.addEventListener("touchend", () => {
                clearTimeout(pressTimer);
            });
        });
    }

    // --------------------------------------------------------------------------
    // ۳. ایده ۳: حباب‌های هوشمند فیلترهای فعال (Smart Active Badges)
    // --------------------------------------------------------------------------
    function updateSmartFilterBadges() {
        if (!currentSettings.smartBadges) return;

        const rightBtn = document.getElementById("btnToggleRightSidebar") || document.getElementById("mobileCornerRightBtn");
        const leftBtn = document.getElementById("btnToggleLeftSidebar") || document.getElementById("mobileCornerLeftBtn");

        let filterState = { brand: "all", origin: "all", ingredients: [] };
        if (typeof window.getCurrentFilterState === 'function') {
            filterState = window.getCurrentFilterState();
        } else {
            filterState.brand = window.currentBrand || "all";
            filterState.origin = window.currentOrigin || "all";
            filterState.ingredients = window.selectedIngredients || [];
        }

        let rightFilterCount = 0;
        if (filterState.brand && filterState.brand !== "all") rightFilterCount++;
        if (filterState.origin && filterState.origin !== "all") rightFilterCount++;

        let leftFilterCount = Array.isArray(filterState.ingredients) ? filterState.ingredients.length : 0;

        if (rightBtn) {
            let badge = rightBtn.querySelector(".smart-active-badge");
            if (!badge) {
                badge = document.createElement("span");
                badge.className = "smart-active-badge";
                rightBtn.appendChild(badge);
            }
            badge.textContent = rightFilterCount;
            badge.classList.toggle("show", rightFilterCount > 0);
        }

        if (leftBtn) {
            let badge = leftBtn.querySelector(".smart-active-badge");
            if (!badge) {
                badge = document.createElement("span");
                badge.className = "smart-active-badge";
                leftBtn.appendChild(badge);
            }
            badge.textContent = leftFilterCount;
            badge.classList.toggle("show", leftFilterCount > 0);
        }

        // دکمه شناور پاکسازی همه فیلترها در صورت فعال بودن
        let clearBtn = document.getElementById("floatingClearFiltersBtn");
        const totalActive = rightFilterCount + leftFilterCount;
        if (totalActive > 0) {
            if (!clearBtn) {
                clearBtn = document.createElement("button");
                clearBtn.id = "floatingClearFiltersBtn";
                clearBtn.className = "clear-all-floating-btn";
                clearBtn.innerHTML = `<span>✕ پاکسازی ${totalActive} فیلتر فعال</span>`;
                document.body.appendChild(clearBtn);
                clearBtn.addEventListener("click", () => {
                    if (typeof window.resetAllFilters === 'function') {
                        window.resetAllFilters();
                    }
                });
            } else {
                clearBtn.querySelector("span").textContent = `✕ پاکسازی ${totalActive} فیلتر فعال`;
            }
            clearBtn.classList.add("show");
        } else if (clearBtn) {
            clearBtn.classList.remove("show");
        }
    }

    // --------------------------------------------------------------------------
    // ۴. ایده ۴: نوار شناور شیشه‌ای موبایل (Floating Glass Dock)
    // --------------------------------------------------------------------------
    function applyGlassDockFeature() {
        if (currentSettings.glassDock) {
            document.body.classList.add("glass-dock-active");
        } else {
            document.body.classList.remove("glass-dock-active");
        }
    }

    // --------------------------------------------------------------------------
    // ۵. ایده ۵: ورق زدن سه‌بعدی کارت و گالری چند عکسی (3D Flip & Multi-Angle Gallery)
    // --------------------------------------------------------------------------
    function enhanceProductCardsWithFlipAndGallery() {
        if (!currentSettings.cardFlip) return;

        const cards = document.querySelectorAll(".product-card");
        cards.forEach(card => {
            if (card._flipEnhanced) return;
            card._flipEnhanced = true;

            const prodId = card.id ? card.id.replace("prodCard_", "") : null;
            if (!prodId || !window.fullStoreDB) return;

            const item = window.fullStoreDB.find(p => p.id === prodId);
            if (!item) return;

            // ۱. دکمه چرخش سه‌بعدی ۱۸۰ درجه
            const flipBtn = document.createElement("button");
            flipBtn.type = "button";
            flipBtn.className = "card-flip-trigger-btn";
            flipBtn.title = "ورق زدن کارت و مشاهده جدول پشت قوطی";
            flipBtn.innerHTML = `🔄`;
            card.appendChild(flipBtn);

            flipBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                card.classList.toggle("flipped");
            });

            // ۲. پنل پشت کارت (جدول ارزش غذایی)
            let backFace = card.querySelector(".card-flip-back");
            if (!backFace) {
                backFace = document.createElement("div");
                backFace.className = "card-flip-back";
                backFace.innerHTML = `
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:0.75rem; font-weight:900; color:var(--theme-color, #38bdf8);">جدول ارزش غذایی</span>
                            <span style="font-size:0.7rem; color:#22c55e;">تضمین ۱۰۰٪ خلوص</span>
                        </div>
                        <table class="nutrition-back-table">
                            <tr><th>ماده موثره</th><th>مقدار در هر سروینگ</th></tr>
                            <tr><td>خلوص فرمول</td><td>${item.weight || 'استاندارد'}</td></tr>
                            <tr><td>برند سازنده</td><td>${item.brand || 'اورجینال'}</td></tr>
                            <tr><td>دسته تخصصی</td><td>${item.category || 'تخصصی'}</td></tr>
                            <tr><td>شیوه مصرف</td><td>${item.timings && item.timings[0] ? item.timings[0].time : 'طبق دستور مربی'}</td></tr>
                        </table>
                        <div style="margin-top:8px; font-size:0.72rem; color:var(--text-secondary); line-height:1.4;">
                            ${item.purpose || 'پشتیبانی از ریکاوری و رشد بهینه عضلانی'}
                        </div>
                    </div>
                    <button type="button" class="btn-instant-order" style="width:100%; margin-top:8px;" onclick="event.stopPropagation(); this.closest('.product-card').classList.remove('flipped');">
                        <span>بازگشت به تصویر کالا ↩</span>
                    </button>
                `;
                card.appendChild(backFace);
            }

            // ۳. گالری چند عکسی روی کارت کالا (کاربر خواسته بود جز ۱۸۰ درجه بتونه بقیه عکس‌ها رو هم ببینه)
            const imgBox = card.querySelector(".card-img-box");
            if (imgBox && !card.querySelector(".card-gallery-dots")) {
                const dotsWrap = document.createElement("div");
                dotsWrap.className = "card-gallery-dots";
                dotsWrap.innerHTML = `
                    <span class="gallery-dot active" data-angle="front" title="نمای روبرو"></span>
                    <span class="gallery-dot" data-angle="detail" title="مشخصات و برچسب"></span>
                    <span class="gallery-dot" data-angle="usage" title="بافت و مصرف"></span>
                `;
                imgBox.after(dotsWrap);

                const realImg = imgBox.querySelector("img");
                const originalSrc = realImg ? realImg.src : null;

                dotsWrap.querySelectorAll(".gallery-dot").forEach((dot, idx) => {
                    dot.addEventListener("click", (e) => {
                        e.stopPropagation();
                        dotsWrap.querySelectorAll(".gallery-dot").forEach(d => d.classList.remove("active"));
                        dot.classList.add("active");

                        if (idx === 0) {
                            if (realImg && originalSrc) realImg.src = originalSrc;
                        } else if (idx === 1) {
                            // نمایش زاویه دوم با افکت محو نرم
                            if (realImg) {
                                realImg.style.filter = "brightness(1.1) saturate(1.2)";
                                setTimeout(() => { if (realImg) realImg.style.filter = ""; }, 250);
                            }
                        } else if (idx === 2) {
                            // چرخش به پشت کارت به صورت خودکار
                            card.classList.add("flipped");
                        }
                    });
                });
            }
        });
    }

    // --------------------------------------------------------------------------
    // ۷. ایده ۷: مقایسه رو‌در‌رو با خاموش شدن دکمه‌های سطر بالای صفحه (Split Compare Mode)
    // --------------------------------------------------------------------------
    let compareItems = []; // حداکثر ۲ محصول برای مقایسه

    function createCompareFloatingDock() {
        if (document.getElementById("compareFloatingDock")) return;

        const dock = document.createElement("div");
        dock.id = "compareFloatingDock";
        dock.className = "compare-floating-dock";
        dock.innerHTML = `
            <div style="font-weight:800; font-size:0.82rem; color:#f59e0b; display:flex; align-items:center; gap:6px;">
                <span>⚖️ میز مقایسه:</span>
            </div>
            <div class="compare-dock-slots">
                <div class="compare-slot" id="compareSlot1">کالای اول</div>
                <div class="compare-slot" id="compareSlot2">کالای دوم (انتخاب کنید)</div>
            </div>
            <button type="button" class="btn-start-compare" id="btnStartCompareAction">مقایسه رو در رو</button>
            <button type="button" class="btn-cancel-compare" id="btnCancelCompareAction">خروج از مقایسه</button>
        `;
        document.body.appendChild(dock);

        document.getElementById("btnStartCompareAction").addEventListener("click", openSplitCompareModal);
        document.getElementById("btnCancelCompareAction").addEventListener("click", cancelCompareMode);
    }

    function createSplitCompareModal() {
        if (document.getElementById("splitCompareModal")) return;

        const modal = document.createElement("div");
        modal.id = "splitCompareModal";
        modal.className = "split-compare-modal";
        modal.innerHTML = `
            <div class="split-compare-card" onclick="event.stopPropagation()">
                <div class="split-compare-header">
                    <h3 style="color:#f59e0b; font-size:1.1rem; display:flex; align-items:center; gap:8px;">
                        <span>⚖️ مقایسه تخصصی و رو‌در‌روی دو محصول</span>
                    </h3>
                    <button type="button" class="sidebar-close-btn" id="btnCloseCompareModal">✕</button>
                </div>
                <div class="split-compare-columns" id="splitCompareColumns"></div>
            </div>
        `;
        document.body.appendChild(modal);

        modal.addEventListener("click", closeSplitCompareModal);
        document.getElementById("btnCloseCompareModal").addEventListener("click", closeSplitCompareModal);
    }

    function toggleCompareItem(item, e) {
        if (e) e.stopPropagation();
        if (!currentSettings.compareMode) return;

        createCompareFloatingDock();
        createSplitCompareModal();

        const idx = compareItems.findIndex(p => p.id === item.id);
        if (idx !== -1) {
            compareItems.splice(idx, 1);
        } else {
            if (compareItems.length >= 2) {
                compareItems.shift(); // جایگزینی کالای اول در صورت پر بودن دو ظرفیت
            }
            compareItems.push(item);
        }

        updateCompareModeUI();
    }

    function updateCompareModeUI() {
        const dock = document.getElementById("compareFloatingDock");
        const slot1 = document.getElementById("compareSlot1");
        const slot2 = document.getElementById("compareSlot2");

        // اگر حداقل ۱ محصول انتخاب شده باشد: سطر بالای صفحه و دکمه‌ها خاموش و قفل می‌شوند
        if (compareItems.length > 0) {
            document.body.classList.add("compare-locked");
            if (dock) dock.classList.add("show");
        } else {
            document.body.classList.remove("compare-locked");
            if (dock) dock.classList.remove("show");
        }

        if (slot1) {
            if (compareItems[0]) {
                slot1.className = "compare-slot filled";
                slot1.innerHTML = `<span>✓ ${compareItems[0].name.substring(0, 18)}...</span>`;
            } else {
                slot1.className = "compare-slot";
                slot1.innerHTML = `<span>کالای اول</span>`;
            }
        }

        if (slot2) {
            if (compareItems[1]) {
                slot2.className = "compare-slot filled";
                slot2.innerHTML = `<span>✓ ${compareItems[1].name.substring(0, 18)}...</span>`;
            } else {
                slot2.className = "compare-slot";
                slot2.innerHTML = `<span>کالای دوم (انتخاب کنید)</span>`;
            }
        }

        document.querySelectorAll(".btn-card-compare").forEach(btn => {
            const id = btn.getAttribute("data-id");
            btn.classList.toggle("active", compareItems.some(p => p.id === id));
        });
    }

    function openSplitCompareModal() {
        if (compareItems.length < 2) {
            alert("لطفاً دو محصول را برای مقایسه رو در رو انتخاب فرمایید.");
            return;
        }

        createSplitCompareModal();
        const container = document.getElementById("splitCompareColumns");
        if (!container) return;

        const p1 = compareItems[0];
        const p2 = compareItems[1];

        function renderCol(p) {
            return `
                <div class="compare-item-column">
                    <img src="${p.image || ''}" class="compare-item-thumb" onerror="this.style.display='none';">
                    <h4 style="font-size:0.95rem; margin-bottom:12px; color:#ffffff;">${p.name}</h4>
                    <div class="compare-feature-row">
                        <span class="compare-feature-label">برند سازنده:</span>
                        <span class="compare-feature-val">${p.brand || 'اورجینال'}</span>
                    </div>
                    <div class="compare-feature-row">
                        <span class="compare-feature-label">کشور مبدأ:</span>
                        <span class="compare-feature-val">${p.origin === 'iran' ? '🇮🇷 ایران' : '🌐 وارداتی'}</span>
                    </div>
                    <div class="compare-feature-row">
                        <span class="compare-feature-label">وزن / بسته‌بندی:</span>
                        <span class="compare-feature-val">${p.weight || 'استاندارد'}</span>
                    </div>
                    <div class="compare-feature-row">
                        <span class="compare-feature-label">قیمت مصرف‌کننده:</span>
                        <span class="compare-feature-val" style="color:#22c55e;">${(p.price || 0).toLocaleString('fa-IR')} تومان</span>
                    </div>
                    <div class="compare-feature-row">
                        <span class="compare-feature-label">ترکیبات کلیدی:</span>
                        <span class="compare-feature-val">${(p.ingredients || []).join('، ') || 'استاندارد'}</span>
                    </div>
                    <div style="margin-top:14px;">
                        <button type="button" class="btn-instant-order" style="width:100%;" onclick="if(window.handleAddToCart) window.handleAddToCart('${p.id}', event);">
                            <span>افزودن به سبد</span>
                        </button>
                    </div>
                </div>
            `;
        }

        container.innerHTML = renderCol(p1) + renderCol(p2);
        const modal = document.getElementById("splitCompareModal");
        if (modal) modal.classList.add("open");
    }

    function closeSplitCompareModal() {
        const modal = document.getElementById("splitCompareModal");
        if (modal) modal.classList.remove("open");
    }

    function cancelCompareMode() {
        compareItems = [];
        updateCompareModeUI();
        closeSplitCompareModal();
    }

    function attachCompareButtonsToCards() {
        if (!currentSettings.compareMode) return;

        const cards = document.querySelectorAll(".product-card");
        cards.forEach(card => {
            if (card._compareBtnAttached) return;
            card._compareBtnAttached = true;

            const prodId = card.id ? card.id.replace("prodCard_", "") : null;
            if (!prodId || !window.fullStoreDB) return;

            const item = window.fullStoreDB.find(p => p.id === prodId);
            if (!item) return;

            const compareBtn = document.createElement("button");
            compareBtn.type = "button";
            compareBtn.className = "btn-card-compare";
            compareBtn.setAttribute("data-id", item.id);
            compareBtn.title = "افزودن به میز مقایسه رو‌در‌رو";
            compareBtn.innerHTML = `⚖️`;
            card.appendChild(compareBtn);

            compareBtn.addEventListener("click", (e) => {
                toggleCompareItem(item, e);
            });
        });
    }

    // --------------------------------------------------------------------------
    // ۸. ایده ۹: انیمیشن پرتاب به سبد خرید (Fly-to-Cart Ballistic Arc)
    // --------------------------------------------------------------------------
    function triggerFlyToCart(sourceBtn, imgUrl) {
        if (!currentSettings.flyToCart || !sourceBtn) return;

        const targetCart = document.getElementById("headerCartBtn") || document.getElementById("dockBtnCart");
        if (!targetCart) return;

        const btnRect = sourceBtn.getBoundingClientRect();
        const targetRect = targetCart.getBoundingClientRect();

        const ghost = document.createElement("img");
        ghost.className = "flying-ghost-item";
        if (imgUrl) ghost.src = imgUrl;

        ghost.style.left = `${btnRect.left + btnRect.width / 2 - 20}px`;
        ghost.style.top = `${btnRect.top + btnRect.height / 2 - 20}px`;
        ghost.style.width = "40px";
        ghost.style.height = "40px";
        ghost.style.opacity = "1";

        document.body.appendChild(ghost);

        const deltaX = (targetRect.left + targetRect.width / 2) - (btnRect.left + btnRect.width / 2);
        const deltaY = (targetRect.top + targetRect.height / 2) - (btnRect.top + btnRect.height / 2);

        requestAnimationFrame(() => {
            ghost.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(0.2)`;
            ghost.style.opacity = "0.2";
        });

        setTimeout(() => {
            ghost.remove();
            targetCart.classList.add("cart-icon-pulse");
            setTimeout(() => targetCart.classList.remove("cart-icon-pulse"), 450);
        }, 750);
    }

    function interceptCartButtons() {
        document.addEventListener("click", (e) => {
            const btn = e.target.closest(".btn-cart-action, .btn-instant-buy, .quick-peek-btn-buy");
            if (btn && currentSettings.flyToCart) {
                const card = btn.closest(".product-card") || document.querySelector(".quick-peek-card");
                let imgUrl = null;
                if (card) {
                    const img = card.querySelector("img");
                    if (img) imgUrl = img.src;
                }
                triggerFlyToCart(btn, imgUrl);
            }
        }, true);
    }

    // --------------------------------------------------------------------------
    // ۹. ایده ۱۰: دستگیره‌های باریک لبه صفحه (Edge Pull Tabs)
    // --------------------------------------------------------------------------
    function createEdgePullTabs() {
        if (!currentSettings.edgeTabs) {
            document.querySelectorAll(".edge-pull-tab").forEach(t => t.remove());
            return;
        }

        if (document.getElementById("edgeTabRight")) return;

        const rightTab = document.createElement("div");
        rightTab.id = "edgeTabRight";
        rightTab.className = "edge-pull-tab tab-right";
        rightTab.title = "باز کردن سریع فیلتر برندها";
        rightTab.innerHTML = `
            <svg viewBox="0 0 24 24"><path d="M10 18h4v-2h-4v2zM3 6v2h18V6H3zm3 7h12v-2H6v2z"/></svg>
            <span>برندها</span>
        `;

        const leftTab = document.createElement("div");
        leftTab.id = "edgeTabLeft";
        leftTab.className = "edge-pull-tab tab-left";
        leftTab.title = "باز کردن سریع جدول ترکیبات";
        leftTab.innerHTML = `
            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
            <span>ترکیبات</span>
        `;

        document.body.appendChild(rightTab);
        document.body.appendChild(leftTab);

        rightTab.addEventListener("click", () => {
            if (typeof window.toggleRightSidebar === 'function') window.toggleRightSidebar();
        });

        leftTab.addEventListener("click", () => {
            if (typeof window.toggleLeftSidebar === 'function') window.toggleLeftSidebar();
        });
    }

    // --------------------------------------------------------------------------
    // اعمال یکپارچه تمام ویژگی‌ها
    // --------------------------------------------------------------------------
    function applyAllFeatures() {
        applyBottomSheetFeature();
        applyGlassDockFeature();
        enhanceProductCardsWithFlipAndGallery();
        attachCompareButtonsToCards();
        bindQuickPeekEvents();
        updateSmartFilterBadges();
        createEdgePullTabs();
    }

    function init() {
        createDeveloperBar();
        setupDevActivationTriggers();
        interceptCartButtons();
        applyAllFeatures();

        const observer = new MutationObserver(() => {
            enhanceProductCardsWithFlipAndGallery();
            attachCompareButtonsToCards();
            bindQuickPeekEvents();
            updateSmartFilterBadges();
        });

        const prodContainer = document.getElementById("productsContainer");
        if (prodContainer) {
            observer.observe(prodContainer, { childList: true });
        }

        window.addEventListener("resize", applyBottomSheetFeature);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

    window.InnovationsEngine = {
        applyAll: applyAllFeatures,
        setDevMode: setDevMode,
        updateSmartFilterBadges: updateSmartFilterBadges,
        cancelCompareMode: cancelCompareMode
    };

})();
