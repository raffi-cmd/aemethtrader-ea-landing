import re, sys, io, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read original head css
with open('index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

head_css = orig[:orig.find('</head>')] + '''  <style>
    .faq-answer { display: none; }
    .faq-answer.open { display: block; animation: faqFadeIn 0.25s ease-out; }
    @keyframes faqFadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }
    .faq-chevron { transition: transform 0.25s ease; display: inline-block; }
    .faq-chevron.rotate { transform: rotate(180deg); }
  </style>
</head>
<body class="antialiased selection:bg-white selection:text-black">
'''

MAYAR = 'https://mayar.id/aemethtrader'
GUMROAD = 'https://aemethtrader.gumroad.com'
TG_BASE = 'https://t.me/aemethtrader?text=Halo%20AEMETH%20TRADER%2C%20saya%20mau%20beli%20'

def pay_buttons(mayar_url, gumroad_url, tg_item):
    return f'''      <div class="mt-5 grid grid-cols-1 gap-2 text-[11px]">
        <a href="{mayar_url}" target="_blank" class="flex items-center justify-center gap-2 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold tracking-wide transition-all shadow-md hover:scale-[1.01]"><span>🏦</span><span data-i18n="btn_pay_qris">QRIS / BANK TRANSFER</span></a>
        <a href="{gumroad_url}" target="_blank" class="flex items-center justify-center gap-2 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold tracking-wide transition-all shadow-md hover:scale-[1.01]"><span>💳</span><span data-i18n="btn_pay_global">PAYPAL / CARD / CRYPTO</span></a>
        <a href="{TG_BASE}{tg_item}" target="_blank" class="flex items-center justify-center gap-2 py-3 rounded-xl bg-zinc-700 hover:bg-zinc-600 text-white font-bold tracking-wide transition-all shadow-md hover:scale-[1.01]"><span>📱</span><span data-i18n="btn_pay_tg">P2P CRYPTO (USDT)</span></a>
      </div>'''

# 1. HEADER & TOP BANNER
nav_html = '''<!-- NAV -->
<header class="w-full pt-4 pb-3 px-4 sm:px-8 max-w-7xl mx-auto flex items-center justify-between z-40 sticky top-0 bg-bgDark/95 backdrop-blur-md border-b border-zinc-800/80">
  <a href="#" class="flex items-center space-x-2.5 group shrink-0">
    <span class="font-serif text-2xl font-light tracking-tighter text-white">AT</span>
    <div class="flex flex-col">
      <span class="text-xs font-mono font-bold tracking-[0.25em] uppercase text-white">AEMETH <span class="text-emerald-400">TRADER</span></span>
      <span class="text-[8px] font-mono tracking-[0.3em] uppercase text-zinc-500" data-i18n="nav_sub_brand">SYSTEMATIC MT5 LAB</span>
    </div>
  </a>
  <nav class="hidden xl:flex items-center space-x-5 text-xs font-mono font-semibold uppercase tracking-wider text-zinc-400">
    <a href="#performance-snapshot" class="hover:text-emerald-400 transition-colors" data-i18n="nav_perf">PERFORMANCE</a>
    <a href="#why-aemeth" class="hover:text-white transition-colors" data-i18n="nav_why">WHY AEMETH?</a>
    <a href="#paket-bundle" class="hover:text-amber-400 transition-colors">🎁 <span data-i18n="nav_bundle">PAKET BUNDLE</span></a>
    <a href="#katalog-ea" class="hover:text-emerald-400 transition-colors">🤖 <span data-i18n="nav_ea">EA SATUAN</span></a>
    <a href="#katalog-indikator" class="hover:text-purple-400 transition-colors">📊 <span data-i18n="nav_ind">INDIKATOR</span></a>
    <a href="#package-includes" class="hover:text-zinc-200 transition-colors" data-i18n="nav_inc">INCLUSIONS</a>
    <a href="#faq" class="hover:text-amber-400 transition-colors">❓ <span data-i18n="nav_faq">FAQ</span></a>
  </nav>
  <div class="flex items-center space-x-2.5 shrink-0">
    <!-- Status badge -->
    <div class="hidden sm:inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[10px] font-mono text-emerald-400">
      <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
      <span data-i18n="nav_status">Status EA: Active &amp; Verified</span>
    </div>
    <!-- Language Toggle (Fixed prominent button) -->
    <div class="flex items-center p-0.5 bg-zinc-900 border border-zinc-700/80 rounded-full text-xs font-mono shadow-sm">
      <button id="lang-id-btn" onclick="setLanguage('id')" type="button" class="cursor-pointer px-3 py-1 rounded-full text-xs font-bold transition-all bg-white text-black shadow">ID</button>
      <button id="lang-en-btn" onclick="setLanguage('en')" type="button" class="cursor-pointer px-3 py-1 rounded-full text-xs font-medium text-zinc-400 hover:text-white transition-all">EN</button>
    </div>
    <a href="#paket-bundle" class="inline-flex items-center px-3.5 sm:px-4 py-1.5 sm:py-2 bg-white text-black font-semibold text-xs rounded-full hover:bg-zinc-200 transition-all group shrink-0">
      <span data-i18n="nav_catalog">KATALOG EA</span> <span class="ml-1 group-hover:translate-x-0.5 transition-transform">↗</span>
    </a>
  </div>
</header>

<main class="max-w-7xl mx-auto px-4 sm:px-12 pb-24">

<!-- TRUST BOOSTER BANNER -->
<div class="mt-4 p-3.5 bg-gradient-to-r from-emerald-950/40 via-zinc-900 to-blue-950/40 border border-emerald-500/30 rounded-2xl flex flex-col sm:flex-row items-center justify-between text-xs font-mono gap-2 text-center sm:text-left">
  <div class="flex items-center space-x-2.5 text-zinc-300">
    <span class="px-2 py-0.5 rounded bg-emerald-500 text-slate-950 font-bold text-[10px] uppercase" data-i18n="top_vip_badge">VIP SERVICE</span>
    <span data-i18n="top_service">Gratis Panduan &amp; Bantuan Pasang via AnyDesk / TeamViewer &bull; Garansi File .EX5 Terkirim Instan</span>
  </div>
  <a href="https://t.me/aemethtrader" target="_blank" rel="noopener noreferrer" class="text-emerald-400 hover:text-emerald-300 font-bold shrink-0 flex items-center space-x-1">
    <span data-i18n="top_tele">KONSULTASI TELEGRAM</span>
    <span>↗</span>
  </a>
</div>
'''

# 2. HERO
hero_html = '''<!-- HERO -->
<section class="relative pt-8 pb-14 hero-spotlight">
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
    <div class="lg:col-span-7 z-10">
      <div class="inline-flex items-center space-x-2 text-[11px] font-mono tracking-[0.25em] text-zinc-400 uppercase mb-4 bg-zinc-900/80 px-3.5 py-1 rounded-full border border-zinc-800">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span data-i18n="hero_kicker">SYSTEMATIC ALGORITHMIC TRADING TOOLS</span>
      </div>
      <h1 class="hero-giant-text text-6xl sm:text-8xl lg:text-9xl font-bold text-white uppercase mb-6" data-i18n="hero_title">QUANTUM<br/>TRADER</h1>
      <p class="text-zinc-400 text-sm sm:text-base leading-relaxed max-w-xl mb-8 font-light" data-i18n="hero_desc">
        Sistem trading kuantitatif MT5 berbasis aturan terukur (rule-based). Menggabungkan algoritma MQL5 berlatensi rendah, manajemen posisi terkontrol, dan pengujian historis transparan.
      </p>
      <div class="flex flex-wrap gap-3 mb-6">
        <a href="#paket-bundle" class="inline-flex items-center px-6 sm:px-7 py-3.5 bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-black text-xs uppercase tracking-wider rounded-xl hover:from-amber-400 hover:to-amber-500 transition-all shadow-glow-amber group">
          <span>🎁</span><span class="ml-1.5" data-i18n="hero_btn_bundle">PAKET BUNDLE</span><span class="ml-2 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform">↗</span>
        </a>
        <a href="#katalog-ea" class="inline-flex items-center px-6 sm:px-7 py-3.5 bg-emerald-500 text-slate-950 font-bold text-xs uppercase tracking-wider rounded-xl hover:bg-emerald-400 transition-all shadow-glow-emerald group">
          <span>🤖</span><span class="ml-1.5" data-i18n="hero_btn_ea">EA SATUAN</span><span class="ml-2 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform">↗</span>
        </a>
        <a href="#katalog-indikator" class="inline-flex items-center px-6 sm:px-7 py-3.5 bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs uppercase tracking-wider rounded-xl transition-all shadow-glow-purple group">
          <span>📊</span><span class="ml-1.5" data-i18n="hero_btn_ind">INDIKATOR PRO</span><span class="ml-2 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform">↗</span>
        </a>
      </div>
      <!-- Global Payment badges -->
      <div class="flex items-center space-x-3 text-xs font-mono text-zinc-400 pt-2">
        <span class="text-zinc-500 text-[11px]" data-i18n="hero_pay_label">METODE PEMBAYARAN:</span>
        <span class="px-2 py-0.5 bg-zinc-900 border border-zinc-800 rounded text-emerald-400 font-bold">QRIS</span>
        <span class="px-2 py-0.5 bg-zinc-900 border border-zinc-800 rounded text-blue-400 font-bold">PayPal</span>
        <span class="px-2 py-0.5 bg-zinc-900 border border-zinc-800 rounded text-amber-400 font-bold">P2P Crypto (USDT)</span>
      </div>
    </div>
    <div class="lg:col-span-5 flex justify-center lg:justify-end">
      <!-- HERO RIGHT CARD -->
      <div class="relative w-full max-w-md aspect-[4/5] rounded-3xl overflow-hidden bg-gradient-to-t from-black via-cardDark to-zinc-900 border border-zinc-800/80 p-6 flex flex-col justify-between shadow-2xl">
        <div class="flex justify-between items-start">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
            <span class="text-zinc-400 font-mono text-[10px] uppercase tracking-widest">// ALGO_CORE_v4.0 ACTIVE</span>
          </div>
          <span class="text-emerald-400 text-xl font-mono">✦</span>
        </div>
        <!-- MT5 Mockup -->
        <div class="my-auto py-3">
          <div class="rounded-2xl border border-zinc-800/80 bg-zinc-950 p-3.5 font-mono text-xs shadow-inner">
            <div class="flex justify-between items-center border-b border-zinc-800 pb-2 mb-2.5 text-[10px] text-zinc-500">
              <span class="text-emerald-400 font-bold">XAUUSD, M15</span>
              <span>EXNESS PRO SERVER</span>
            </div>
            <svg class="w-full h-24 my-1" viewBox="0 0 240 70" fill="none">
              <line x1="0" y1="20" x2="240" y2="20" stroke="#1f2937" stroke-dasharray="2 2" stroke-width="0.8"/>
              <line x1="0" y1="45" x2="240" y2="45" stroke="#1f2937" stroke-dasharray="2 2" stroke-width="0.8"/>
              <path d="M 10 58 Q 60 52 110 35 T 180 18 T 230 10" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="3 3"/>
              <line x1="25" y1="40" x2="25" y2="58" stroke="#f43f5e" stroke-width="1"/>
              <rect x="22" y="44" width="6" height="10" fill="#f43f5e"/>
              <line x1="50" y1="36" x2="50" y2="55" stroke="#10b981" stroke-width="1"/>
              <rect x="47" y="40" width="6" height="12" fill="#10b981"/>
              <line x1="75" y1="25" x2="75" y2="48" stroke="#10b981" stroke-width="1"/>
              <rect x="72" y="30" width="6" height="14" fill="#10b981"/>
              <line x1="100" y1="28" x2="100" y2="42" stroke="#f43f5e" stroke-width="1"/>
              <rect x="97" y="31" width="6" height="7" fill="#f43f5e"/>
              <line x1="125" y1="18" x2="125" y2="38" stroke="#10b981" stroke-width="1"/>
              <rect x="122" y="22" width="6" height="14" fill="#10b981"/>
              <polygon points="125,48 120,54 130,54" fill="#10b981"/>
              <text x="133" y="53" fill="#10b981" font-size="7" font-family="monospace" font-weight="bold">BUY 0.50</text>
              <line x1="150" y1="12" x2="150" y2="30" stroke="#10b981" stroke-width="1"/>
              <rect x="147" y="15" width="6" height="12" fill="#10b981"/>
              <line x1="175" y1="6" x2="175" y2="24" stroke="#10b981" stroke-width="1"/>
              <rect x="172" y="8" width="6" height="12" fill="#10b981"/>
              <line x1="110" y1="10" x2="230" y2="10" stroke="#10b981" stroke-dasharray="2 2" stroke-width="1"/>
              <text x="180" y="8" fill="#10b981" font-size="7" font-family="monospace">TP HIT +$840.00</text>
            </svg>
            <div class="flex justify-between items-center text-[10px] text-zinc-400 pt-1 border-t border-zinc-800/80">
              <span class="text-zinc-500" data-i18n="hero_mockup_routing">Order Routing: MT5 Native C++</span>
              <span class="text-emerald-400 font-bold">+342.8% Total Net</span>
            </div>
          </div>
        </div>
        <div class="bg-zinc-950/80 backdrop-blur-md border border-zinc-800 rounded-2xl p-4 flex items-center justify-between">
          <div>
            <span class="block text-[9px] font-mono text-zinc-500 uppercase tracking-widest" data-i18n="hero_prop_tag">PROP FIRM COMPATIBLE</span>
            <span class="text-xs font-bold text-white uppercase tracking-wider" data-i18n="hero_prop_title">RISK BOUNDED MODEL</span>
          </div>
          <a href="#paket-bundle" class="w-9 h-9 rounded-full bg-white text-black flex items-center justify-center hover:scale-110 transition-transform font-bold text-sm">↗</a>
        </div>
      </div>
    </div>
  </div>
</section>
'''

# 3. PERFORMANCE SNAPSHOT
perf_html = '''<!-- PERFORMANCE SNAPSHOT -->
<section id="performance-snapshot" class="my-10">
  <div class="bg-cardDark rounded-3xl border border-zinc-800/90 p-6 sm:p-8 shadow-xl">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-zinc-800/80 pb-5 mb-6">
      <div>
        <span class="text-[11px] font-mono uppercase tracking-[0.25em] text-emerald-400 font-bold block" data-i18n="perf_kicker">VERIFIED AUDIT BENCHMARK</span>
        <h3 class="text-xl sm:text-2xl font-bold text-white uppercase tracking-tight" data-i18n="perf_title">PERFORMANCE SNAPSHOT</h3>
      </div>
      <div class="mt-2 sm:mt-0 flex items-center space-x-2">
        <span class="text-xs font-mono text-zinc-300 px-3 py-1 bg-zinc-900 rounded-full border border-zinc-800" data-i18n="perf_pair">XAUUSD &middot; MT5 &middot; Backtest</span>
      </div>
    </div>
    <!-- 3 Core Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center border-b border-zinc-800/80 pb-6">
      <div class="p-4 bg-zinc-950/60 rounded-2xl border border-zinc-800/60">
        <div class="text-zinc-500 text-xs font-mono mb-1">// PROFIT FACTOR</div>
        <div class="text-4xl sm:text-5xl font-bold text-white tracking-tight">5.91</div>
        <div class="text-[10px] font-mono uppercase tracking-[0.2em] text-zinc-400 mt-1" data-i18n="stat_pf">PROFIT FACTOR</div>
      </div>
      <div class="p-4 bg-zinc-950/60 rounded-2xl border border-zinc-800/60">
        <div class="text-zinc-500 text-xs font-mono mb-1">// WIN RATE</div>
        <div class="text-4xl sm:text-5xl font-bold text-emerald-400 tracking-tight">94.8%</div>
        <div class="text-[10px] font-mono uppercase tracking-[0.2em] text-zinc-400 mt-1" data-i18n="stat_win">WIN RATE</div>
      </div>
      <div class="p-4 bg-zinc-950/60 rounded-2xl border border-zinc-800/60">
        <div class="text-zinc-500 text-xs font-mono mb-1">// MAX DRAWDOWN</div>
        <div class="text-4xl sm:text-5xl font-bold text-blue-400 tracking-tight">4.02%</div>
        <div class="text-[10px] font-mono uppercase tracking-[0.2em] text-zinc-400 mt-1" data-i18n="stat_dd">MAX DRAWDOWN</div>
      </div>
    </div>
    <!-- Context & Disclaimer -->
    <div class="pt-4 flex flex-col sm:flex-row items-start sm:items-center justify-between text-[11px] font-mono text-zinc-400 space-y-2 sm:space-y-0">
      <div class="flex items-start sm:items-center space-x-2">
        <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 shrink-0 mt-1 sm:mt-0"></span>
        <span data-i18n="perf_context"><strong>Results based on:</strong> AEMETH Quantum Neural Master v4.0, Jan 2024&ndash;Dec 2025, M15 Timeframe (Exness Pro Server, 99.9% Tick Quality). Past performance does not guarantee future results.</span>
      </div>
      <div class="text-zinc-500 text-[10px] shrink-0" data-i18n="perf_disc">*Simulated historical testing under fixed risk parameters.</div>
    </div>
  </div>
</section>
'''

# 4. WHY AEMETH
why_html = '''<!-- WHY AEMETH -->
<section id="why-aemeth" class="my-16 pt-8 border-t border-zinc-800/80">
  <div class="text-center max-w-2xl mx-auto mb-12">
    <span class="text-xs font-mono uppercase tracking-[0.25em] text-emerald-400 font-bold" data-i18n="why_kicker">SYSTEMATIC ARCHITECTURE</span>
    <h2 class="text-3xl sm:text-4xl font-black text-white uppercase tracking-tight mt-1" data-i18n="why_title">WHY AEMETH TRADER?</h2>
    <p class="text-zinc-400 text-sm mt-2" data-i18n="why_sub">Dibangun dengan filosofi trading sistematis dan manajemen eksposur yang disiplin.</p>
  </div>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
    <div class="bg-cardDark p-5 rounded-2xl border border-zinc-800/90">
      <div class="text-xs font-mono text-emerald-400 font-bold mb-2">01 // LOGIC</div>
      <h3 class="text-sm font-bold text-white uppercase mb-2" data-i18n="w1t">Rule-Based Execution</h3>
      <p class="text-xs text-zinc-400 leading-relaxed font-light" data-i18n="w1d">Menghilangkan keputusan subjektif. Order dieksekusi murni berdasarkan parameter teknis yang terukur.</p>
    </div>
    <div class="bg-cardDark p-5 rounded-2xl border border-zinc-800/90">
      <div class="text-xs font-mono text-blue-400 font-bold mb-2">02 // RISK CONTROL</div>
      <h3 class="text-sm font-bold text-white uppercase mb-2" data-i18n="w2t">Automated Risk Management</h3>
      <p class="text-xs text-zinc-400 leading-relaxed font-light" data-i18n="w2d">Automated risk management designed to reduce excessive exposure. Hard Stop Loss setiap transaksi dan batas drawdown terukur.</p>
    </div>
    <div class="bg-cardDark p-5 rounded-2xl border border-zinc-800/90">
      <div class="text-xs font-mono text-purple-400 font-bold mb-2">03 // SPEED</div>
      <h3 class="text-sm font-bold text-white uppercase mb-2" data-i18n="w3t">MT5 Native C++</h3>
      <p class="text-xs text-zinc-400 leading-relaxed font-light" data-i18n="w3d">Low-latency native execution untuk MetaTrader 5. Efisiensi memori optimal dan kompatibilitas broker ECN modern.</p>
    </div>
    <div class="bg-cardDark p-5 rounded-2xl border border-zinc-800/90">
      <div class="text-xs font-mono text-amber-400 font-bold mb-2">04 // VALUE</div>
      <h3 class="text-sm font-bold text-white uppercase mb-2" data-i18n="w4t">Lifetime License</h3>
      <p class="text-xs text-zinc-400 leading-relaxed font-light" data-i18n="w4d">Satu kali pembelian permanen tanpa biaya langganan bulanan tersembunyi.</p>
    </div>
    <div class="bg-cardDark p-5 rounded-2xl border border-zinc-800/90">
      <div class="text-xs font-mono text-emerald-400 font-bold mb-2">05 // DELIVERY</div>
      <h3 class="text-sm font-bold text-white uppercase mb-2" data-i18n="w5t">Instant Delivery</h3>
      <p class="text-xs text-zinc-400 leading-relaxed font-light" data-i18n="w5d">File .ex5 dan panduan konfigurasi terkirim otomatis dalam 1 detik setelah checkout.</p>
    </div>
  </div>
</section>
'''

# 5. PAKET BUNDLE (With dynamic main/orig/sub price data-i18n tags)
bundle_html = f'''<!-- ========================================== -->
<!-- 1. SECTION: PAKET BUNDLE HEMAT MT5 -->
<!-- ========================================== -->
<section id="paket-bundle" class="my-16 pt-12 border-t border-zinc-800">
  <div class="text-center max-w-3xl mx-auto mb-10">
    <div class="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 font-mono text-xs font-bold uppercase tracking-widest mb-3">
      <span>🎁</span>
      <span data-i18n="bundle_kicker">PENAWARAN HEMAT ALL-IN-ONE</span>
    </div>
    <h2 class="text-3xl sm:text-5xl font-black text-white uppercase tracking-tight" data-i18n="bundle_title">PAKET BUNDLE HEMAT MT5</h2>
    <p class="text-zinc-400 text-sm sm:text-base mt-3 leading-relaxed" data-i18n="bundle_sub">Dapatkan kombinasi lengkap Robot EA otomatis multi-strategi + Indikator Pro non-repaint dengan diskon 50%. Solusi terbaik untuk diversifikasi portofolio dan akun challenge.</p>
  </div>

  <div id="bundle-grid" class="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 items-stretch">

    <!-- BUNDLE 1: Rp 3.000.000 / $199 USD — INSTITUTIONAL FLAGSHIP (ATTENTION MAGNET) -->
    <div class="bundle-card bg-gradient-to-b from-cardDark via-zinc-950 to-emerald-950/40 rounded-3xl border-2 border-emerald-400 shadow-[0_0_60px_-10px_rgba(16,185,129,0.45)] ring-2 ring-emerald-500/40 p-7 sm:p-8 flex flex-col justify-between relative overflow-hidden group scale-[1.01] hover:scale-[1.02] transition-transform">
      <!-- Top floating ribbon -->
      <div class="absolute top-0 right-0 bg-gradient-to-l from-emerald-500 via-teal-400 to-emerald-600 text-black font-mono font-black text-[10px] uppercase tracking-widest px-5 py-2 rounded-bl-2xl shadow-xl flex items-center gap-1.5">
        <span>👑</span>
        <span data-i18n="b1_badge">INSTITUTIONAL FLAGSHIP</span>
      </div>

      <div>
        <!-- Header Pill & Badges -->
        <div class="mb-4 pr-36">
          <div class="flex flex-wrap gap-1.5 mb-2">
            <span class="inline-flex items-center space-x-1 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/50 text-emerald-300 text-xs font-mono font-bold shadow-sm">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              <span data-i18n="b1_hot_tag">⭐ REKOMENDASI TERBAIK UNTUK AKUN BESAR &amp; PROP FIRM</span>
            </span>
            <span class="px-2.5 py-1 rounded-full bg-amber-500/20 border border-amber-500/40 text-amber-300 text-[10px] font-mono font-bold" data-i18n="b1_save_tag">HEMAT RP 3.000.000</span>
          </div>
          <h3 class="text-2xl sm:text-3xl font-black text-white tracking-tight group-hover:text-emerald-400 transition-colors" data-i18n="b1_title">AEMETH MASTER BUNDLE 6 Tools</h3>
          <div class="text-xs font-mono text-zinc-400 mt-1" data-i18n="b1_tools_line">4 Robot EA MT5 + 2 Indikator Pro — Akses Seumur Hidup</div>
        </div>

        <p class="text-zinc-300 text-xs sm:text-sm leading-relaxed font-light" data-i18n="bundle_desc">Loading...</p>

        <!-- Detailed Tool Breakdown -->
        <div class="mt-4 p-4 rounded-2xl bg-zinc-950/80 border border-zinc-800">
          <div class="text-[11px] font-mono font-bold uppercase tracking-wider text-emerald-400 mb-2 flex items-center gap-1.5">
            <span>📦</span>
            <span data-i18n="b1_inc_header">DAFTAR 6 TOOLS YANG DIDAPAT:</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono text-zinc-300">
            <div class="flex items-center gap-2 p-1.5 rounded-lg bg-zinc-900/60 border border-zinc-800/80">
              <span class="text-amber-400 font-bold shrink-0">👑</span>
              <div><strong class="text-white">Neural Master v4.0</strong> <span class="text-[10px] text-zinc-500 block">XAUUSD AI Scalper</span></div>
            </div>
            <div class="flex items-center gap-2 p-1.5 rounded-lg bg-zinc-900/60 border border-zinc-800/80">
              <span class="text-cyan-400 font-bold shrink-0">⚡</span>
              <div><strong class="text-white">HFT Multi v3.2</strong> <span class="text-[10px] text-zinc-500 block">Multi-Pair High-Frequency</span></div>
            </div>
            <div class="flex items-center gap-2 p-1.5 rounded-lg bg-zinc-900/60 border border-zinc-800/80">
              <span class="text-rose-400 font-bold shrink-0">🛡️</span>
              <div><strong class="text-white">Prop Shield v2.1</strong> <span class="text-[10px] text-zinc-500 block">Challenge Risk Armor</span></div>
            </div>
            <div class="flex items-center gap-2 p-1.5 rounded-lg bg-zinc-900/60 border border-zinc-800/80">
              <span class="text-violet-400 font-bold shrink-0">📈</span>
              <div><strong class="text-white">Trend Pulse v2.0</strong> <span class="text-[10px] text-zinc-500 block">Trend Pullback Confluence</span></div>
            </div>
            <div class="flex items-center gap-2 p-1.5 rounded-lg bg-zinc-900/60 border border-zinc-800/80">
              <span class="text-purple-400 font-bold shrink-0">📊</span>
              <div><strong class="text-white">Order Block Hunter</strong> <span class="text-[10px] text-zinc-500 block">SMC Pro Indicator</span></div>
            </div>
            <div class="flex items-center gap-2 p-1.5 rounded-lg bg-zinc-900/60 border border-zinc-800/80">
              <span class="text-emerald-400 font-bold shrink-0">🎯</span>
              <div><strong class="text-white">Arrow Signal Pro</strong> <span class="text-[10px] text-zinc-500 block">0% Non-Repaint Signals</span></div>
            </div>
          </div>
        </div>

        <!-- VIP Special Privileges Box -->
        <div class="my-4 p-4 rounded-2xl bg-gradient-to-r from-emerald-950/80 via-zinc-900 to-teal-950/80 border border-emerald-500/50 text-xs font-mono shadow-inner">
          <div class="flex items-center justify-between text-emerald-400 font-bold mb-2 text-[11px]">
            <span class="flex items-center gap-1.5">
              <span>💎</span>
              <span data-i18n="b1_vip_bonus_title">EXCLUSIVE VIP PRIVILEGES:</span>
            </span>
            <span class="bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded text-[10px]" data-i18n="b1_free_tag">GRATIS</span>
          </div>
          <ul class="space-y-1.5 text-zinc-300 text-[11px]">
            <li class="flex items-center gap-2">
              <span class="text-emerald-400 font-bold shrink-0">✓</span>
              <span data-i18n="b1_bonus_1">1-on-1 Remote Setup via AnyDesk / TeamViewer Prioritas</span>
            </li>
            <li class="flex items-center gap-2">
              <span class="text-emerald-400 font-bold shrink-0">✓</span>
              <span data-i18n="b1_bonus_2">Setfile Khusus Low Drawdown untuk Challenge Prop Firm</span>
            </li>
            <li class="flex items-center gap-2">
              <span class="text-emerald-400 font-bold shrink-0">✓</span>
              <span data-i18n="b1_bonus_3">Akses Komunitas VIP Telegram &amp; Update Algoritma Seumur Hidup</span>
            </li>
          </ul>
        </div>

        <!-- Urgency Alert -->
        <div class="p-2.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-[11px] font-mono text-emerald-300 flex items-center justify-between">
          <span class="flex items-center gap-1.5"><span>⚡</span><span data-i18n="b1_urgency">HANYA TERSISA 5 LISENSI DENGAN BANTUAN ANYDESK SETUP</span></span>
          <span class="text-[10px] text-zinc-400 font-bold">LIMITED</span>
        </div>
      </div>

      <div>
        <div class="mt-5 pt-4 border-t border-zinc-800/80">
          <div class="flex items-center space-x-2 mb-1 text-xs">
            <span class="text-zinc-500 line-through font-mono" data-i18n="price_orig_b1">Rp 6.000.000</span>
            <span class="text-emerald-400 font-bold font-mono text-[10px] bg-emerald-950/80 px-2.5 py-0.5 rounded-full border border-emerald-500/50" data-i18n="bundle_discount_badge">50% DISKON VIP</span>
          </div>
          <div class="text-4xl sm:text-5xl font-black font-mono text-emerald-400 tracking-tight" data-i18n="price_main_b1">Rp 3.000.000</div>
          <div class="text-[11px] font-mono text-zinc-400 mt-0.5" data-i18n="price_sub_b1">atau <strong>$199 USD</strong> &middot; Akses Seumur Hidup (6 Alat)</div>
        </div>
{pay_buttons(MAYAR+'/master-bundle', GUMROAD+'/l/master-bundle', 'MASTER%20BUNDLE%206%20Tools')}
      </div>
    </div>

    <!-- BUNDLE 2: Rp 2.500.000 / $165 USD — BEST SELLER (MAXIMUM VALUE) -->
    <div class="bundle-card bg-gradient-to-b from-cardDark via-zinc-950 to-amber-950/40 rounded-3xl border-2 border-amber-400 shadow-[0_0_60px_-10px_rgba(245,158,11,0.45)] ring-2 ring-amber-500/40 p-7 sm:p-8 flex flex-col justify-between hover:border-amber-300 relative overflow-hidden group scale-[1.01] hover:scale-[1.02] transition-transform">
      <!-- Best Seller Top Ribbon -->
      <div class="absolute top-0 right-0 bg-gradient-to-l from-amber-500 via-orange-500 to-amber-600 text-black font-mono font-black text-[10px] uppercase tracking-widest px-5 py-2 rounded-bl-2xl shadow-xl flex items-center gap-1.5">
        <span>🔥</span>
        <span data-i18n="b2_badge">#1 BEST SELLER — 14 TOOLS</span>
      </div>

      <div>
        <!-- Header Pill & Badges -->
        <div class="mb-4 pr-36">
          <div class="flex flex-wrap gap-1.5 mb-2">
            <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-amber-500/20 border border-amber-500/40 text-amber-300 text-xs font-mono font-bold shadow-sm">
              <span class="animate-pulse">🔥</span>
              <span data-i18n="b2_seller_tag">🏆 PALING BANYAK DIPILIH TRADER (14 TOOLS ALL-IN-ONE)</span>
            </span>
            <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-[10px] font-mono font-bold" data-i18n="b2_rate_tag">HANYA RP 178.000 / TOOL!</span>
          </div>
          <h3 class="text-2xl sm:text-3xl font-black text-white tracking-tight group-hover:text-amber-400 transition-colors" data-i18n="b2_title">AEMETH MEGA BUNDLE 14 Tools v2.0</h3>
          <div class="text-xs font-mono text-zinc-400 mt-1" data-i18n="b2_tools_line">10 Robot EA MT5 + 4 Indikator Pro — Akses Seumur Hidup</div>
        </div>

        <p class="text-zinc-300 text-xs sm:text-sm leading-relaxed font-light" data-i18n="bundle2_desc">Loading...</p>

        <!-- Detailed 14 Tools Showcase -->
        <div class="mt-4 p-4 rounded-2xl bg-zinc-950/80 border border-zinc-800">
          <div class="text-[11px] font-mono font-bold uppercase tracking-wider text-amber-400 mb-2 flex items-center gap-1.5">
            <span>📦</span>
            <span data-i18n="b2_inc_header">ARSENAL LENGKAP 14 TOOLS MT5:</span>
          </div>
          <div class="space-y-2 text-xs font-mono">
            <div>
              <span class="text-zinc-500 text-[10px] block mb-1">🤖 10 ROBOT EA MT5 OTOMATIS:</span>
              <div class="flex flex-wrap gap-1.5">
                <span class="px-2 py-0.5 rounded bg-amber-950/70 border border-amber-700/60 text-amber-300 text-[10px]">Neural Master</span>
                <span class="px-2 py-0.5 rounded bg-cyan-950/70 border border-cyan-700/60 text-cyan-300 text-[10px]">HFT Multi</span>
                <span class="px-2 py-0.5 rounded bg-rose-950/70 border border-rose-700/60 text-rose-300 text-[10px]">Prop Shield</span>
                <span class="px-2 py-0.5 rounded bg-violet-950/70 border border-violet-700/60 text-violet-300 text-[10px]">Trend Pulse</span>
                <span class="px-2 py-0.5 rounded bg-yellow-950/70 border border-yellow-700/60 text-yellow-300 text-[10px]">Quantum Scalper</span>
                <span class="px-2 py-0.5 rounded bg-teal-950/70 border border-teal-700/60 text-teal-300 text-[10px]">Micro Cent</span>
                <span class="px-2 py-0.5 rounded bg-lime-950/70 border border-lime-700/60 text-lime-300 text-[10px]">Budget Scalper</span>
                <span class="px-2 py-0.5 rounded bg-zinc-800 border border-zinc-700 text-zinc-300 text-[10px]">Mini Grid</span>
                <span class="px-2 py-0.5 rounded bg-orange-950/70 border border-orange-700/60 text-orange-300 text-[10px]">London Breakout</span>
                <span class="px-2 py-0.5 rounded bg-cyan-950/70 border border-cyan-700/60 text-cyan-300 text-[10px]">Grid Momentum</span>
              </div>
            </div>
            <div class="pt-1.5 border-t border-zinc-800/80">
              <span class="text-zinc-500 text-[10px] block mb-1">📊 4 INDIKATOR PRO NON-REPAINT:</span>
              <div class="flex flex-wrap gap-1.5">
                <span class="px-2 py-0.5 rounded bg-purple-950/70 border border-purple-700/60 text-purple-300 text-[10px]">Order Block SMC</span>
                <span class="px-2 py-0.5 rounded bg-emerald-950/70 border border-emerald-700/60 text-emerald-300 text-[10px]">Arrow Signal Pro</span>
                <span class="px-2 py-0.5 rounded bg-rose-950/70 border border-rose-700/60 text-rose-300 text-[10px]">Supply &amp; Demand</span>
                <span class="px-2 py-0.5 rounded bg-amber-950/70 border border-amber-700/60 text-amber-300 text-[10px]">Divergence Matrix</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Huge Value Calculation Box -->
        <div class="my-4 p-3.5 rounded-2xl bg-amber-950/30 border border-amber-500/40 text-xs font-mono">
          <div class="flex items-center justify-between text-zinc-400 text-[11px] mb-1">
            <span data-i18n="b2_val_calc_lbl">Total Harga Beli Satuan (14 Tools):</span>
            <span class="line-through font-bold text-zinc-500" data-i18n="b2_val_calc_orig">Rp 9.800.000+</span>
          </div>
          <div class="flex items-center justify-between text-amber-300 font-bold text-xs">
            <span data-i18n="b2_val_save_lbl">Penghematan Bersih Anda:</span>
            <span class="text-emerald-400 font-black" data-i18n="b2_val_save_val">+Rp 7.300.000 (Hemat 74%)</span>
          </div>
        </div>

        <!-- Social Proof Badge -->
        <div class="p-2.5 rounded-xl bg-zinc-950/80 border border-zinc-800 text-[11px] font-mono text-zinc-300 flex items-center justify-between">
          <span class="flex items-center gap-1.5"><span>⭐</span><span data-i18n="b2_social_proof">98% TRADER MEMILIH PAKET INI KARENA PALING LENGKAP</span></span>
          <span class="text-[10px] text-amber-400 font-bold">BEST SELLER</span>
        </div>
      </div>

      <div>
        <div class="mt-5 pt-4 border-t border-zinc-800/80">
          <div class="flex items-center space-x-2 mb-1 text-xs">
            <span class="text-zinc-500 line-through font-mono" data-i18n="price_orig_b2">Rp 5.000.000</span>
            <span class="text-amber-400 font-bold font-mono text-[10px] bg-amber-950/80 px-2.5 py-0.5 rounded-full border border-amber-500/50" data-i18n="bundle2_discount_badge">50% DISKON LAUNCH</span>
          </div>
          <div class="text-4xl sm:text-5xl font-black font-mono text-amber-400 tracking-tight" data-i18n="price_main_b2">Rp 2.500.000</div>
          <div class="text-[11px] font-mono text-zinc-400 mt-0.5" data-i18n="price_sub_b2">atau <strong>$165 USD</strong> &middot; Akses Seumur Hidup (14 Alat)</div>
        </div>
{pay_buttons(MAYAR+'/mega-bundle', GUMROAD+'/l/mega-bundle', 'MEGA%20BUNDLE%2014%20Tools')}
      </div>
    </div>

    <!-- BUNDLE 3: Rp 2.000.000 / $130 USD — STARTER BUNDLE -->
    <div class="bundle-card bg-cardDark rounded-3xl border-2 border-sky-500/70 p-7 sm:p-8 flex flex-col justify-between hover:border-sky-400 shadow-glow-sky relative overflow-hidden group">
      <div class="absolute top-0 right-0 bg-gradient-to-l from-sky-600 to-sky-800 text-white font-mono font-bold text-[9px] uppercase tracking-widest px-4 py-1.5 rounded-bl-2xl" data-i18n="b4_badge">⚡ STARTER BUNDLE — 11 TOOLS</div>
      <div>
        <div class="mb-4">
          <span class="inline-block px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-[11px] font-mono font-bold mb-2">⚡ 5 EA + 6 INDIKATOR</span>
          <h3 class="text-xl sm:text-2xl font-black text-white tracking-tight group-hover:text-sky-400 transition-colors" data-i18n="b4_title">AEMETH STARTER BUNDLE 5 EA + 6 Ind</h3>
          <div class="text-xs font-mono text-zinc-400 mt-1" data-i18n="b4_tools_line">5 Robot EA MT5 + 6 Indikator Pro — Akses Seumur Hidup</div>
        </div>
        <p class="text-zinc-400 text-xs sm:text-sm leading-relaxed font-light" data-i18n="bundle4_desc">Loading...</p>
        <div class="mt-5 flex flex-wrap gap-2">
          <span class="px-2.5 py-1 rounded-lg bg-sky-800/60 border border-sky-700/50 text-sky-300 text-[10px] font-mono font-bold">✓ 5 Robot EA MT5</span>
          <span class="px-2.5 py-1 rounded-lg bg-purple-800/60 border border-purple-700/50 text-purple-300 text-[10px] font-mono font-bold">✓ 6 Indikator Pro</span>
          <span class="px-2.5 py-1 rounded-lg bg-emerald-800/60 border border-emerald-700/50 text-emerald-300 text-[10px] font-mono font-bold">✓ Free Setup Guide</span>
          <span class="px-2.5 py-1 rounded-lg bg-blue-800/60 border border-blue-700/50 text-blue-300 text-[10px] font-mono font-bold">✓ Lifetime License</span>
        </div>
      </div>
      <div>
        <div class="mt-6 pt-4 border-t border-zinc-800/80">
          <div class="flex items-center space-x-2 mb-1 text-xs">
            <span class="text-zinc-500 line-through font-mono" data-i18n="price_orig_b4">Rp 4.000.000</span>
            <span class="text-sky-400 font-bold font-mono text-[10px] bg-sky-950/60 px-2 py-0.5 rounded-full border border-sky-800/60" data-i18n="bundle4_discount_badge">50% DISKON</span>
          </div>
          <div class="text-3xl sm:text-4xl font-black font-mono text-sky-400 tracking-tight" data-i18n="price_main_b4">Rp 2.000.000</div>
          <div class="text-[11px] font-mono text-zinc-500 mt-0.5" data-i18n="price_sub_b4">atau <strong>$130 USD</strong> &middot; Akses Seumur Hidup (11 Alat)</div>
        </div>
{pay_buttons(MAYAR+'/starter-bundle', GUMROAD+'/l/starter-bundle', 'STARTER%20BUNDLE%205EA%2B6Ind')}
      </div>
    </div>

    <!-- BUNDLE 4: Rp 1.500.000 / $99 USD — HYBRID SUITE -->
    <div class="bundle-card bg-cardDark rounded-3xl border-2 border-purple-500/70 p-7 sm:p-8 flex flex-col justify-between hover:border-purple-400 shadow-glow-purple relative overflow-hidden group">
      <div class="absolute top-0 right-0 bg-gradient-to-l from-purple-600 to-purple-800 text-white font-mono font-bold text-[9px] uppercase tracking-widest px-4 py-1.5 rounded-bl-2xl" data-i18n="b3_badge">🔥 HYBRID BUNDLE — 11 TOOLS</div>
      <div>
        <div class="mb-4">
          <span class="inline-block px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400 text-[11px] font-mono font-bold mb-2">🔥 3 EA + 8 INDIKATOR</span>
          <h3 class="text-xl sm:text-2xl font-black text-white tracking-tight group-hover:text-purple-400 transition-colors" data-i18n="b3_title">AEMETH HYBRID SUITE 3 EA + 8 Ind</h3>
          <div class="text-xs font-mono text-zinc-400 mt-1" data-i18n="b3_tools_line">3 Robot EA MT5 + 8 Indikator Pro — Akses Seumur Hidup</div>
        </div>
        <p class="text-zinc-400 text-xs sm:text-sm leading-relaxed font-light" data-i18n="bundle3_desc">Loading...</p>
        <div class="mt-5 flex flex-wrap gap-2">
          <span class="px-2.5 py-1 rounded-lg bg-purple-800/60 border border-purple-700/50 text-purple-300 text-[10px] font-mono font-bold">✓ 3 Robot EA MT5</span>
          <span class="px-2.5 py-1 rounded-lg bg-pink-800/60 border border-pink-700/50 text-pink-300 text-[10px] font-mono font-bold">✓ 8 Indikator Pro</span>
          <span class="px-2.5 py-1 rounded-lg bg-emerald-800/60 border border-emerald-700/50 text-emerald-300 text-[10px] font-mono font-bold">✓ Free Setup Guide</span>
          <span class="px-2.5 py-1 rounded-lg bg-blue-800/60 border border-blue-700/50 text-blue-300 text-[10px] font-mono font-bold">✓ Lifetime License</span>
        </div>
      </div>
      <div>
        <div class="mt-6 pt-4 border-t border-zinc-800/80">
          <div class="flex items-center space-x-2 mb-1 text-xs">
            <span class="text-zinc-500 line-through font-mono" data-i18n="price_orig_b3">Rp 3.000.000</span>
            <span class="text-purple-400 font-bold font-mono text-[10px] bg-purple-950/60 px-2 py-0.5 rounded-full border border-purple-800/60" data-i18n="bundle3_discount_badge">50% DISKON</span>
          </div>
          <div class="text-3xl sm:text-4xl font-black font-mono text-purple-400 tracking-tight" data-i18n="price_main_b3">Rp 1.500.000</div>
          <div class="text-[11px] font-mono text-zinc-500 mt-0.5" data-i18n="price_sub_b3">atau <strong>$99 USD</strong> &middot; Akses Seumur Hidup (11 Alat)</div>
        </div>
{pay_buttons(MAYAR+'/hybrid-bundle', GUMROAD+'/l/hybrid-bundle', 'HYBRID%20BUNDLE%203EA%2B8Ind')}
      </div>
    </div>

  </div>
</section>
'''

# 6. STANDALONE EA (14 EA Cards with dynamic p{i}_orig, p{i}_main, p{i}_sub)
def ea_card(product_id, num, category, price, badge_color, badge_text, title, version, pair, timeframe, pf, wr, dd, modal_cap_key, mayar_url, gumroad_url, tg_text, orig_val="Rp 4.000.000", main_val="Rp 2.000.000", sub_val="atau <strong>$135 USD</strong> &middot; Lisensi Seumur Hidup"):
    return f'''
    <!-- EA SATUAN: {product_id} -->
    <div class="product-card bg-cardDark rounded-3xl border-2 border-{badge_color}-500/50 p-6 flex flex-col justify-between hover:border-{badge_color}-400 shadow-glow-{badge_color} relative overflow-hidden group" data-category="{category}" data-product-id="{product_id}" data-price="{price}">
      <div class="absolute top-0 right-0 bg-{badge_color}-600 text-white font-mono font-bold text-[9px] uppercase tracking-widest px-3.5 py-1 rounded-bl-xl">{badge_text}</div>
      <div>
        <h3 class="text-lg font-bold text-white tracking-tight group-hover:text-{badge_color}-400 transition-colors pr-24">{title} <span class="text-xs font-mono text-zinc-500">{version}</span></h3>
        <div class="flex gap-2 mt-2 flex-wrap">
          <span class="px-2 py-0.5 rounded-full bg-{badge_color}-500/20 border border-{badge_color}-500/40 text-{badge_color}-300 text-[10px] font-bold font-mono">{pair}</span>
          <span class="px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-400 text-[10px] font-mono">{timeframe}</span>
          <span class="px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-400 text-[10px] font-mono">MT5</span>
        </div>
        <div class="grid grid-cols-3 gap-2 mt-4 text-center">
          <div class="bg-zinc-950/70 p-2.5 rounded-xl border border-zinc-800"><div class="text-lg font-black font-mono text-{badge_color}-400">{pf}</div><div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-0.5" data-i18n="lbl_pf">Profit Factor</div></div>
          <div class="bg-zinc-950/70 p-2.5 rounded-xl border border-zinc-800"><div class="text-lg font-black font-mono text-emerald-400">{wr}%</div><div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-0.5" data-i18n="lbl_win">Win Rate</div></div>
          <div class="bg-zinc-950/70 p-2.5 rounded-xl border border-zinc-800"><div class="text-lg font-black font-mono text-rose-400">{dd}%</div><div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-0.5" data-i18n="lbl_dd">Max DD</div></div>
        </div>
        <div class="mt-3 text-[10px] font-mono text-zinc-500 text-center" data-i18n="lbl_backtest_note">Data Backtest &bull; Performa masa lalu bukan jaminan hasil masa depan</div>
        <div class="mt-4 text-[11px] font-mono text-zinc-400"><span data-i18n="lbl_min_cap">Modal Minimal:</span> <strong class="text-zinc-200" data-i18n="{modal_cap_key}">Loading...</strong></div>
      </div>
      <div>
        <div class="mt-6 pt-4 border-t border-zinc-800/80">
          <div class="flex items-center space-x-2 mb-1 text-xs">
            <span class="text-zinc-500 line-through font-mono" data-i18n="p{num}_orig">{orig_val}</span>
            <span class="text-emerald-400 font-bold font-mono text-[10px] bg-emerald-950/60 px-2 py-0.5 rounded-full border border-emerald-800/60" data-i18n="disc_badge">50% Launch Price</span>
          </div>
          <div class="text-2xl font-black font-mono text-{badge_color}-400 tracking-tight" data-i18n="p{num}_main">{main_val}</div>
          <div class="text-[11px] font-mono text-zinc-500 mt-0.5" data-i18n="p{num}_sub">{sub_val}</div>
        </div>
        <div class="mt-3">
          <button onclick="openModal('{product_id}')" class="w-full py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white text-xs font-bold tracking-wide transition-all cursor-pointer" data-i18n="btn_detail">LIHAT DETAIL 📄</button>
        </div>
{pay_buttons(mayar_url, gumroad_url, tg_text)}
      </div>
    </div>'''

ea_html = f'''<!-- ========================================== -->
<!-- 2. SECTION: KATALOG ROBOT EA SATUAN (STANDALONE) -->
<!-- ========================================== -->
<section id="katalog-ea" class="my-16 pt-12 border-t border-zinc-800">
  <div class="text-center max-w-3xl mx-auto mb-10">
    <div class="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono text-xs font-bold uppercase tracking-widest mb-3">
      <span>🤖</span>
      <span data-i18n="cat_kicker">STANDALONE ALGORITHMS</span>
    </div>
    <h2 class="text-3xl sm:text-5xl font-black text-white uppercase tracking-tight" data-i18n="cat_title">KATALOG ROBOT EA SATUAN</h2>
    <p class="text-zinc-400 text-sm sm:text-base mt-3 leading-relaxed" data-i18n="cat_sub">Pilih robot EA satuan sesuai modal dan strategi kamu mulai dari Rp 50.000 hingga Rp 4.000.000 dengan screenshot backtest terverifikasi.</p>
  </div>

  <!-- PRICE FILTER -->
  <div class="mb-4">
    <div class="text-xs font-mono text-zinc-400 mb-2 uppercase tracking-widest" data-i18n="lbl_price">FILTER HARGA PRODUK:</div>
    <div class="filter-scroll flex gap-2 pb-1">
      <button class="price-btn active whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-bold font-mono border border-emerald-500 text-emerald-300 bg-emerald-950/50 transition-all cursor-pointer" onclick="setPrice('all',this)" data-i18n="f_all">SEMUA (14)</button>
      <button class="price-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setPrice('100k',this)" data-i18n="f_100k">≤ Rp 100K</button>
      <button class="price-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setPrice('500k',this)" data-i18n="f_500k">≤ Rp 500K</button>
      <button class="price-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setPrice('1m',this)" data-i18n="f_1m">≤ Rp 1JT</button>
      <button class="price-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setPrice('vip',this)" data-i18n="f_vip">👑 VIP (> 1JT)</button>
    </div>
  </div>

  <!-- CATEGORY FILTER -->
  <div class="mb-8">
    <div class="text-xs font-mono text-zinc-400 mb-2 uppercase tracking-widest" data-i18n="lbl_cat">KATEGORI STRATEGI:</div>
    <div class="filter-scroll flex gap-2 pb-1">
      <button class="cat-btn active whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-bold font-mono border border-emerald-500 text-emerald-300 bg-emerald-950/50 transition-all cursor-pointer" onclick="setCategory('all',this)" data-i18n="c_all">SEMUA (14)</button>
      <button class="cat-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setCategory('flagship',this)" data-i18n="c_flagship">👑 FLAGSHIP</button>
      <button class="cat-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setCategory('hft',this)" data-i18n="c_hft">⚡ HIGH-FREQUENCY</button>
      <button class="cat-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setCategory('risk',this)" data-i18n="c_risk">🛡️ RISK MANAGEMENT</button>
      <button class="cat-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setCategory('trend',this)" data-i18n="c_trend">📈 TREND SYSTEM</button>
      <button class="cat-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setCategory('gold',this)" data-i18n="c_gold">🥇 GOLD SCALPING</button>
      <button class="cat-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setCategory('starter',this)" data-i18n="c_starter">🌱 STARTER &amp; CENT</button>
      <button class="cat-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer" onclick="setCategory('budget',this)" data-i18n="c_budget">🏷️ BUDGET (≤ 100K)</button>
    </div>
  </div>

  <div id="catalog-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 sm:gap-6">
    <!-- FILTER EMPTY STATE -->
    <div id="filter-empty" class="col-span-full text-center py-16 hidden">
      <div class="text-5xl mb-4">🔍</div>
      <div class="text-zinc-400 font-mono" data-i18n="empty_filter">Tidak ada robot EA yang cocok dengan filter ini.</div>
    </div>

{ea_card('apex-titan', 14, 'flagship','4000000','amber','👑 ULTRA INSTITUTIONAL',
    'AEMETH Apex Neural Titan Ultra','v5.0','XAUUSD / US30 / NAS100','M5 / M15',
    '6.85','92.40','3.10','cap14',
    MAYAR+'/apex-titan', GUMROAD+'/l/apex-titan', 'Apex%20Neural%20Titan%20Ultra%204jt',
    'Rp 8.000.000', 'Rp 4.000.000', 'atau <strong>$265 USD</strong> &middot; Lisensi Seumur Hidup')}

{ea_card('neural-master', 1, 'flagship','2000000','amber','👑 FLAGSHIP',
    'AEMETH Quantum Neural Master','v4.0','XAUUSD','M15',
    '5.91','90.16','4.02','cap1',
    MAYAR+'/neural-master', GUMROAD+'/l/neural-master', 'Neural%20Master%20v4')}

{ea_card('hft-multi', 2, 'hft','1500000','cyan','⚡ HIGH-FREQUENCY',
    'AEMETH Institutional HFT Multi','v3.2','EURUSD/GBPUSD','M1',
    '4.77','87.30','5.14','cap2',
    MAYAR+'/hft-multi', GUMROAD+'/l/hft-multi', 'HFT%20Multi%20v3')}

{ea_card('prop-shield', 3, 'risk','799000','rose','🛡️ RISK MANAGEMENT',
    'AEMETH Prop Shield','v2.1','All Pairs','M5',
    '3.88','85.60','3.50','cap3',
    MAYAR+'/prop-shield', GUMROAD+'/l/prop-shield', 'Prop%20Shield%20v2')}

{ea_card('trend-pulse', 4, 'trend','650000','violet','📈 TREND SYSTEM',
    'AEMETH Trend Pulse','v2.0','XAUUSD/Forex','H1',
    '3.21','82.40','6.80','cap3',
    MAYAR+'/trend-pulse', GUMROAD+'/l/trend-pulse', 'Trend%20Pulse%20v2')}

{ea_card('quantum-scalper', 5, 'gold','500000','yellow','🥇 GOLD SCALPING',
    'AEMETH Quantum Scalper Gold','v1.5','XAUUSD','M5',
    '4.12','88.50','4.75','cap4',
    MAYAR+'/quantum-scalper', GUMROAD+'/l/quantum-scalper', 'Quantum%20Scalper%20Gold')}

{ea_card('micro-cent', 6, 'starter','400000','teal','🌱 STARTER & CENT',
    'AEMETH Micro Cent Trader','v1.3','Any Pair','M15',
    '2.95','78.20','8.30','cap6',
    MAYAR+'/micro-cent', GUMROAD+'/l/micro-cent', 'Micro%20Cent%20Trader')}

{ea_card('budget-scalper', 7, 'budget','100000','lime','🏷️ BUDGET',
    'AEMETH Budget Scalper Nano','v1.0','EURUSD','M1',
    '2.30','74.50','9.80','cap7',
    MAYAR+'/budget-scalper', GUMROAD+'/l/budget-scalper', 'Budget%20Scalper%20Nano')}

{ea_card('mini-grid', 8, 'budget','50000','slate','🏷️ BUDGET',
    'AEMETH Mini Grid Breaker','v1.0','Any Pair','M5',
    '2.10','72.30','11.50','cap8',
    MAYAR+'/mini-grid', GUMROAD+'/l/mini-grid', 'Mini%20Grid%20Breaker')}

{ea_card('london-breakout', 9, 'trend','650000','orange','📈 TREND SYSTEM',
    'AEMETH London Breakout Rider','v1.2','EURUSD/GBPUSD','H1',
    '3.45','83.10','5.90','cap3',
    MAYAR+'/london-breakout', GUMROAD+'/l/london-breakout', 'London%20Breakout%20Rider')}

{ea_card('grid-momentum', 10, 'hft','500000','cyan','⚡ HIGH-FREQUENCY',
    'AEMETH Grid Momentum Pro','v1.1','EURUSD/GBPJPY','M5',
    '3.70','85.00','7.20','cap4',
    MAYAR+'/grid-momentum', GUMROAD+'/l/grid-momentum', 'Grid%20Momentum%20Pro')}

{ea_card('news-armor', 11, 'risk','799000','rose','🛡️ RISK MANAGEMENT',
    'AEMETH News Volatility Armor','v1.0','All Pairs','M1',
    '3.15','80.70','4.10','cap3',
    MAYAR+'/news-armor', GUMROAD+'/l/news-armor', 'News%20Volatility%20Armor')}

{ea_card('night-scalper', 12, 'gold','400000','yellow','🥇 GOLD SCALPING',
    'AEMETH Night Scalper Elite','v1.0','XAUUSD','M1',
    '4.05','87.60','5.20','cap6',
    MAYAR+'/night-scalper', GUMROAD+'/l/night-scalper', 'Night%20Scalper%20Elite')}

{ea_card('swing-multi', 13, 'trend','1500000','violet','📈 TREND SYSTEM',
    'AEMETH Multi-Currency Swing','v2.0','Multi-Pair','H4',
    '4.30','86.20','4.80','cap2',
    MAYAR+'/swing-multi', GUMROAD+'/l/swing-multi', 'Multi%20Currency%20Swing')}
  </div>
</section>
'''

# 7. INDICATORS (13 Indicators with dynamic ind{i}_orig, ind{i}_main, ind{i}_sub)
def ind_card(num, badge_tag, badge_color, title, desc_key, feat1_label, feat1_val, feat2_label, feat2_val, mayar_url, gumroad_url, tg_text):
    return f'''
    <!-- IND {num} -->
    <div class="bg-cardDark rounded-3xl border-2 border-{badge_color}-500/50 p-6 flex flex-col justify-between hover:border-{badge_color}-400 shadow-glow-{badge_color} relative overflow-hidden group">
      <div class="absolute top-0 right-0 bg-{badge_color}-600 text-white font-mono font-bold text-[9px] uppercase tracking-widest px-3.5 py-1 rounded-bl-xl">{badge_tag}</div>
      <div>
        <div class="flex items-center justify-between mb-4">
          <span class="px-2 py-0.5 rounded-full bg-{badge_color}-500/20 border border-{badge_color}-500/40 text-{badge_color}-300 text-[10px] font-bold font-mono">Non-Repaint</span>
          <span class="text-[10px] font-mono text-zinc-400">MT5</span>
        </div>
        <h3 class="text-base font-bold text-white tracking-tight group-hover:text-{badge_color}-400 transition-colors">{title}</h3>
        <p class="text-zinc-400 text-xs leading-relaxed mt-2 font-light" data-i18n="{desc_key}">Loading...</p>
        <div class="grid grid-cols-2 gap-2 mt-4 text-[11px] font-mono text-zinc-400">
          <div class="bg-zinc-950/70 p-2.5 rounded-xl border border-zinc-800">{feat1_label}: <strong class="text-zinc-200">{feat1_val}</strong></div>
          <div class="bg-zinc-950/70 p-2.5 rounded-xl border border-zinc-800">{feat2_label}: <strong class="{badge_color}-300">{feat2_val}</strong></div>
        </div>
      </div>
      <div>
        <div class="mt-6 pt-4 border-t border-zinc-800/80">
          <div class="flex items-center space-x-2 mb-1 text-xs">
            <span class="text-zinc-500 line-through font-mono" data-i18n="ind{num}_orig">Rp 900.000</span>
            <span class="text-emerald-400 font-bold font-mono text-[10px] bg-emerald-950/60 px-2 py-0.5 rounded-full border border-emerald-800/60" data-i18n="disc_badge">50% Launch Price</span>
          </div>
          <div class="text-2xl font-black font-mono text-{badge_color}-400 tracking-tight" data-i18n="ind{num}_main">Rp 450.000</div>
          <div class="text-[11px] font-mono text-zinc-500 mt-0.5" data-i18n="ind{num}_sub">atau <strong>$30 USD</strong> &middot; Lisensi Seumur Hidup</div>
        </div>
{pay_buttons(mayar_url, gumroad_url, tg_text)}
      </div>
    </div>'''

ind_html = f'''<!-- ========================================== -->
<!-- 3. SECTION: KATALOG INDIKATOR MT5 PRO -->
<!-- ========================================== -->
<section id="katalog-indikator" class="my-16 pt-12 border-t border-zinc-800">
  <div class="text-center max-w-2xl mx-auto mb-10">
    <span class="text-xs font-mono uppercase tracking-[0.25em] text-purple-400 font-bold" data-i18n="ind_kicker">PROFESSIONAL MT5 CUSTOM TOOLS</span>
    <h2 class="text-3xl sm:text-4xl font-black text-white uppercase tracking-tight mt-1" data-i18n="ind_title">KATALOG INDIKATOR MT5 PRO</h2>
    <p class="text-zinc-400 text-sm mt-2" data-i18n="ind_sub">Loading...</p>
  </div>
  
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 sm:gap-6">
{ind_card(1,'SMC PRO','purple',
    'AEMETH Order Block &amp; Liquidity Hunter',
    'ind1_desc','Fitur','Alert &amp; Popup','Platform','All MT5 Pairs',
    MAYAR+'/ind-ob', GUMROAD+'/l/ind-ob', 'Indikator%20Order%20Block')}

{ind_card(2,'SIGNAL','emerald',
    'AEMETH Non-Repaint Arrow Signal Pro',
    'ind2_desc','Type','Buy/Sell Arrow','Repaint','0% Non-Repaint',
    MAYAR+'/ind-signal', GUMROAD+'/l/ind-signal', 'Indikator%20Arrow%20Signal')}

{ind_card(3,'SUPPLY DEMAND','rose',
    'AEMETH Supply &amp; Demand Zone Pro',
    'ind3_desc','Fitur','Auto Zone Draw','Platform','All MT5 Pairs',
    MAYAR+'/ind-sd', GUMROAD+'/l/ind-sd', 'Indikator%20Supply%20Demand')}

{ind_card(4,'DIVERGENCE','amber',
    'AEMETH RSI &amp; MACD Divergence Matrix',
    'ind4_desc','Type','RSI &amp; MACD','Signals','Real-time Alert',
    MAYAR+'/ind-div', GUMROAD+'/l/ind-div', 'Indikator%20Divergence%20Matrix')}

{ind_card(5,'TREND HUD','blue',
    'AEMETH Multi-TF Trend Dashboard',
    'ind5_desc','TF Coverage','M1 to D1','Display','Single HUD',
    MAYAR+'/ind-trend', GUMROAD+'/l/ind-trend', 'Indikator%20Trend%20Dashboard')}

{ind_card(6,'SUPPORT RES','teal',
    'AEMETH Dynamic Support &amp; Resistance',
    'ind6_desc','Type','Fractal Nodes','Fitur','Breakout Target',
    MAYAR+'/ind-sr', GUMROAD+'/l/ind-sr', 'Indikator%20Support%20Resistance')}

{ind_card(7,'CANDLE HUD','zinc',
    'AEMETH Candle Timer &amp; Spread Monitor',
    'ind7_desc','Info','Timer &amp; Spread','Extra','Server Ping',
    MAYAR+'/ind-timer', GUMROAD+'/l/ind-timer', 'Indikator%20Candle%20Timer')}

{ind_card(8,'VOLUME PROFILE','violet',
    'AEMETH Volume Profile &amp; VWAP Pro',
    'ind8_desc','Type','Volume Profile','Fitur','VWAP + SD Bands',
    MAYAR+'/ind-vp', GUMROAD+'/l/ind-vp', 'Indikator%20Volume%20Profile')}

{ind_card(9,'ICT TOOLS','sky',
    'AEMETH ICT Concepts Suite',
    'ind9_desc','Fitur','FVG + MSS + OTE','Platform','All MT5 Pairs',
    MAYAR+'/ind-ict', GUMROAD+'/l/ind-ict', 'Indikator%20ICT%20Suite')}

{ind_card(10,'BOLLINGER+RSI','lime',
    'AEMETH Bollinger Squeeze &amp; RSI Alert',
    'ind10_desc','Type','Squeeze Scanner','Alert','Push &amp; Email',
    MAYAR+'/ind-bb', GUMROAD+'/l/ind-bb', 'Indikator%20Bollinger%20Squeeze')}

{ind_card(11,'FIBONACCI','orange',
    'AEMETH Auto Fibonacci Extension Pro',
    'ind11_desc','Type','Auto Fib Draw','Levels','23.6% - 4.236%',
    MAYAR+'/ind-fib', GUMROAD+'/l/ind-fib', 'Indikator%20Fibonacci%20Auto')}

{ind_card(12,'SESSION MAP','pink',
    'AEMETH Market Session &amp; Killzone Map',
    'ind12_desc','Sessions','London/NY/Asia','Fitur','Killzone Overlay',
    MAYAR+'/ind-session', GUMROAD+'/l/ind-session', 'Indikator%20Session%20Map')}

{ind_card(13,'PIVOT POINTS','cyan',
    'AEMETH Smart Pivot Points &amp; CPR Pro',
    'ind13_desc','Type','Daily/Weekly CPR','Levels','S1-S3 R1-R3',
    MAYAR+'/ind-pivot', GUMROAD+'/l/ind-pivot', 'Indikator%20Pivot%20Points')}
  </div>
</section>
'''

# 8. PACKAGE INCLUDES
pkg_html = '''<!-- ========================================== -->
<!-- 4. SECTION: PACKAGE INCLUDES -->
<!-- ========================================== -->
<section id="package-includes" class="my-16 pt-12 border-t border-zinc-800/80">
  <div class="metallic-shine rounded-3xl border border-zinc-700/60 p-6 sm:p-12 shadow-2xl">
    <div class="text-center max-w-2xl mx-auto mb-10">
      <span class="text-xs font-mono uppercase tracking-[0.25em] text-emerald-400 font-bold" data-i18n="pkg_kicker">COMPLETE DELIVERABLE PACKAGE</span>
      <h2 class="text-3xl sm:text-4xl font-black text-white uppercase tracking-tight mt-1" data-i18n="pkg_title">APA YANG ANDA DAPATKAN</h2>
      <p class="text-zinc-400 text-sm mt-2" data-i18n="pkg_sub">Bukan sekadar file program, Anda menerima paket ekosistem trading terstruktur siap pakai.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 text-xs font-mono">
      <div class="flex items-start space-x-3 p-4 bg-zinc-950/80 rounded-2xl border border-zinc-800/90">
        <span class="text-emerald-400 text-base font-bold shrink-0">&#10003;</span>
        <div>
          <strong class="text-white block mb-1" data-i18n="pkg_1_t">File Murni .EX5 (MT5 Native)</strong>
          <span class="text-zinc-400" data-i18n="pkg_1_d">Compiled binary original siap dimasukkan ke folder Experts MT5.</span>
        </div>
      </div>
      <div class="flex items-start space-x-3 p-4 bg-zinc-950/80 rounded-2xl border border-zinc-800/90">
        <span class="text-emerald-400 text-base font-bold shrink-0">&#10003;</span>
        <div>
          <strong class="text-white block mb-1" data-i18n="pkg_2_t">Lifetime Permanent License</strong>
          <span class="text-zinc-400" data-i18n="pkg_2_d">Lisensi permanen tanpa biaya langganan bulanan berulang.</span>
        </div>
      </div>
      <div class="flex items-start space-x-3 p-4 bg-zinc-950/80 rounded-2xl border border-zinc-800/90">
        <span class="text-emerald-400 text-base font-bold shrink-0">&#10003;</span>
        <div>
          <strong class="text-white block mb-1" data-i18n="pkg_3_t">Panduan Instalasi (PDF &amp; Video)</strong>
          <span class="text-zinc-400" data-i18n="pkg_3_d">Tutorial ramah pemula dari pasang hingga aktivasi dalam 5 menit.</span>
        </div>
      </div>
      <div class="flex items-start space-x-3 p-4 bg-zinc-950/80 rounded-2xl border border-zinc-800/90">
        <span class="text-emerald-400 text-base font-bold shrink-0">&#10003;</span>
        <div>
          <strong class="text-white block mb-1" data-i18n="pkg_4_t">Preset Setting File (.SET)</strong>
          <span class="text-zinc-400" data-i18n="pkg_4_d">Konfigurasi terkalibrasi untuk Gold, Forex mayor, dan indeks.</span>
        </div>
      </div>
      <div class="flex items-start space-x-3 p-4 bg-zinc-950/80 rounded-2xl border border-zinc-800/90">
        <span class="text-emerald-400 text-base font-bold shrink-0">&#10003;</span>
        <div>
          <strong class="text-white block mb-1" data-i18n="pkg_5_t">Free Algorithm Update Policy</strong>
          <span class="text-zinc-400" data-i18n="pkg_5_d">Pembaruan perbaikan bug dan kalibrasi algoritma gratis selamanya.</span>
        </div>
      </div>
      <div class="flex items-start space-x-3 p-4 bg-zinc-950/80 rounded-2xl border border-zinc-800/90">
        <span class="text-emerald-400 text-base font-bold shrink-0">&#10003;</span>
        <div>
          <strong class="text-white block mb-1" data-i18n="pkg_6_t">VIP AnyDesk &amp; Telegram Support</strong>
          <span class="text-zinc-400" data-i18n="pkg_6_d">Bantuan remote setting via AnyDesk bagi pemula serta konsultasi strategi.</span>
        </div>
      </div>
    </div>
  </div>
</section>
'''

# 9. FAQ & DISCLAIMER (With pre-rendered content and robust toggle)
faq_html = '''<!-- ========================================== -->
<!-- 5. SECTION: FAQ & DISCLAIMER -->
<!-- ========================================== -->
<section id="faq" class="my-16 pt-12 border-t border-zinc-800">
  <div class="text-center max-w-2xl mx-auto mb-10">
    <span class="text-xs font-mono uppercase tracking-[0.25em] text-amber-400 font-bold" data-i18n="faq_kicker">KNOWLEDGE BASE &amp; RISK POLICY</span>
    <h2 class="text-3xl sm:text-4xl font-black text-white uppercase tracking-tight mt-1" data-i18n="faq_title">PERTANYAAN UMUM &amp; DISCLAIMER</h2>
    <p class="text-zinc-400 text-sm mt-2" data-i18n="faq_sub">Penjelasan transparan tentang cara kerja EA, risiko trading, dan batasan tanggung jawab hukum.</p>
  </div>
  <div class="max-w-4xl mx-auto space-y-3.5">
    <div class="bg-cardDark border border-zinc-800 rounded-2xl overflow-hidden hover:border-zinc-700 transition-all">
      <button onclick="toggleFaq(this)" type="button" class="w-full p-5 sm:p-6 text-left flex items-center justify-between space-x-4 focus:outline-none cursor-pointer">
        <span class="font-bold text-white text-sm sm:text-base" data-i18n="faq1_q"><span class="text-emerald-400 mr-2">&#129302;</span> Apa itu Robot Expert Advisor (EA) MT5 dan bagaimana cara kerjanya?</span>
        <span class="faq-chevron text-zinc-400 font-mono shrink-0 select-none">&#9660;</span>
      </button>
      <div class="faq-answer px-5 sm:px-6 pb-5 text-xs sm:text-sm text-zinc-300 leading-relaxed border-t border-zinc-800/60 pt-4" data-i18n="faq1_a">
        <strong>Robot Expert Advisor (EA)</strong> adalah program perangkat lunak algoritma yang dipasang di MetaTrader 5 (MT5). EA bekerja otomatis 24/5 menganalisis harga, menghitung lot, membuka posisi Buy/Sell, dan memasang TP/SL secara otomatis tanpa intervensi emosi manusia.
      </div>
    </div>
    <div class="bg-cardDark border-2 border-amber-500/40 rounded-2xl overflow-hidden hover:border-amber-400 transition-all">
      <button onclick="toggleFaq(this)" type="button" class="w-full p-5 sm:p-6 text-left flex items-center justify-between space-x-4 focus:outline-none cursor-pointer">
        <span class="font-bold text-amber-300 text-sm sm:text-base" data-i18n="faq2_q"><span class="text-amber-400 mr-2">&#9888;&#65039;</span> Apakah Robot EA ini selalu profit dan ada jaminan keuntungan?</span>
        <span class="faq-chevron text-amber-400 font-mono shrink-0 select-none">&#9660;</span>
      </button>
      <div class="faq-answer px-5 sm:px-6 pb-5 text-xs sm:text-sm text-zinc-300 leading-relaxed border-t border-amber-500/20 pt-4 bg-amber-950/20" data-i18n="faq2_a">
        <p class="mb-2"><strong>TIDAK. Robot EA TIDAK SELALU PROFIT, dan kami SAMA SEKALI TIDAK MENJAMIN PROFIT.</strong></p>
        <p class="text-zinc-400 mb-2">Trading memiliki risiko fluktuasi harga yang tinggi. Hasil backtest tidak menjamin keuntungan di masa mendatang.</p>
        <p class="text-amber-300 font-semibold">Gunakanlah selalu dana dingin yang siap Anda tanggung risikonya.</p>
      </div>
    </div>
    <div class="bg-cardDark border-2 border-rose-500/40 rounded-2xl overflow-hidden hover:border-rose-400 transition-all">
      <button onclick="toggleFaq(this)" type="button" class="w-full p-5 sm:p-6 text-left flex items-center justify-between space-x-4 focus:outline-none cursor-pointer">
        <span class="font-bold text-rose-300 text-sm sm:text-base" data-i18n="faq3_q"><span class="text-rose-400 mr-2">&#9878;&#65039;</span> Bagaimana jika terjadi kerugian (Loss) pada akun trading saya?</span>
        <span class="faq-chevron text-rose-400 font-mono shrink-0 select-none">&#9660;</span>
      </button>
      <div class="faq-answer px-5 sm:px-6 pb-5 text-xs sm:text-sm text-zinc-300 leading-relaxed border-t border-rose-500/20 pt-4 bg-rose-950/20" data-i18n="faq3_a">
        <p class="mb-2"><strong>Segala kerugian finansial, margin call, atau drawdown sepenuhnya adalah TANGGUNG JAWAB PRIBADI ANDA SEBAGAI TRADER.</strong></p>
        <p class="text-zinc-400 mb-2">Kami bertindak murni sebagai pengembang software. Kami <strong>BUKAN pengelola dana, bukan penasihat keuangan, dan TIDAK BERTANGGUNG JAWAB</strong> atas kerugian akun, gangguan broker/internet, atau kesalahan pemilihan lot.</p>
        <p class="text-zinc-400">Dengan membeli software ini, Anda menyatakan telah membaca dan menyetujui seluruh risiko perdagangan.</p>
      </div>
    </div>
    <div class="bg-cardDark border border-zinc-800 rounded-2xl overflow-hidden hover:border-zinc-700 transition-all">
      <button onclick="toggleFaq(this)" type="button" class="w-full p-5 sm:p-6 text-left flex items-center justify-between space-x-4 focus:outline-none cursor-pointer">
        <span class="font-bold text-white text-sm sm:text-base" data-i18n="faq4_q"><span class="text-purple-400 mr-2">&#128202;</span> Apa perbedaan Robot EA dengan Indikator MT5?</span>
        <span class="faq-chevron text-zinc-400 font-mono shrink-0 select-none">&#9660;</span>
      </button>
      <div class="faq-answer px-5 sm:px-6 pb-5 text-xs sm:text-sm text-zinc-300 leading-relaxed border-t border-zinc-800/60 pt-4" data-i18n="faq4_a">
        <strong>Robot EA</strong> adalah sistem otomatis penuh yang membuka dan menutup posisi sendiri. <strong>Indikator Custom</strong> adalah alat bantu visual (Order Block, Supply &amp; Demand, sinyal panah) untuk membantu trading manual.
      </div>
    </div>
    <div class="bg-cardDark border border-zinc-800 rounded-2xl overflow-hidden hover:border-zinc-700 transition-all">
      <button onclick="toggleFaq(this)" type="button" class="w-full p-5 sm:p-6 text-left flex items-center justify-between space-x-4 focus:outline-none cursor-pointer">
        <span class="font-bold text-white text-sm sm:text-base" data-i18n="faq5_q"><span class="text-blue-400 mr-2">&#127760;</span> Apakah saya harus memakai VPS?</span>
        <span class="faq-chevron text-zinc-400 font-mono shrink-0 select-none">&#9660;</span>
      </button>
      <div class="faq-answer px-5 sm:px-6 pb-5 text-xs sm:text-sm text-zinc-300 leading-relaxed border-t border-zinc-800/60 pt-4" data-i18n="faq5_a">
        Untuk Robot EA, sangat disarankan menggunakan <strong>VPS Windows</strong> agar EA berjalan 24 jam nonstop tanpa laptop Anda harus menyala. Rekomendasi VPS murah berkualitas ($3-$5/bulan) tersedia di dalam panduan instalasi.
      </div>
    </div>
  </div>
  <!-- Risk callout -->
  <div class="max-w-4xl mx-auto mt-10 p-6 bg-gradient-to-r from-amber-950/40 via-zinc-900 to-rose-950/40 border border-amber-500/40 rounded-2xl shadow-xl">
    <div class="flex items-start space-x-3.5">
      <span class="text-2xl shrink-0">&#128737;&#65039;</span>
      <div>
        <h4 class="text-sm font-bold uppercase tracking-wider text-amber-300 mb-1" data-i18n="disc_title">PEMBERITAHUAN RESMI TENTANG RISIKO &amp; TANGGUNG JAWAB</h4>
        <p class="text-xs text-zinc-400 leading-relaxed" data-i18n="disc_desc">Trading Forex, Komoditas (Emas/XAUUSD), dan Indeks membawa tingkat risiko kerugian finansial yang signifikan. Produk software kami disediakan apa adanya ("as-is") sebagai alat bantu teknologi analisis. Anda bertanggung jawab penuh atas segala hasil, untung, maupun rugi pada portofolio Anda.</p>
      </div>
    </div>
  </div>
</section>

</main>
'''

# 10. DETAIL MODAL
modal_html = '''<!-- DETAIL MODAL -->
<div id="detail-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/85 backdrop-blur-md overflow-y-auto">
  <div class="relative w-full max-w-2xl bg-zinc-950 border border-zinc-800 rounded-3xl p-6 sm:p-8 shadow-2xl my-auto">
    <button onclick="closeModal()" class="absolute top-5 right-5 w-8 h-8 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-400 hover:text-white flex items-center justify-center font-bold text-sm transition-all cursor-pointer">&times;</button>
    <div class="flex items-center space-x-2 mb-2">
      <span id="modal-tag" class="px-3 py-1 rounded-full text-xs font-bold font-mono"></span>
      <span class="text-zinc-500 text-xs font-mono">MetaTrader 5 Native</span>
    </div>
    <h3 id="modal-name" class="text-2xl font-black text-white tracking-tight"></h3>
    <div class="flex flex-wrap gap-2 mt-2 text-xs font-mono text-zinc-400">
      <span class="bg-zinc-900 px-2.5 py-1 rounded-lg border border-zinc-800">Pair: <strong id="modal-pair" class="text-white"></strong></span>
      <span class="bg-zinc-900 px-2.5 py-1 rounded-lg border border-zinc-800">Timeframe: <strong id="modal-tf" class="text-white"></strong></span>
      <span class="bg-zinc-900 px-2.5 py-1 rounded-lg border border-zinc-800">Strategy: <strong id="modal-strategy" class="text-emerald-400"></strong></span>
    </div>
    
    <!-- Stats Grid -->
    <div class="grid grid-cols-4 gap-2 mt-5 text-center">
      <div class="bg-zinc-900/80 p-3 rounded-2xl border border-zinc-800">
        <div id="modal-pf" class="text-xl font-black font-mono text-amber-400"></div>
        <div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-0.5" data-i18n="lbl_pf">Profit Factor</div>
      </div>
      <div class="bg-zinc-900/80 p-3 rounded-2xl border border-zinc-800">
        <div id="modal-wr" class="text-xl font-black font-mono text-emerald-400"></div>
        <div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-0.5" data-i18n="lbl_win">Win Rate</div>
      </div>
      <div class="bg-zinc-900/80 p-3 rounded-2xl border border-zinc-800">
        <div id="modal-dd" class="text-xl font-black font-mono text-rose-400"></div>
        <div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-0.5" data-i18n="lbl_dd">Max DD</div>
      </div>
      <div class="bg-zinc-900/80 p-3 rounded-2xl border border-zinc-800">
        <div id="modal-trades" class="text-xl font-black font-mono text-blue-400"></div>
        <div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-0.5" data-i18n="m_lbl_trades">Total Trades</div>
      </div>
    </div>
    <div class="mt-2 text-[10px] font-mono text-zinc-500 text-center">
      <span data-i18n="m_lbl_period">Periode Pengujian:</span> <strong id="modal-period" class="text-zinc-400"></strong>
    </div>

    <!-- Description -->
    <div class="mt-4 pt-4 border-t border-zinc-800/80">
      <h4 class="text-xs font-mono text-zinc-400 uppercase tracking-wider mb-1.5" data-i18n="m_lbl_desc">Deskripsi Algoritma:</h4>
      <p id="modal-desc" class="text-xs sm:text-sm text-zinc-300 leading-relaxed font-light"></p>
    </div>

    <!-- Inclusions list -->
    <div class="mt-4 pt-4 border-t border-zinc-800/80">
      <h4 class="text-xs font-mono text-zinc-400 uppercase tracking-wider mb-2" data-i18n="m_lbl_inc">Paket Yang Anda Terima:</h4>
      <ul id="modal-includes" class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono text-zinc-300"></ul>
    </div>

    <!-- Note -->
    <div class="mt-4 p-3 rounded-xl bg-zinc-900 border border-zinc-800 text-[11px] font-mono text-zinc-400 flex items-start space-x-2">
      <span class="text-amber-400 shrink-0">⚠️</span>
      <span id="modal-note"></span>
    </div>
  </div>
</div>
'''

# 11. FOOTER
footer_html = '''<!-- FOOTER -->
<footer class="w-full border-t border-zinc-800/80 py-8 px-4 sm:px-12 max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between text-[11px] font-mono text-zinc-500 space-y-4 sm:space-y-0">
  <div data-i18n="ft_rights">&copy; 2026 AEMETH TRADER. Hak Cipta Dilindungi.</div>
  <div class="flex items-center space-x-6 text-zinc-400">
    <span class="text-zinc-600" data-i18n="ft_connect">HUBUNGI KAMI</span>
    <a href="https://t.me/aemethtrader" target="_blank" class="hover:text-white transition-colors">Telegram</a>
    <a href="#" class="hover:text-white transition-colors">X / Twitter</a>
    <a href="#" class="hover:text-white transition-colors">YouTube</a>
    <a href="#" class="hover:text-white transition-colors">TradingView</a>
  </div>
</footer>
'''

# 12. SCRIPT with complete dictionaries and perfect syntax
script_html = '''<script>
const T = {
  id: {
    nav_sub_brand:"SYSTEMATIC MT5 LAB",
    top_vip_badge:"VIP SERVICE",
    top_service:"Gratis Panduan &amp; Bantuan Pasang via AnyDesk / TeamViewer &bull; Garansi File .EX5 Terkirim Instan",
    top_tele:"KONSULTASI TELEGRAM",
    nav_perf:"PERFORMA", nav_why:"KENAPA AEMETH?", nav_bundle:"PAKET BUNDLE", nav_ea:"EA SATUAN", nav_ind:"INDIKATOR", nav_inc:"KELENGKAPAN", nav_faq:"FAQ", nav_catalog:"KATALOG EA",
    nav_status:"Status EA: Aktif &amp; Terverifikasi",
    hero_kicker:"SISTEM TRADING ALGORITMIK KUANTITATIF MT5",
    hero_title:"QUANTUM<br/>TRADER",
    hero_desc:"Sistem trading kuantitatif MT5 berbasis aturan terukur (rule-based). Menggabungkan algoritma MQL5 berlatensi rendah, manajemen posisi terkontrol, dan pengujian historis transparan.",
    hero_btn_bundle:"PAKET BUNDLE", hero_btn_ea:"EA SATUAN", hero_btn_ind:"INDIKATOR PRO",
    hero_pay_label:"METODE PEMBAYARAN:",
    hero_mockup_routing:"Order Routing: MT5 Native C++",
    hero_prop_tag:"KOMPATIBEL PROP FIRM", hero_prop_title:"MODEL RISIKO TERUKUR",
    perf_kicker:"DATA AUDIT BACKTEST TERVERIFIKASI", perf_title:"RINGKASAN PERFORMA",
    perf_pair:"XAUUSD &middot; MT5 &middot; Backtest",
    stat_pf:"PROFIT FACTOR", stat_win:"WIN RATE", stat_dd:"MAX DRAWDOWN",
    perf_context:"<strong>Hasil berdasarkan:</strong> AEMETH Quantum Neural Master v4.0, Jan 2024&ndash;Des 2025, Timeframe M15 (Exness Pro Server, 99.9% Tick Quality). Hasil backtest bukan jaminan performa masa depan.",
    perf_disc:"*Pengujian historis tersimulasi di bawah parameter risiko tetap.",
    why_kicker:"ARSITEKTUR SISTEMATIS", why_title:"KENAPA MEMILIH AEMETH?",
    why_sub:"Dibangun dengan filosofi trading sistematis dan manajemen eksposur yang disiplin.",
    w1t:"Eksekusi Rule-Based", w1d:"Menghilangkan gangguan emosi subjektif. Order dieksekusi murni berdasarkan parameter teknikal terukur.",
    w2t:"Manajemen Risiko Otomatis", w2d:"Dirancang untuk mengurangi exposure berlebihan. Hard Stop Loss setiap transaksi dan batas drawdown harian terukur.",
    w3t:"MT5 Native C++", w3d:"Eksekusi native latensi rendah untuk MetaTrader 5 memastikan efisiensi memori optimal dan routing broker ECN.",
    w4t:"Lisensi Seumur Hidup", w4d:"Akuisisi permanen satu kali tanpa biaya langganan bulanan berulang.",
    w5t:"Pengiriman Instan", w5d:"File .ex5 binary murni dan file konfigurasi dikirim ke inbox kamu dalam 1 detik setelah pembayaran terkonfirmasi.",
    bundle_kicker:"PENAWARAN HEMAT ALL-IN-ONE", bundle_title:"PAKET BUNDLE HEMAT MT5",
    bundle_sub:"Dapatkan kombinasi lengkap Robot EA otomatis multi-strategi + Indikator Pro non-repaint dengan diskon 50%. Solusi terbaik untuk diversifikasi portofolio dan akun challenge.",
    b1_badge:"INSTITUTIONAL FLAGSHIP",
    b1_hot_tag:"⭐ REKOMENDASI TERBAIK UNTUK AKUN BESAR &amp; PROP FIRM",
    b1_save_tag:"HEMAT RP 3.000.000",
    b1_title:"AEMETH MASTER BUNDLE 6 Tools",
    b1_tools_line:"4 Robot EA MT5 + 2 Indikator Pro — Akses Seumur Hidup",
    bundle_desc:"Dapatkan suite lengkap: 4 Expert Advisor MT5 institusional + 2 Indikator MT5 Pro non-repaint. Arsenal all-in-one untuk pertumbuhan pribadi, scalping cepat, dan evaluasi challenge Prop Firm.",
    b1_inc_header:"DAFTAR 6 TOOLS YANG DIDAPAT:",
    b1_vip_bonus_title:"HAK ISTIMEWA VIP EKSKLUSIF:",
    b1_free_tag:"GRATIS",
    b1_bonus_1:"1-on-1 Remote Setup via AnyDesk / TeamViewer Prioritas",
    b1_bonus_2:"Setfile Khusus Low Drawdown untuk Challenge Prop Firm",
    b1_bonus_3:"Akses Komunitas VIP Telegram &amp; Update Algoritma Seumur Hidup",
    b1_urgency:"HANYA TERSISA 5 LISENSI DENGAN BANTUAN ANYDESK SETUP",
    bundle_discount_badge:"50% DISKON VIP",
    price_orig_b1:"Rp 6.000.000",
    price_main_b1:"Rp 3.000.000",
    price_sub_b1:"atau <strong>$199 USD</strong> &middot; Akses Seumur Hidup (6 Alat)",
    b2_badge:"#1 BEST SELLER — 14 TOOLS",
    b2_seller_tag:"🏆 PALING BANYAK DIPILIH TRADER (14 TOOLS ALL-IN-ONE)",
    b2_rate_tag:"HANYA RP 178.000 / TOOL!",
    b2_title:"AEMETH MEGA BUNDLE 14 Tools v2.0",
    b2_tools_line:"10 Robot EA MT5 + 4 Indikator Pro — Akses Seumur Hidup",
    bundle2_desc:"Suite all-inclusive terlengkap dari AEMETH TRADER. Dapatkan 10 Robot EA MT5 otomatis (Gold, Forex, Indeks, Prop Firm, Cent &amp; HFT) plus 4 Indikator MT5 Pro non-repaint untuk trading manual. Termasuk dukungan instalasi remote AnyDesk gratis.",
    b2_inc_header:"ARSENAL LENGKAP 14 TOOLS MT5:",
    b2_val_calc_lbl:"Total Harga Beli Satuan (14 Tools):",
    b2_val_calc_orig:"Rp 9.800.000+",
    b2_val_save_lbl:"Penghematan Bersih Anda:",
    b2_val_save_val:"+Rp 7.300.000 (Hemat 74%)",
    b2_social_proof:"98% TRADER MEMILIH PAKET INI KARENA PALING LENGKAP",
    bundle2_discount_badge:"50% DISKON LAUNCH",
    price_orig_b2:"Rp 5.000.000",
    price_main_b2:"Rp 2.500.000",
    price_sub_b2:"atau <strong>$165 USD</strong> &middot; Akses Seumur Hidup (14 Alat)",
    b4_badge:"⚡ STARTER BUNDLE — 11 TOOLS",
    b4_title:"AEMETH STARTER BUNDLE 5 EA + 6 Ind",
    b4_tools_line:"5 Robot EA MT5 + 6 Indikator Pro — Akses Seumur Hidup",
    bundle4_desc:"Paket pemula lengkap dari AEMETH TRADER. Dapatkan 5 Robot EA MT5 otomatis (London Breakout, Grid Momentum, News Armor, Night Scalper, Swing Multi) plus 6 Indikator MT5 Pro pilihan untuk trading manual. Termasuk panduan setup gratis.",
    bundle4_discount_badge:"50% DISKON",
    price_orig_b4:"Rp 4.000.000",
    price_main_b4:"Rp 2.000.000",
    price_sub_b4:"atau <strong>$130 USD</strong> &middot; Akses Seumur Hidup (11 Alat)",
    b3_badge:"🔥 HYBRID BUNDLE — 11 TOOLS",
    b3_title:"AEMETH HYBRID SUITE 3 EA + 8 Ind",
    b3_tools_line:"3 Robot EA MT5 + 8 Indikator Pro — Akses Seumur Hidup",
    bundle3_desc:"Sinergi optimal antara otomasi penuh dan charting manual. Dapatkan 3 EA MT5 terbukti (Gold Scalper, Trend Pulse, Micro Cent) plus semua 8 Indikator MT5 Pro non-repaint untuk presisi charting institusional.",
    bundle3_discount_badge:"50% DISKON",
    price_orig_b3:"Rp 3.000.000",
    price_main_b3:"Rp 1.500.000",
    price_sub_b3:"atau <strong>$99 USD</strong> &middot; Akses Seumur Hidup (11 Alat)",
    cat_kicker:"STANDALONE ALGORITHMS", cat_title:"KATALOG ROBOT EA SATUAN",
    cat_sub:"Pilih robot EA satuan sesuai modal dan strategi kamu mulai dari Rp 50.000 hingga Rp 4.000.000 dengan screenshot backtest terverifikasi.",
    lbl_price:"FILTER HARGA PRODUK:", hint_price:"Filter berdasarkan harga jual software",
    f_all:"SEMUA (14)", f_100k:"≤ Rp 100K", f_500k:"≤ Rp 500K", f_1m:"≤ Rp 1JT", f_vip:"👑 VIP (> 1JT)",
    lbl_cat:"KATEGORI STRATEGI:", hint_cat:"Pilih gaya trading robot",
    c_all:"SEMUA (14)", c_flagship:"👑 FLAGSHIP", c_hft:"⚡ HIGH-FREQUENCY",
    c_risk:"🛡️ RISK MANAGEMENT", c_trend:"📈 TREND SYSTEM", c_gold:"🥇 GOLD SCALPING", c_starter:"🌱 STARTER &amp; CENT", c_budget:"🏷️ BUDGET (≤ 100K)",
    empty_filter:"Tidak ada robot EA yang cocok dengan filter ini.",
    lbl_pf:"Profit Factor", lbl_win:"Win Rate", lbl_dd:"Max DD",
    lbl_backtest_note:"Data Backtest &bull; Performa masa lalu bukan jaminan hasil masa depan",
    lbl_min_cap:"Modal Minimal:",
    btn_detail:"LIHAT DETAIL 📄",
    btn_pay_qris:"QRIS / BANK TRANSFER", btn_pay_global:"PAYPAL / CARD / CRYPTO", btn_pay_tg:"P2P CRYPTO (USDT)",
    disc_badge:"50% Harga Launch",
    cap1:"Modal $500+ (10JT IDR)", cap2:"Modal $300+ (5JT IDR)", cap3:"Modal $100+ (1JT IDR)", cap4:"Modal $50 (500K IDR)",
    cap5:"$10 Cent/Std (100K IDR)", cap6:"$10 Cent (100K IDR)", cap7:"$5 Cent (50K IDR)", cap8:"$5 Cent (50K IDR)",
    cap9:"Modal $100+ (1JT IDR)", cap10:"Modal $50 (500K IDR)", cap11:"Modal $100+ (1JT IDR)", cap12:"$10 Cent (100K IDR)", cap13:"Modal $300+ (5JT IDR)",
    cap14:"Modal $1,000+ (15JT IDR) / Prop Firm $50K-$200K",
    p14_orig:"Rp 8.000.000", p14_main:"Rp 4.000.000", p14_sub:"atau <strong>$265 USD</strong> &middot; Lisensi Seumur Hidup",
    p1_orig:"Rp 4.000.000", p1_main:"Rp 2.000.000", p1_sub:"atau <strong>$135 USD</strong> &middot; Lisensi Seumur Hidup",
    p2_orig:"Rp 3.000.000", p2_main:"Rp 1.500.000", p2_sub:"atau <strong>$99 USD</strong> &middot; Lisensi Seumur Hidup",
    p3_orig:"Rp 1.599.000", p3_main:"Rp 799.000", p3_sub:"atau <strong>$55 USD</strong> &middot; Lisensi Seumur Hidup",
    p4_orig:"Rp 1.300.000", p4_main:"Rp 650.000", p4_sub:"atau <strong>$45 USD</strong> &middot; Lisensi Seumur Hidup",
    p5_orig:"Rp 1.000.000", p5_main:"Rp 500.000", p5_sub:"atau <strong>$35 USD</strong> &middot; Lisensi Seumur Hidup",
    p6_orig:"Rp 800.000", p6_main:"Rp 400.000", p6_sub:"atau <strong>$28 USD</strong> &middot; Lisensi Seumur Hidup",
    p7_orig:"Rp 200.000", p7_main:"Rp 100.000", p7_sub:"atau <strong>$7 USD</strong> &middot; Lisensi Seumur Hidup",
    p8_orig:"Rp 100.000", p8_main:"Rp 50.000", p8_sub:"atau <strong>$3.5 USD</strong> &middot; Lisensi Seumur Hidup",
    p9_orig:"Rp 1.300.000", p9_main:"Rp 650.000", p9_sub:"atau <strong>$45 USD</strong> &middot; Lisensi Seumur Hidup",
    p10_orig:"Rp 1.000.000", p10_main:"Rp 500.000", p10_sub:"atau <strong>$35 USD</strong> &middot; Lisensi Seumur Hidup",
    p11_orig:"Rp 1.599.000", p11_main:"Rp 799.000", p11_sub:"atau <strong>$55 USD</strong> &middot; Lisensi Seumur Hidup",
    p12_orig:"Rp 800.000", p12_main:"Rp 400.000", p12_sub:"atau <strong>$28 USD</strong> &middot; Lisensi Seumur Hidup",
    p13_orig:"Rp 3.000.000", p13_main:"Rp 1.500.000", p13_sub:"atau <strong>$99 USD</strong> &middot; Lisensi Seumur Hidup",
    ind_kicker:"ALAT CUSTOM MT5 PROFESIONAL", ind_title:"KATALOG INDIKATOR MT5 PRO",
    ind_sub:"13 Indikator SMC, Order Block, Divergensi, Volume Profile, dan HUD Dashboard profesional mulai Rp 50.000 untuk trader manual dengan opsi pembayaran lokal &amp; global.",
    ind1_desc:"Otomatis memetakan zona Order Block institusi, Fair Value Gap (FVG), Break of Structure (BOS), dan Change of Character (CHoCH).",
    ind2_desc:"Sinyal panah Buy/Sell Non-Repaint murni pada kelelahan tren dan konfirmasi divergensi volume.",
    ind3_desc:"Otomatis menggambar zona Supply dan Demand baru dengan rasio Risk-to-Reward tinggi untuk entry terstruktur.",
    ind4_desc:"Deteksi otomatis real-time divergensi regular dan hidden pada RSI &amp; MACD untuk konfirmasi reversal probabilitas tinggi.",
    ind5_desc:"Scanner multi-timeframe kompak yang menampilkan konfluensi tren arah dari M1 hingga D1 dalam satu dashboard terpadu.",
    ind6_desc:"Kalkulator level Support &amp; Resistance dinamis yang memplot node swing institusional fraktal kunci dan target breakout.",
    ind7_desc:"HUD on-chart yang menampilkan hitungan mundur penutupan candle, monitoring spread broker live, dan latensi ping eksekusi server.",
    ind8_desc:"Visualisasi Volume Profile lengkap dengan VWAP dan band standar deviasi untuk identifikasi zona nilai institusional.",
    ind9_desc:"Suite konsep ICT lengkap: Fair Value Gap otomatis, Market Structure Shift, Optimal Trade Entry (OTE), dan killzone session.",
    ind10_desc:"Scanner Bollinger Squeeze non-repaint dengan alert RSI multi-TF untuk menangkap momen ledakan volatilitas.",
    ind11_desc:"Fibonacci Extension otomatis yang menggambar level 23.6% hingga 4.236% dari swing high/low terbaru tanpa input manual.",
    ind12_desc:"Overlay sesi pasar London, New York, dan Asia dengan killzone visual untuk timing entry optimal berdasarkan likuiditas.",
    ind13_desc:"Smart Pivot Points dan Central Pivot Range (CPR) harian/mingguan dengan level S1-S3 dan R1-R3 otomatis.",
    ind1_orig:"Rp 900.000", ind1_main:"Rp 450.000", ind1_sub:"atau <strong>$30 USD</strong> &middot; Lisensi Seumur Hidup",
    ind2_orig:"Rp 750.000", ind2_main:"Rp 375.000", ind2_sub:"atau <strong>$25 USD</strong> &middot; Lisensi Seumur Hidup",
    ind3_orig:"Rp 600.000", ind3_main:"Rp 300.000", ind3_sub:"atau <strong>$20 USD</strong> &middot; Lisensi Seumur Hidup",
    ind4_orig:"Rp 400.000", ind4_main:"Rp 200.000", ind4_sub:"atau <strong>$14 USD</strong> &middot; Lisensi Seumur Hidup",
    ind5_orig:"Rp 300.000", ind5_main:"Rp 150.000", ind5_sub:"atau <strong>$10 USD</strong> &middot; Lisensi Seumur Hidup",
    ind6_orig:"Rp 200.000", ind6_main:"Rp 100.000", ind6_sub:"atau <strong>$7 USD</strong> &middot; Lisensi Seumur Hidup",
    ind7_orig:"Rp 100.000", ind7_main:"Rp 50.000", ind7_sub:"atau <strong>$3.5 USD</strong> &middot; Lisensi Seumur Hidup",
    ind8_orig:"Rp 600.000", ind8_main:"Rp 300.000", ind8_sub:"atau <strong>$20 USD</strong> &middot; Lisensi Seumur Hidup",
    ind9_orig:"Rp 500.000", ind9_main:"Rp 250.000", ind9_sub:"atau <strong>$17 USD</strong> &middot; Lisensi Seumur Hidup",
    ind10_orig:"Rp 300.000", ind10_main:"Rp 150.000", ind10_sub:"atau <strong>$10 USD</strong> &middot; Lisensi Seumur Hidup",
    ind11_orig:"Rp 250.000", ind11_main:"Rp 125.000", ind11_sub:"atau <strong>$8 USD</strong> &middot; Lisensi Seumur Hidup",
    ind12_orig:"Rp 200.000", ind12_main:"Rp 100.000", ind12_sub:"atau <strong>$7 USD</strong> &middot; Lisensi Seumur Hidup",
    ind13_orig:"Rp 150.000", ind13_main:"Rp 75.000", ind13_sub:"atau <strong>$5 USD</strong> &middot; Lisensi Seumur Hidup",
    pkg_kicker:"PAKET LENGKAP YANG DAPAT DIKIRIM", pkg_title:"APA YANG ANDA DAPATKAN", pkg_sub:"Bukan sekadar file program, Anda menerima paket ekosistem trading terstruktur siap pakai.",
    pkg_1_t:"File Murni .EX5 (MT5 Native)", pkg_1_d:"Compiled binary original siap dimasukkan ke folder Experts MT5.",
    pkg_2_t:"Lifetime Permanent License", pkg_2_d:"Lisensi permanen tanpa biaya langganan bulanan berulang.",
    pkg_3_t:"Panduan Instalasi (PDF &amp; Video)", pkg_3_d:"Tutorial ramah pemula dari pasang hingga aktivasi dalam 5 menit.",
    pkg_4_t:"Preset Setting File (.SET)", pkg_4_d:"Konfigurasi terkalibrasi untuk Gold, Forex mayor, dan indeks.",
    pkg_5_t:"Kebijakan Update Algoritma Gratis", pkg_5_d:"Pembaruan perbaikan bug dan kalibrasi algoritma gratis selamanya.",
    pkg_6_t:"VIP AnyDesk &amp; Telegram Support", pkg_6_d:"Bantuan remote setting via AnyDesk bagi pemula serta konsultasi strategi.",
    faq_kicker:"BASIS PENGETAHUAN &amp; KEBIJAKAN RISIKO", faq_title:"PERTANYAAN UMUM &amp; DISCLAIMER", faq_sub:"Penjelasan transparan tentang cara kerja EA, risiko trading, dan batasan tanggung jawab hukum.",
    faq1_q:"<span class=\\'text-emerald-400 mr-2\\'>🤖</span> Apa itu Robot Expert Advisor (EA) MT5 dan bagaimana cara kerjanya?",
    faq1_a:"<strong>Robot Expert Advisor (EA)</strong> adalah program perangkat lunak algoritma yang dipasang di MetaTrader 5 (MT5). EA bekerja otomatis 24/5 menganalisis harga, menghitung lot, membuka posisi Buy/Sell, dan memasang TP/SL secara otomatis tanpa intervensi emosi manusia.",
    faq2_q:"<span class=\\'text-amber-400 mr-2\\'>⚠️</span> Apakah Robot EA ini selalu profit dan ada jaminan keuntungan?",
    faq2_a:"<p class=\\'mb-2\\'><strong>TIDAK. Robot EA TIDAK SELALU PROFIT, dan kami SAMA SEKALI TIDAK MENJAMIN PROFIT.</strong></p><p class=\\'text-zinc-400 mb-2\\'>Trading memiliki risiko fluktuasi harga yang tinggi. Hasil backtest tidak menjamin keuntungan di masa mendatang.</p><p class=\\'text-amber-300 font-semibold\\'>Gunakanlah selalu dana dingin yang siap Anda tanggung risikonya.</p>",
    faq3_q:"<span class=\\'text-rose-400 mr-2\\'>⚖️</span> Bagaimana jika terjadi kerugian (Loss) pada akun trading saya?",
    faq3_a:"<p class=\\'mb-2\\'><strong>Segala kerugian finansial, margin call, atau drawdown sepenuhnya adalah TANGGUNG JAWAB PRIBADI ANDA SEBAGAI TRADER.</strong></p><p class=\\'text-zinc-400 mb-2\\'>Kami bertindak murni sebagai pengembang software. Kami <strong>BUKAN pengelola dana, bukan penasihat keuangan, dan TIDAK BERTANGGUNG JAWAB</strong> atas kerugian akun, gangguan broker/internet, atau kesalahan pemilihan lot.</p><p class=\\'text-zinc-400\\'>Dengan membeli software ini, Anda menyatakan telah membaca dan menyetujui seluruh risiko perdagangan.</p>",
    faq4_q:"<span class=\\'text-purple-400 mr-2\\'>📊</span> Apa perbedaan Robot EA dengan Indikator MT5?",
    faq4_a:"<strong>Robot EA</strong> adalah sistem otomatis penuh yang membuka dan menutup posisi sendiri. <strong>Indikator Custom</strong> adalah alat bantu visual (Order Block, Supply &amp; Demand, sinyal panah) untuk membantu trading manual.",
    faq5_q:"<span class=\\'text-blue-400 mr-2\\'>🌐</span> Apakah saya harus memakai VPS?",
    faq5_a:"Untuk Robot EA, sangat disarankan menggunakan <strong>VPS Windows</strong> agar EA berjalan 24 jam nonstop tanpa laptop Anda harus menyala. Rekomendasi VPS murah berkualitas ($3-$5/bulan) tersedia di dalam panduan instalasi.",
    disc_title:"PEMBERITAHUAN RESMI TENTANG RISIKO &amp; TANGGUNG JAWAB",
    disc_desc:"Trading Forex, Komoditas (Emas/XAUUSD), dan Indeks membawa tingkat risiko kerugian finansial yang signifikan. Produk software kami disediakan apa adanya (\\'as-is\\') sebagai alat bantu teknologi analisis. Anda bertanggung jawab penuh atas segala hasil, untung, maupun rugi pada portofolio Anda.",
    m_lbl_trades:"Total Trades", m_lbl_period:"Periode Pengujian:", m_lbl_desc:"Deskripsi Algoritma:", m_lbl_inc:"Paket Yang Anda Terima:",
    ft_rights:"&copy; 2026 AEMETH TRADER. Hak Cipta Dilindungi.", ft_connect:"HUBUNGI KAMI"
  },
  en: {
    nav_sub_brand:"SYSTEMATIC MT5 LAB",
    top_vip_badge:"VIP SERVICE",
    top_service:"Free Setup Assistance via AnyDesk / TeamViewer &bull; Guaranteed Instant .EX5 Delivery",
    top_tele:"TELEGRAM CONSULTATION",
    nav_perf:"PERFORMANCE", nav_why:"WHY AEMETH?", nav_bundle:"BUNDLE PACKAGES", nav_ea:"STANDALONE EA", nav_ind:"INDICATORS", nav_inc:"INCLUSIONS", nav_faq:"FAQ", nav_catalog:"EA CATALOG",
    nav_status:"EA Status: Active &amp; Verified",
    hero_kicker:"SYSTEMATIC ALGORITHMIC TRADING TOOLS",
    hero_title:"QUANTUM<br/>TRADER",
    hero_desc:"Rule-based quantitative MT5 trading systems. Low-latency native MQL5 algorithms, bounded position risk management, and transparent historical backtests.",
    hero_btn_bundle:"BUNDLE PACKAGES", hero_btn_ea:"STANDALONE EA", hero_btn_ind:"PRO INDICATORS",
    hero_pay_label:"PAYMENT METHODS:",
    hero_mockup_routing:"Order Routing: MT5 Native C++",
    hero_prop_tag:"PROP FIRM COMPATIBLE", hero_prop_title:"RISK BOUNDED MODEL",
    perf_kicker:"VERIFIED AUDIT BENCHMARK", perf_title:"PERFORMANCE SNAPSHOT",
    perf_pair:"XAUUSD &middot; MT5 &middot; Backtest",
    stat_pf:"PROFIT FACTOR", stat_win:"WIN RATE", stat_dd:"MAX DRAWDOWN",
    perf_context:"<strong>Results based on:</strong> AEMETH Quantum Neural Master v4.0, Jan 2024&ndash;Dec 2025, M15 Timeframe (Exness Pro Server, 99.9% Tick Quality). Past performance does not guarantee future results.",
    perf_disc:"*Simulated historical testing under fixed risk parameters.",
    why_kicker:"SYSTEMATIC ARCHITECTURE", why_title:"WHY CHOOSE AEMETH?",
    why_sub:"Built with systematic quantitative principles and disciplined exposure control.",
    w1t:"Rule-Based Execution", w1d:"Eliminates subjective emotional bias. Purely rule-based execution on quantitative parameters.",
    w2t:"Automated Risk Management", w2d:"Automated risk management designed to eliminate excessive exposure. Hard Stop Loss on every entry and daily drawdown circuit breakers.",
    w3t:"MT5 Native C++", w3d:"Low-latency native execution for MetaTrader 5 ensuring optimal memory efficiency and ECN broker routing.",
    w4t:"Lifetime License", w4d:"One-time permanent ownership with no monthly recurring subscription fees.",
    w5t:"Instant Delivery", w5d:"Pure .ex5 binary and configuration files delivered to your inbox within seconds of confirmed payment.",
    bundle_kicker:"ALL-IN-ONE VALUE SUITES", bundle_title:"MT5 BUNDLE PACKAGES",
    bundle_sub:"Get complete suites combining multi-strategy automated EA robots + pro non-repaint indicators with up to 50% discount. Lifetime permanent licenses.",
    b1_badge:"INSTITUTIONAL FLAGSHIP",
    b1_hot_tag:"⭐ BEST RECOMMENDED FOR LARGE ACCOUNTS &amp; PROP FIRMS",
    b1_save_tag:"SAVE $199 USD",
    b1_title:"AEMETH MASTER BUNDLE 6 Tools",
    b1_tools_line:"4 MT5 Robot EAs + 2 Pro Indicators — Lifetime Access",
    bundle_desc:"Get the complete suite: 4 institutional MT5 Expert Advisors + 2 MT5 Pro non-repaint indicators. An all-in-one arsenal for personal growth, rapid scalping, and Prop Firm challenge evaluations.",
    b1_inc_header:"INCLUDED 6 ARSENAL TOOLS:",
    b1_vip_bonus_title:"EXCLUSIVE VIP PRIVILEGES:",
    b1_free_tag:"INCLUDED FREE",
    b1_bonus_1:"Priority 1-on-1 Remote Setup via AnyDesk / TeamViewer",
    b1_bonus_2:"Custom Low-Drawdown Setfiles for Prop Firm Challenges",
    b1_bonus_3:"VIP Telegram Group Access &amp; Lifetime Algorithm Upgrades",
    b1_urgency:"ONLY 5 LICENSES LEFT WITH VIP REMOTE SETUP INCLUDED",
    bundle_discount_badge:"50% VIP DISCOUNT",
    price_orig_b1:"$398 USD",
    price_main_b1:"$199 USD",
    price_sub_b1:"or ~<strong>Rp 3.000.000 IDR</strong> &middot; Lifetime Permanent Access (6 Tools)",
    b2_badge:"#1 BEST SELLER — 14 TOOLS",
    b2_seller_tag:"🏆 MOST POPULAR SUITE (14 TOOLS ALL-IN-ONE)",
    b2_rate_tag:"ONLY $12 / TOOL! (74% SAVINGS)",
    b2_title:"AEMETH MEGA BUNDLE 14 Tools v2.0",
    b2_tools_line:"10 MT5 Robot EAs + 4 Pro Indicators — Lifetime Access",
    bundle2_desc:"The ultimate all-inclusive suite from AEMETH TRADER. Get 10 automated MT5 EAs (Gold, Forex, Indices, Prop Firm, Cent &amp; HFT) plus 4 MT5 Pro non-repaint indicators for manual trading. Includes free remote AnyDesk installation support.",
    b2_inc_header:"COMPLETE 14 MT5 TOOLS INVENTORY:",
    b2_val_calc_lbl:"Total Retail Value (14 Tools):",
    b2_val_calc_orig:"$650 USD+",
    b2_val_save_lbl:"Your Net Savings:",
    b2_val_save_val:"+$485 USD (74% SAVINGS)",
    b2_social_proof:"98% OF TRADERS CHOOSE THIS BUNDLE FOR FULL ARSENAL",
    bundle2_discount_badge:"50% DISCOUNT",
    price_orig_b2:"$330 USD",
    price_main_b2:"$165 USD",
    price_sub_b2:"or ~<strong>Rp 2.500.000 IDR</strong> &middot; Lifetime Permanent Access (14 Tools)",
    b4_badge:"⚡ STARTER BUNDLE — 11 TOOLS",
    b4_title:"AEMETH STARTER BUNDLE 5 EA + 6 Ind",
    b4_tools_line:"5 MT5 Robot EAs + 6 Pro Indicators — Lifetime Access",
    bundle4_desc:"The complete starter suite from AEMETH TRADER. Get 5 automated MT5 EAs (London Breakout, Grid Momentum, News Armor, Night Scalper, Swing Multi) plus 6 MT5 Pro indicators for manual trading. Includes free setup guide.",
    bundle4_discount_badge:"50% DISCOUNT",
    price_orig_b4:"$260 USD",
    price_main_b4:"$130 USD",
    price_sub_b4:"or ~<strong>Rp 2.000.000 IDR</strong> &middot; Lifetime Permanent Access (11 Tools)",
    b3_badge:"🔥 HYBRID BUNDLE — 11 TOOLS",
    b3_title:"AEMETH HYBRID SUITE 3 EA + 8 Ind",
    b3_tools_line:"3 MT5 Robot EAs + 8 Pro Indicators — Lifetime Access",
    bundle3_desc:"The optimal synergy between full automation and manual charting. Get 3 proven MT5 EAs (Gold Scalper, Trend Pulse, Micro Cent) plus all 8 MT5 Pro non-repaint indicators for institutional charting precision.",
    bundle3_discount_badge:"50% DISCOUNT",
    price_orig_b3:"$198 USD",
    price_main_b3:"$99 USD",
    price_sub_b3:"or ~<strong>Rp 1.500.000 IDR</strong> &middot; Lifetime Permanent Access (11 Tools)",
    cat_kicker:"STANDALONE ALGORITHMS", cat_title:"STANDALONE MT5 ROBOT EA CATALOG",
    cat_sub:"Select standalone EA robots matching your trading capital and style. 14 verified algorithms starting from $3.50 to $265 USD Flagship.",
    lbl_price:"FILTER BY PRODUCT PRICE:", hint_price:"Filter by software retail price",
    f_all:"ALL (14)", f_100k:"&le; $7 (100K IDR)", f_500k:"&le; $35 (500K IDR)", f_1m:"&le; $70 (1M IDR)", f_vip:"&#x1F451; &gt; $70 (VIP)",
    lbl_cat:"STRATEGY CATEGORY:", hint_cat:"Select trading robot style",
    c_all:"ALL (14)", c_flagship:"&#x1F451; FLAGSHIP", c_hft:"&#x26A1; HIGH-FREQUENCY",
    c_risk:"&#x1F6E1; RISK MANAGEMENT", c_trend:"&#x1F4C8; TREND SYSTEM", c_gold:"&#x1F947; GOLD SCALPING", c_starter:"&#x1F331; STARTER &amp; CENT", c_budget:"&#x1F3F7; BUDGET (&le; $7)",
    empty_filter:"No trading robots match the selected filters.",
    lbl_pf:"Profit Factor", lbl_win:"Win Rate", lbl_dd:"Max DD",
    lbl_backtest_note:"Backtest Data &bull; Past performance does not guarantee future results",
    lbl_min_cap:"Min. Capital:",
    btn_detail:"VIEW DETAILS 📄",
    btn_pay_qris:"QRIS / BANK TRANSFER", btn_pay_global:"PAYPAL / CARD / CRYPTO", btn_pay_tg:"P2P CRYPTO (USDT)",
    disc_badge:"50% Launch Price",
    cap1:"$500+ (10M IDR)", cap2:"$300+ (5M IDR)", cap3:"$100+ (1M IDR)", cap4:"$50 (500K IDR)",
    cap5:"$10 Cent/Std (100K IDR)", cap6:"$10 Cent (100K IDR)", cap7:"$5 Cent (50K IDR)", cap8:"$5 Cent (50K IDR)",
    cap9:"$100+ (1M IDR)", cap10:"$50 (500K IDR)", cap11:"$100+ (1M IDR)", cap12:"$10 Cent (100K IDR)", cap13:"$300+ (5M IDR)",
    cap14:"$1,000+ ($50K-$200K Prop Firm)",
    p14_orig:"$530 USD", p14_main:"$265 USD", p14_sub:"or ~<strong>Rp 4.000.000 IDR</strong> &middot; Lifetime License",
    p1_orig:"$270 USD", p1_main:"$135 USD", p1_sub:"or ~<strong>Rp 2.000.000 IDR</strong> &middot; Lifetime License",
    p2_orig:"$198 USD", p2_main:"$99 USD", p2_sub:"or ~<strong>Rp 1.500.000 IDR</strong> &middot; Lifetime License",
    p3_orig:"$110 USD", p3_main:"$55 USD", p3_sub:"or ~<strong>Rp 799.000 IDR</strong> &middot; Lifetime License",
    p4_orig:"$90 USD", p4_main:"$45 USD", p4_sub:"or ~<strong>Rp 650.000 IDR</strong> &middot; Lifetime License",
    p5_orig:"$70 USD", p5_main:"$35 USD", p5_sub:"or ~<strong>Rp 500.000 IDR</strong> &middot; Lifetime License",
    p6_orig:"$56 USD", p6_main:"$28 USD", p6_sub:"or ~<strong>Rp 400.000 IDR</strong> &middot; Lifetime License",
    p7_orig:"$14 USD", p7_main:"$7 USD", p7_sub:"or ~<strong>Rp 100.000 IDR</strong> &middot; Lifetime License",
    p8_orig:"$7 USD", p8_main:"$3.50 USD", p8_sub:"or ~<strong>Rp 50.000 IDR</strong> &middot; Lifetime License",
    p9_orig:"$90 USD", p9_main:"$45 USD", p9_sub:"or ~<strong>Rp 650.000 IDR</strong> &middot; Lifetime License",
    p10_orig:"$70 USD", p10_main:"$35 USD", p10_sub:"or ~<strong>Rp 500.000 IDR</strong> &middot; Lifetime License",
    p11_orig:"$110 USD", p11_main:"$55 USD", p11_sub:"or ~<strong>Rp 799.000 IDR</strong> &middot; Lifetime License",
    p12_orig:"$56 USD", p12_main:"$28 USD", p12_sub:"or ~<strong>Rp 400.000 IDR</strong> &middot; Lifetime License",
    p13_orig:"$198 USD", p13_main:"$99 USD", p13_sub:"or ~<strong>Rp 1.500.000 IDR</strong> &middot; Lifetime License",
    ind_kicker:"PROFESSIONAL MT5 CUSTOM TOOLS", ind_title:"MT5 PRO INDICATORS CATALOG",
    ind_sub:"13 professional SMC, Order Block, Divergence, Volume Profile, and HUD tools starting from $3.50 with local &amp; global payment support.",
    ind1_desc:"Automatically maps institutional Order Blocks, Fair Value Gaps (FVG), Break of Structure (BOS), and Change of Character (CHoCH).",
    ind2_desc:"Pure Non-Repaint Buy/Sell signal arrows on trend exhaustion and volume divergence confirmation.",
    ind3_desc:"Automatically draws fresh Supply and Demand zones with high Risk-to-Reward ratios for structured entries.",
    ind4_desc:"Real-time automated detection of regular and hidden divergences across RSI &amp; MACD for high-probability reversal confirmation.",
    ind5_desc:"Compact multi-timeframe scanner displaying directional trend confluence from M1 to D1 in a single unified dashboard.",
    ind6_desc:"Dynamic Support and Resistance level calculator plotting key institutional fractal swing nodes and breakout targets.",
    ind7_desc:"On-chart HUD displaying candle closing countdown, live broker spread monitoring, and server execution ping latency.",
    ind8_desc:"Full Volume Profile visualization with VWAP and standard deviation bands for institutional value zone identification.",
    ind9_desc:"Complete ICT concepts suite: automated Fair Value Gap, Market Structure Shift, Optimal Trade Entry (OTE), and session killzones.",
    ind10_desc:"Non-repaint Bollinger Squeeze scanner with multi-TF RSI alert to catch volatility explosion moments.",
    ind11_desc:"Automatic Fibonacci Extension drawing levels from 23.6% to 4.236% from latest swing high/low without manual input.",
    ind12_desc:"London, New York, and Asia session market overlay with visual killzones for optimal entry timing based on liquidity.",
    ind13_desc:"Smart Pivot Points and Central Pivot Range (CPR) daily/weekly with automatic S1-S3 and R1-R3 levels.",
    ind1_orig:"$60 USD", ind1_main:"$30 USD", ind1_sub:"or ~<strong>Rp 450.000 IDR</strong> &middot; Lifetime License",
    ind2_orig:"$50 USD", ind2_main:"$25 USD", ind2_sub:"or ~<strong>Rp 375.000 IDR</strong> &middot; Lifetime License",
    ind3_orig:"$40 USD", ind3_main:"$20 USD", ind3_sub:"or ~<strong>Rp 300.000 IDR</strong> &middot; Lifetime License",
    ind4_orig:"$28 USD", ind4_main:"$14 USD", ind4_sub:"or ~<strong>Rp 200.000 IDR</strong> &middot; Lifetime License",
    ind5_orig:"$20 USD", ind5_main:"$10 USD", ind5_sub:"or ~<strong>Rp 150.000 IDR</strong> &middot; Lifetime License",
    ind6_orig:"$14 USD", ind6_main:"$7 USD", ind6_sub:"or ~<strong>Rp 100.000 IDR</strong> &middot; Lifetime License",
    ind7_orig:"$7 USD", ind7_main:"$3.50 USD", ind7_sub:"or ~<strong>Rp 50.000 IDR</strong> &middot; Lifetime License",
    ind8_orig:"$40 USD", ind8_main:"$20 USD", ind8_sub:"or ~<strong>Rp 300.000 IDR</strong> &middot; Lifetime License",
    ind9_orig:"$34 USD", ind9_main:"$17 USD", ind9_sub:"or ~<strong>Rp 250.000 IDR</strong> &middot; Lifetime License",
    ind10_orig:"$20 USD", ind10_main:"$10 USD", ind10_sub:"or ~<strong>Rp 150.000 IDR</strong> &middot; Lifetime License",
    ind11_orig:"$16 USD", ind11_main:"$8 USD", ind11_sub:"or ~<strong>Rp 125.000 IDR</strong> &middot; Lifetime License",
    ind12_orig:"$14 USD", ind12_main:"$7 USD", ind12_sub:"or ~<strong>Rp 100.000 IDR</strong> &middot; Lifetime License",
    ind13_orig:"$10 USD", ind13_main:"$5 USD", ind13_sub:"or ~<strong>Rp 75.000 IDR</strong> &middot; Lifetime License",
    pkg_kicker:"COMPLETE DELIVERABLE PACKAGE", pkg_title:"WHAT YOUR PURCHASE INCLUDES", pkg_sub:"More than standalone files, you receive a production-grade automated trading ecosystem.",
    pkg_1_t:"Pure .EX5 Binaries (MT5 Native)", pkg_1_d:"Clean compiled original binary ready to install into MT5 Experts directory.",
    pkg_2_t:"Lifetime Permanent License", pkg_2_d:"Permanent license with zero recurring monthly subscription fees.",
    pkg_3_t:"Installation Guide (PDF &amp; Video)", pkg_3_d:"Beginner-friendly step-by-step setup in under 5 minutes.",
    pkg_4_t:"Pre-calibrated Preset Files (.SET)", pkg_4_d:"Calibrated configurations for Gold, major Forex pairs, and indices.",
    pkg_5_t:"Free Algorithm Update Policy", pkg_5_d:"Lifetime free bug fixes, patches, and algorithmic recalibrations.",
    pkg_6_t:"VIP AnyDesk &amp; Telegram Support", pkg_6_d:"1-on-1 remote setup assistance via AnyDesk and strategy consultation.",
    faq_kicker:"KNOWLEDGE BASE &amp; RISK POLICY", faq_title:"FAQ &amp; OFFICIAL DISCLAIMER", faq_sub:"Transparent disclosures regarding EA operations, financial risk, and limitation of liability.",
    faq1_q:"<span class=\\'text-emerald-400 mr-2\\'>🤖</span> What is an MT5 Expert Advisor (EA) and how does it work?",
    faq1_a:"An <strong>Expert Advisor (EA)</strong> is automated algorithmic software installed inside MetaTrader 5. It operates 24/5 analyzing price action, calculating position size, executing Buy/Sell orders, and managing TP/SL without human emotion.",
    faq2_q:"<span class=\\'text-amber-400 mr-2\\'>⚠️</span> Does this EA always make a profit? Is profit guaranteed?",
    faq2_a:"<p class=\\'mb-2\\'><strong>NO. The EA DOES NOT ALWAYS PROFIT in all conditions. We DO NOT GUARANTEE ANY PROFIT.</strong></p><p class=\\'text-zinc-400 mb-2\\'>Past backtest results cannot guarantee future live market performance.</p><p class=\\'text-amber-300 font-semibold\\'>Always trade with risk capital you are prepared to lose.</p>",
    faq3_q:"<span class=\\'text-rose-400 mr-2\\'>⚖️</span> What if my trading account incurs a loss?",
    faq3_a:"<p class=\\'mb-2\\'><strong>Any financial loss, margin call, or drawdown is SOLELY YOUR PERSONAL RESPONSIBILITY AS A TRADER.</strong></p><p class=\\'text-zinc-400 mb-2\\'>We are <strong>NOT financial advisors or fund managers, and WE ARE NOT LIABLE</strong> for trading outcomes or account losses.</p><p class=\\'text-zinc-400\\'>By purchasing this software, you acknowledge and accept all trading risks.</p>",
    faq4_q:"<span class=\\'text-purple-400 mr-2\\'>📊</span> What is the difference between an EA Robot and a Custom Indicator?",
    faq4_a:"An <strong>EA Robot</strong> is a fully automated trading system. A <strong>Custom Indicator</strong> is a visual analytical tool (Order Blocks, Supply &amp; Demand, signal arrows) to assist manual trading.",
    faq5_q:"<span class=\\'text-blue-400 mr-2\\'>🌐</span> Do I need a VPS?",
    faq5_a:"For automated EAs, a <strong>Windows VPS</strong> is highly recommended so the EA runs 24/5 without your PC staying on. Inexpensive VPS options ($3-$5/month) are covered in our setup guide.",
    disc_title:"OFFICIAL NOTICE ON RISK &amp; LIMITATION OF LIABILITY",
    disc_desc:"Trading Forex, Commodities (Gold/XAUUSD), and Indices involves significant risk of loss. Our software is provided \\'as-is\\' for technical analysis assistance. You assume full responsibility for all trading outcomes and portfolio performance.",
    m_lbl_trades:"Total Trades", m_lbl_period:"Tested Period:", m_lbl_desc:"Algorithm Description:", m_lbl_inc:"What You Receive:",
    ft_rights:"&copy; 2026 AEMETH TRADER. All Rights Reserved.", ft_connect:"LET\\'S CONNECT"
  }
};

let priceFilter = "all";
let catFilter = "all";

function setPrice(tier, btn) {
  priceFilter = tier;
  document.querySelectorAll(".price-btn").forEach(b => {
    b.className = "price-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer";
  });
  btn.className = "price-btn active whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-bold font-mono border border-emerald-500 text-emerald-300 bg-emerald-950/50 transition-all cursor-pointer";
  applyFilters();
}

function setCategory(cat, btn) {
  catFilter = cat;
  document.querySelectorAll(".cat-btn").forEach(b => {
    b.className = "cat-btn whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-mono border border-zinc-700 text-zinc-400 hover:border-zinc-500 transition-all cursor-pointer";
  });
  btn.className = "cat-btn active whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-bold font-mono border border-emerald-500 text-emerald-300 bg-emerald-950/50 transition-all cursor-pointer";
  applyFilters();
}

function applyFilters() {
  const cards = document.querySelectorAll("#catalog-grid .product-card");
  let visibleCount = 0;
  cards.forEach(card => {
    const cat = card.getAttribute("data-category") || "";
    const price = parseInt(card.getAttribute("data-price") || "0");
    let showPrice = true;
    if (priceFilter === "100k") showPrice = price <= 100000;
    else if (priceFilter === "500k") showPrice = price <= 500000;
    else if (priceFilter === "1m") showPrice = price <= 1000000;
    else if (priceFilter === "vip") showPrice = price > 1000000;
    const showCat = catFilter === "all" || cat === catFilter;
    const show = showPrice && showCat;
    card.style.display = show ? "" : "none";
    if (show) visibleCount++;
  });
  const emptyEl = document.getElementById("filter-empty");
  if (emptyEl) emptyEl.classList.toggle("hidden", visibleCount > 0);
}

function toggleFaq(btn) {
  const card = btn.closest(".bg-cardDark") || btn.parentElement;
  const answer = card.querySelector(".faq-answer");
  const chevron = btn.querySelector(".faq-chevron");
  if (!answer) return;
  const isOpen = answer.classList.contains("open");
  if (isOpen) {
    answer.classList.remove("open");
    answer.style.display = "none";
    if (chevron) chevron.classList.remove("rotate");
  } else {
    answer.classList.add("open");
    answer.style.display = "block";
    if (chevron) chevron.classList.add("rotate");
  }
}

const products = {
  "apex-titan": {
    name: "AEMETH Apex Neural Titan Ultra v5.0",
    tag: "👑 ULTRA INSTITUTIONAL", color: "#f59e0b",
    pair: "XAUUSD / US30 / NAS100", tf: "M5 / M15",
    strategy_id: "Deep Neural Machine Learning + Cross-Asset Arbitrage",
    strategy_en: "Deep Neural Machine Learning + Cross-Asset Arbitrage",
    pf: "6.85", wr: "92.40%", dd: "3.10%", trades: "3,840", period: "Jan 2024 – Des 2025",
    desc_id: "Paket EA satuan kasta tertinggi dari AEMETH TRADER. Algoritma kuantitatif canggih berbasis arsitektur deep neural network yang membaca aliran likuiditas instrumen volatilitas tinggi (Emas & Indeks AS). Dilengkapi manajemen margin otomatis, perlindungan drawdown harian ketat, serta garansi kelayakan evaluasi akun Prop Firm $100k-$200k.",
    desc_en: "The pinnacle standalone EA package by AEMETH TRADER. Advanced quantitative algorithm built on deep neural network architecture reading high-volatility liquidity flows (Gold & US Indices). Features automated margin management, strict daily drawdown protection, and verified compliance for $100k-$200k Prop Firm accounts.",
    includes_id: [
      "File Binary AEMETH Apex Neural Titan Ultra v5.0 (.ex5)",
      "Setfile Preset Institusional Khusus Prop Firm $100K - $200K",
      "Prioritas VIP 1-on-1 Remote Setup via AnyDesk / TeamViewer",
      "Panduan Lengkap Optimalisasi Arsitektur Kuantitatif (PDF)",
      "Akses Seumur Hidup Grup VIP Telegram & Update Rutin",
      "Lisensi Permanen Seumur Hidup (Tanpa Iuran Bulanan)"
    ],
    includes_en: [
      "AEMETH Apex Neural Titan Ultra v5.0 Binary (.ex5)",
      "Institutional Prop Firm Preset Bundle ($100K - $200K)",
      "Priority 1-on-1 AnyDesk / TeamViewer Remote Installation",
      "Comprehensive Quantitative Optimization Manual (PDF)",
      "Lifetime VIP Telegram Group Access & Direct Updates",
      "Permanent Lifetime License (Zero Monthly Fees)"
    ],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "neural-master": {
    name: "AEMETH Quantum Neural Master v4.0",
    tag: "👑 FLAGSHIP", color: "#f59e0b",
    pair: "XAUUSD", tf: "M15",
    strategy_id: "Adaptive Neural Scalping + Trend Follow",
    strategy_en: "Adaptive Neural Scalping + Trend Follow",
    pf: "5.91", wr: "90.16%", dd: "4.02%", trades: "2,481", period: "Jan 2024 – Dec 2025",
    desc_id: "Sistem EA MT5 institusional dengan arsitektur neural-adaptive yang mengeksekusi scalping presisi tinggi di XAUUSD. Menggabungkan konfirmasi multi-TF, filter volatilitas adaptif, dan multi-layer risk management.",
    desc_en: "Institutional MT5 EA with neural-adaptive architecture executing high-precision scalping on XAUUSD. Integrates multi-timeframe confluence, adaptive volatility filters, and multi-layer risk management.",
    includes_id: ["File AEMETH Neural Master v4.0 (.ex5)", "Input Parameter Template (.set)", "Panduan Instalasi PDF", "Panduan Set File Optimal", "Support AnyDesk 1x sesi", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Neural Master v4.0 (.ex5)", "Optimal Preset Template (.set)", "PDF Installation Guide", "Setfile Optimization Manual", "1-on-1 AnyDesk Remote Session", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "hft-multi": {
    name: "AEMETH Institutional HFT Multi v3.2",
    tag: "⚡ HIGH-FREQUENCY", color: "#06b6d4",
    pair: "EURUSD / GBPUSD", tf: "M1",
    strategy_id: "High-Frequency Tick Scalping",
    strategy_en: "High-Frequency Tick Scalping",
    pf: "4.77", wr: "87.30%", dd: "5.14%", trades: "8,920", period: "Jan 2024 – Dec 2025",
    desc_id: "Robot HFT multi-pair yang mengeksekusi puluhan order cepat per hari pada M1 dengan manajemen risiko ketat. Dirancang untuk broker ECN dengan spread rendah.",
    desc_en: "Multi-pair HFT robot executing rapid tick trades on M1 with strict algorithmic risk boundaries. Optimized for low-spread ECN brokers.",
    includes_id: ["File AEMETH HFT Multi v3.2 (.ex5)", "Input Parameter Template (.set)", "Panduan Instalasi PDF", "Rekomendasi Broker ECN", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH HFT Multi v3.2 (.ex5)", "Preset Parameter File (.set)", "PDF Installation Manual", "Recommended ECN Broker List", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "prop-shield": {
    name: "AEMETH Prop Shield v2.1",
    tag: "🛡️ RISK MANAGEMENT", color: "#f43f5e",
    pair: "All Pairs", tf: "M5",
    strategy_id: "Prop Firm Challenge Risk Manager",
    strategy_en: "Prop Firm Challenge Risk Manager",
    pf: "3.88", wr: "85.60%", dd: "3.50%", trades: "1,204", period: "Jan 2024 – Dec 2025",
    desc_id: "EA khusus dirancang untuk melewati evaluasi tantangan Prop Firm dengan circuit breaker drawdown harian otomatis dan position sizing konservatif.",
    desc_en: "EA specifically engineered to pass Prop Firm evaluation challenges with automated daily equity protection circuit breakers and conservative position sizing.",
    includes_id: ["File AEMETH Prop Shield v2.1 (.ex5)", "Input Parameter Template (.set)", "Panduan Challenge Prop Firm", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Prop Shield v2.1 (.ex5)", "Calibrated Challenge Set (.set)", "Prop Firm Evaluation Handbook", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "trend-pulse": {
    name: "AEMETH Trend Pulse v2.0",
    tag: "📈 TREND SYSTEM", color: "#8b5cf6",
    pair: "XAUUSD / Forex Major", tf: "H1",
    strategy_id: "Multi-TF Trend Following",
    strategy_en: "Multi-TF Trend Following",
    pf: "3.21", wr: "82.40%", dd: "6.80%", trades: "634", period: "Jan 2024 – Dec 2025",
    desc_id: "Sistem trend following multi-timeframe yang masuk pada pullback konfirmasi dengan konfluensi indikator EMA dan RSI. Sangat ideal untuk trader swing.",
    desc_en: "Multi-timeframe trend-following algorithm entering on confirmed pullbacks with EMA and RSI indicator confluence. Ideal for swing positions.",
    includes_id: ["File AEMETH Trend Pulse v2.0 (.ex5)", "Input Parameter Template (.set)", "Panduan Instalasi PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Trend Pulse v2.0 (.ex5)", "Preset Parameter File (.set)", "PDF Installation Guide", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "quantum-scalper": {
    name: "AEMETH Quantum Scalper Gold v1.5",
    tag: "🥇 GOLD SCALPING", color: "#eab308",
    pair: "XAUUSD", tf: "M5",
    strategy_id: "Asian Session Gold Scalper",
    strategy_en: "Asian Session Gold Scalper",
    pf: "4.12", wr: "88.50%", dd: "4.75%", trades: "3,215", period: "Jan 2024 – Dec 2025",
    desc_id: "Scalper XAUUSD khusus sesi Asia dengan filter spread adaptif dan target profit harian otomatis. Dirancang untuk modal menengah.",
    desc_en: "Dedicated Asian session XAUUSD scalper featuring dynamic spread filters and automated daily profit banking. Built for medium accounts.",
    includes_id: ["File AEMETH Quantum Scalper v1.5 (.ex5)", "Input Parameter Template (.set)", "Panduan Instalasi PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Quantum Scalper v1.5 (.ex5)", "Asian Session Setfile (.set)", "PDF Installation Guide", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "micro-cent": {
    name: "AEMETH Micro Cent Trader v1.3",
    tag: "🌱 STARTER & CENT", color: "#14b8a6",
    pair: "Any Pair", tf: "M15",
    strategy_id: "Micro Lot Cent Account Starter",
    strategy_en: "Micro Lot Cent Account Starter",
    pf: "2.95", wr: "78.20%", dd: "8.30%", trades: "1,540", period: "Jan 2024 – Dec 2025",
    desc_id: "EA ramah pemula untuk akun cent dengan modal minimal mulai $10. Sangat cocok untuk menguji sistem otomasi dengan eksposur risiko sangat minim.",
    desc_en: "Beginner-friendly cent account EA operating with minimum capital starting at $10. Perfect for exploring automated execution with low financial risk.",
    includes_id: ["File AEMETH Micro Cent v1.3 (.ex5)", "Input Parameter Template (.set)", "Panduan Akun Cent PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Micro Cent v1.3 (.ex5)", "Micro Cent Setfile (.set)", "Cent Account Setup Manual", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "budget-scalper": {
    name: "AEMETH Budget Scalper Nano v1.0",
    tag: "🏷️ BUDGET", color: "#84cc16",
    pair: "EURUSD", tf: "M1",
    strategy_id: "Nano Budget Scalper",
    strategy_en: "Nano Budget Scalper",
    pf: "2.30", wr: "74.50%", dd: "9.80%", trades: "2,100", period: "Jan 2024 – Dec 2025",
    desc_id: "EA budget terjangkau untuk trader pemula dengan modal terbatas. Scalper M1 EURUSD dengan manajemen risiko dasar yang solid.",
    desc_en: "Ultra-affordable budget EA for beginners with micro accounts. M1 EURUSD scalper equipped with core risk control logic.",
    includes_id: ["File AEMETH Budget Scalper Nano v1.0 (.ex5)", "Input Parameter Template (.set)", "Panduan Singkat PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Budget Scalper Nano v1.0 (.ex5)", "Preset Setfile (.set)", "Quick Setup PDF", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "mini-grid": {
    name: "AEMETH Mini Grid Breaker v1.0",
    tag: "🏷️ BUDGET", color: "#94a3b8",
    pair: "Any Pair", tf: "M5",
    strategy_id: "Mini Grid System",
    strategy_en: "Mini Grid System",
    pf: "2.10", wr: "72.30%", dd: "11.50%", trades: "1,870", period: "Jan 2024 – Dec 2025",
    desc_id: "Sistem grid mini untuk akun cent dengan harga paling terjangkau. Pilihan tepat sebagai robot pertama untuk memahami sistem trading otomatis.",
    desc_en: "Most accessible mini grid algorithm for cent accounts. An excellent starter tool to learn automated trading mechanics safely.",
    includes_id: ["File AEMETH Mini Grid Breaker v1.0 (.ex5)", "Input Parameter Template (.set)", "Panduan Singkat PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Mini Grid Breaker v1.0 (.ex5)", "Preset Setfile (.set)", "Quick Setup PDF", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "london-breakout": {
    name: "AEMETH London Breakout Rider v1.2",
    tag: "📈 TREND SYSTEM", color: "#f97316",
    pair: "EURUSD / GBPUSD", tf: "H1",
    strategy_id: "London Session Breakout",
    strategy_en: "London Session Breakout",
    pf: "3.45", wr: "83.10%", dd: "5.90%", trades: "728", period: "Jan 2024 – Dec 2025",
    desc_id: "EA breakout yang mengeksploitasi momentum pembukaan sesi London. Entry pada breakout rentang Asian range dengan konfirmasi volume.",
    desc_en: "Breakout EA capturing volatility momentum during the London session open. Enters on Asian range breakouts with confirmed volume expansion.",
    includes_id: ["File AEMETH London Breakout v1.2 (.ex5)", "Input Parameter Template (.set)", "Panduan Instalasi PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH London Breakout v1.2 (.ex5)", "London Range Setfile (.set)", "Installation PDF Guide", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "grid-momentum": {
    name: "AEMETH Grid Momentum Pro v1.1",
    tag: "⚡ HIGH-FREQUENCY", color: "#06b6d4",
    pair: "EURUSD / GBPJPY", tf: "M5",
    strategy_id: "Momentum Grid HFT",
    strategy_en: "Momentum Grid HFT",
    pf: "3.70", wr: "85.00%", dd: "7.20%", trades: "4,560", period: "Jan 2024 – Dec 2025",
    desc_id: "Sistem grid berbasis momentum dengan entri frekuensi tinggi pada M5. Memanfaatkan osilasi harga mikro secara konsisten dengan target profit dinamis.",
    desc_en: "Momentum-driven grid algorithm with high-frequency entry frequency on M5. Capitalizes on intraday micro swings with dynamic profit targets.",
    includes_id: ["File AEMETH Grid Momentum Pro v1.1 (.ex5)", "Input Parameter Template (.set)", "Panduan Instalasi PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Grid Momentum Pro v1.1 (.ex5)", "Momentum Grid Setfile (.set)", "Installation PDF Guide", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "news-armor": {
    name: "AEMETH News Volatility Armor v1.0",
    tag: "🛡️ RISK MANAGEMENT", color: "#f43f5e",
    pair: "All Pairs", tf: "M1",
    strategy_id: "News Filter + Volatility Shield",
    strategy_en: "News Filter + Volatility Shield",
    pf: "3.15", wr: "80.70%", dd: "4.10%", trades: "1,050", period: "Jan 2024 – Dec 2025",
    desc_id: "EA dengan filter kalender berita otomatis yang melindungi posisi trading sebelum rilis data berdampak tinggi (high-impact economic news).",
    desc_en: "Risk shield EA featuring automated economic calendar news filters that protect and close vulnerable positions ahead of high-impact releases.",
    includes_id: ["File AEMETH News Armor v1.0 (.ex5)", "Input Parameter Template (.set)", "Panduan Kalender Berita PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH News Armor v1.0 (.ex5)", "News Shield Setfile (.set)", "News Calendar Setup Manual", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "night-scalper": {
    name: "AEMETH Night Scalper Elite v1.0",
    tag: "🥇 GOLD SCALPING", color: "#eab308",
    pair: "XAUUSD", tf: "M1",
    strategy_id: "Night Session Gold Scalper",
    strategy_en: "Night Session Gold Scalper",
    pf: "4.05", wr: "87.60%", dd: "5.20%", trades: "2,890", period: "Jan 2024 – Dec 2025",
    desc_id: "Scalper XAUUSD sesi malam memanfaatkan konsolidasi harga dengan spread rendah untuk mengumpulkan keuntungan pips secara konsisten.",
    desc_en: "Night session XAUUSD scalper capturing range-bound market liquidity with tight spreads to generate steady low-drawdown returns.",
    includes_id: ["File AEMETH Night Scalper Elite v1.0 (.ex5)", "Input Parameter Template (.set)", "Panduan Instalasi PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Night Scalper Elite v1.0 (.ex5)", "Night Session Setfile (.set)", "Installation PDF Guide", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  },
  "swing-multi": {
    name: "AEMETH Multi-Currency Swing v2.0",
    tag: "📈 TREND SYSTEM", color: "#8b5cf6",
    pair: "Multi-Pair", tf: "H4",
    strategy_id: "Multi-Currency Swing Trading",
    strategy_en: "Multi-Currency Swing Trading",
    pf: "4.30", wr: "86.20%", dd: "4.80%", trades: "412", period: "Jan 2024 – Dec 2025",
    desc_id: "EA swing trading multi-currency yang beroperasi pada H4 dengan diversifikasi portofolio otomatis guna meredam korelasi risiko antar pasangan mata uang.",
    desc_en: "H4 multi-currency swing trading system with automated cross-pair risk diversification designed for sustained portfolio drawdown stability.",
    includes_id: ["File AEMETH Multi-Currency Swing v2.0 (.ex5)", "Input Parameter Template (.set)", "Panduan Setup Multi-Pair PDF", "Lisensi Permanen Seumur Hidup"],
    includes_en: ["AEMETH Multi-Currency Swing v2.0 (.ex5)", "Multi-Currency Setfile (.set)", "Portfolio Setup Guide PDF", "Lifetime Permanent License"],
    note_id: "Hasil backtest. Performa masa lalu bukan jaminan performa di pasar riil.",
    note_en: "Simulated backtest data. Past performance does not guarantee future live market results."
  }
};

function openModal(id) {
  const p = products[id];
  if (!p) return;
  const lang = localStorage.getItem("lang") || "id";
  document.getElementById("modal-name").textContent = p.name;
  document.getElementById("modal-tag").textContent = p.tag;
  document.getElementById("modal-tag").style.color = p.color;
  document.getElementById("modal-pair").textContent = p.pair;
  document.getElementById("modal-tf").textContent = p.tf;
  document.getElementById("modal-strategy").textContent = lang === "en" ? p.strategy_en : p.strategy_id;
  document.getElementById("modal-pf").textContent = p.pf;
  document.getElementById("modal-wr").textContent = p.wr;
  document.getElementById("modal-dd").textContent = p.dd;
  document.getElementById("modal-trades").textContent = p.trades;
  document.getElementById("modal-period").textContent = p.period;
  document.getElementById("modal-desc").textContent = lang === "en" ? p.desc_en : p.desc_id;
  document.getElementById("modal-note").textContent = lang === "en" ? p.note_en : p.note_id;
  const listEl = document.getElementById("modal-includes");
  const incArr = lang === "en" ? p.includes_en : p.includes_id;
  listEl.innerHTML = incArr.map(i => `<li class="flex items-start gap-2"><span class="text-emerald-400 mt-0.5">✓</span><span>${i}</span></li>`).join("");
  document.getElementById("detail-modal").classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  document.getElementById("detail-modal").classList.add("hidden");
  document.body.style.overflow = "";
}

function setLanguage(lang) {
  localStorage.setItem("lang", lang);
  document.documentElement.lang = lang;
  const idBtn = document.getElementById("lang-id-btn");
  const enBtn = document.getElementById("lang-en-btn");
  if(lang === "id") {
    if (idBtn) idBtn.className = "cursor-pointer px-3 py-1 rounded-full text-xs font-bold transition-all bg-white text-black shadow";
    if (enBtn) enBtn.className = "cursor-pointer px-3 py-1 rounded-full text-xs font-medium text-zinc-400 hover:text-white transition-all";
  } else {
    if (enBtn) enBtn.className = "cursor-pointer px-3 py-1 rounded-full text-xs font-bold transition-all bg-white text-black shadow";
    if (idBtn) idBtn.className = "cursor-pointer px-3 py-1 rounded-full text-xs font-medium text-zinc-400 hover:text-white transition-all";
  }
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if(T[lang] && T[lang][key] !== undefined) {
      el.innerHTML = T[lang][key];
    }
  });
}

window.addEventListener("DOMContentLoaded", () => {
  const saved = localStorage.getItem("lang") || "id";
  setLanguage(saved);
});
</script>

</body>
</html>
'''

full_html = head_css + nav_html + hero_html + perf_html + why_html + bundle_html + ea_html + ind_html + pkg_html + faq_html + modal_html + footer_html + script_html

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Flawless site generated! Length:", len(full_html))
