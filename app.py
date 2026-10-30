import streamlit as st
import json
import textwrap

def render_html(html_str):
    if not html_str:
        return
    # Strip leading whitespace from EVERY line to completely prevent markdown code block detection
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned_html = " ".join(lines)
    st.markdown(cleaned_html, unsafe_allow_html=True)


# Set wide layout and custom page title
st.set_page_config(
    page_title="Dinamika Pelaksanaan UUD 1945 - Pendidikan Pancasila",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "slide" not in st.session_state:
    st.session_state.slide = 0

if "show_notes" not in st.session_state:
    st.session_state.show_notes = False

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# Custom CSS for rich animations, typography, and slide layouts
render_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Cinzel:wght@600;700;800;900&display=swap');

    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main {
        background: radial-gradient(circle at 10% 20%, rgba(16, 29, 66, 0.95) 0%, rgba(7, 13, 30, 0.98) 90%);
        color: #f1faee;
    }

    /* Keyframes for rich animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(28px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInSlide {
        from {
            opacity: 0;
            transform: scale(0.97) translateX(15px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateX(0);
        }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 15px rgba(230, 57, 70, 0.35); }
        50% { box-shadow: 0 0 35px rgba(244, 162, 97, 0.65); }
        100% { box-shadow: 0 0 15px rgba(230, 57, 70, 0.35); }
    }

    @keyframes floatSlow {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-7px) rotate(0.8deg); }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes badgeBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }

    /* Slide Container */
    .slide-wrapper {
        animation: fadeInSlide 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        background: rgba(16, 29, 66, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 32px 38px;
        margin-bottom: 24px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.45);
        position: relative;
        overflow: hidden;
    }

    .slide-wrapper::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #e63946, #ffd166, #e63946);
        background-size: 200% 100%;
        animation: shimmer 4s infinite linear;
    }

    /* Typography */
    .slide-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        background: rgba(230, 57, 70, 0.2);
        color: #ff6b6b;
        border: 1px solid rgba(230, 57, 70, 0.4);
        margin-bottom: 14px;
        animation: fadeInUp 0.4s ease forwards;
    }

    .slide-title {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
        line-height: 1.25;
        letter-spacing: 0.5px;
        text-shadow: 0 3px 12px rgba(0,0,0,0.6);
        animation: fadeInUp 0.5s ease forwards;
    }

    .slide-subtitle {
        font-size: 1.05rem;
        color: #a8dadc;
        font-weight: 400;
        margin-bottom: 24px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        padding-bottom: 14px;
        animation: fadeInUp 0.6s ease forwards;
    }

    /* Cards */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-top: 18px;
    }

    .content-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        transition: all 0.35s cubic-bezier(0.2, 0.8, 0.2, 1);
        position: relative;
    }

    .content-card:hover {
        transform: translateY(-6px);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(244, 162, 97, 0.45);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.35);
    }

    .card-icon {
        font-size: 2rem;
        margin-bottom: 12px;
        display: inline-block;
    }

    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffd166;
        margin-bottom: 8px;
    }

    .card-text {
        font-size: 0.92rem;
        line-height: 1.6;
        color: #e2e8f0;
    }

    /* Cover Page Specific Styles */
    .cover-hero {
        text-align: center;
        padding: 40px 20px;
        position: relative;
    }

    .cover-garuda {
        animation: floatSlow 5s ease-in-out infinite;
        filter: drop-shadow(0 0 25px rgba(255, 209, 102, 0.55));
        margin-bottom: 20px;
    }

    .cover-main-title {
        font-family: 'Cinzel', serif;
        font-size: 2.85rem;
        font-weight: 900;
        letter-spacing: 1.5px;
        background: linear-gradient(135deg, #ffffff 20%, #ffd166 60%, #e63946 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    .cover-tagline {
        font-size: 1.25rem;
        color: #a8dadc;
        max-width: 850px;
        margin: 0 auto 30px auto;
        line-height: 1.6;
    }

    .member-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 16px;
        max-width: 1000px;
        margin: 28px auto 0 auto;
    }

    .member-chip {
        background: linear-gradient(135deg, rgba(230, 57, 70, 0.12), rgba(16, 29, 66, 0.5));
        border: 1px solid rgba(255, 209, 102, 0.25);
        border-radius: 12px;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        text-align: left;
        transition: all 0.3s ease;
        animation: fadeInUp 0.7s ease forwards;
    }

    .member-chip:hover {
        transform: translateY(-4px) scale(1.02);
        border-color: #ffd166;
        box-shadow: 0 8px 20px rgba(255, 209, 102, 0.25);
        background: linear-gradient(135deg, rgba(230, 57, 70, 0.25), rgba(16, 29, 66, 0.7));
    }

    .member-number {
        background: #e63946;
        color: #ffffff;
        font-weight: 800;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.88rem;
        box-shadow: 0 0 10px rgba(230, 57, 70, 0.5);
    }

    .member-name {
        font-weight: 700;
        color: #ffffff;
        font-size: 0.96rem;
        letter-spacing: 0.3px;
    }

    .member-role {
        font-size: 0.75rem;
        color: #a8dadc;
    }

    /* Timeline Horizontal Flow */
    .timeline-container {
        display: flex;
        overflow-x: auto;
        gap: 14px;
        padding: 20px 8px;
        margin-top: 10px;
        scrollbar-width: thin;
    }

    .timeline-step {
        flex: 1;
        min-width: 170px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        position: relative;
        transition: all 0.3s;
    }

    .timeline-step.active {
        border-color: #ffd166;
        background: rgba(255, 209, 102, 0.12);
        box-shadow: 0 0 16px rgba(255, 209, 102, 0.35);
        transform: translateY(-3px);
    }

    .timeline-year {
        font-size: 0.85rem;
        font-weight: 800;
        color: #e63946;
        margin-bottom: 4px;
    }

    .timeline-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* Highlights & Quotes */
    .quote-box {
        border-left: 4px solid #ffd166;
        padding: 16px 22px;
        background: rgba(255, 209, 102, 0.08);
        border-radius: 0 12px 12px 0;
        margin: 20px 0;
        font-style: italic;
        color: #f1faee;
        font-size: 1.02rem;
    }

    .badge-highlight {
        background: rgba(244, 162, 97, 0.2);
        color: #ffd166;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    /* Presenter Notes Styling */
    .speaker-notes {
        background: rgba(10, 17, 40, 0.8);
        border: 1px dashed rgba(255, 209, 102, 0.5);
        border-radius: 12px;
        padding: 18px 24px;
        margin-top: 20px;
        color: #ffd166;
        font-size: 0.9rem;
    }
    
    /* Replica SVG Box */
    .replica-graphic-box {
        background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 280px;
        text-align: center;
    }
</style>
""")




# Helper Generator for 15 Replica Animated Mini-Videos
def get_replica_video_card(slide_id):
    videos = {
        0: {
            "title": "KILAS DOKUMENTER: REVOLUSI & LAHIRNYA UUD 1945",
            "tag": "DOKUMENTER HISTORIS • REPLIKA ARCHIVE",
            "badge_color": "#e63946",
            "time": "17 - 18 AGUSTUS 1945",
            "desc": "Simulasi visual pengibaran Sang Saka Merah Putih di Pegangsaan Timur 56 dan momentum sidang penetapan UUD 1945 oleh PPKI.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <radialGradient id="skyGrad" cx="50%" cy="30%" r="70%">
                            <stop offset="0%" stop-color="#2a0845"/>
                            <stop offset="60%" stop-color="#140b2d"/>
                            <stop offset="100%" stop-color="#070a1a"/>
                        </radialGradient>
                        <linearGradient id="flagRed" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#ff0000"/>
                            <stop offset="50%" stop-color="#cc0000"/>
                            <stop offset="100%" stop-color="#ff3333"/>
                        </linearGradient>
                    </defs>
                    <rect width="400" height="210" fill="url(#skyGrad)"/>
                    <circle cx="200" cy="90" r="75" fill="#ffd166" opacity="0.12">
                        <animate attributeName="r" values="70;82;70" dur="4s" repeatCount="indefinite"/>
                        <animate attributeName="opacity" values="0.08;0.18;0.08" dur="4s" repeatCount="indefinite"/>
                    </circle>
                    <!-- Tiang Bendera -->
                    <rect x="130" y="25" width="5" height="165" fill="#e2e8f0" rx="2"/>
                    <circle cx="132.5" cy="24" r="5" fill="#ffd166"/>
                    <!-- Bendera Berkibar Animasi -->
                    <g>
                        <path d="M135 30 Q165 24 195 32 T255 30 L255 58 Q225 64 195 56 T135 60 Z" fill="url(#flagRed)">
                            <animate attributeName="d" values="
                                M135 30 Q165 24 195 32 T255 30 L255 58 Q225 64 195 56 T135 60 Z;
                                M135 30 Q165 35 195 26 T255 33 L255 61 Q225 54 195 63 T135 60 Z;
                                M135 30 Q165 24 195 32 T255 30 L255 58 Q225 64 195 56 T135 60 Z" dur="2.2s" repeatCount="indefinite"/>
                        </path>
                        <path d="M135 60 Q165 54 195 62 T255 60 L255 88 Q225 94 195 86 T135 90 Z" fill="#ffffff">
                            <animate attributeName="d" values="
                                M135 60 Q165 54 195 62 T255 60 L255 88 Q225 94 195 86 T135 90 Z;
                                M135 60 Q165 65 195 56 T255 63 L255 91 Q225 84 195 93 T135 90 Z;
                                M135 60 Q165 54 195 62 T255 60 L255 88 Q225 94 195 86 T135 90 Z" dur="2.2s" repeatCount="indefinite"/>
                        </path>
                    </g>
                    <!-- Siluet Tokoh Proklamasi & Garuda -->
                    <path d="M0 210 L0 185 Q100 175 200 185 Q300 195 400 180 L400 210 Z" fill="#0d1b2a"/>
                    <circle cx="280" cy="140" r="14" fill="#1b263b"/>
                    <path d="M265 185 C265 158 295 158 295 185 Z" fill="#1b263b"/>
                    <circle cx="320" cy="144" r="12" fill="#1b263b"/>
                    <path d="M308 185 C308 162 332 162 332 185 Z" fill="#1b263b"/>
                    <text x="200" y="200" fill="#ffd166" font-size="9" font-family="'Cinzel', serif" font-weight="bold" text-anchor="middle" letter-spacing="2">PROKLAMASI & PENGESAHAN UUD 1945</text>
                </svg>
            """
        },
        1: {
            "title": "TIMELINE JOURNEY: 6 BABAK DINAMIKA KONSTITUSI",
            "tag": "INTERACTIVE INFOGRAPHIC ANIMATION",
            "badge_color": "#ffd166",
            "time": "1945 - ERA SEKARANG",
            "desc": "Simulasi alur gerak pulsa garis waktu menyusuri 6 periode metamorfosis tata negara dari revolusi kemerdekaan hingga era digital.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#0a1128"/>
                    <!-- Path Garis Alur Berdenyut -->
                    <path d="M30 105 C90 40 130 170 190 105 C250 40 290 170 370 105" stroke="#1d3557" stroke-width="6" fill="none" stroke-linecap="round"/>
                    <path d="M30 105 C90 40 130 170 190 105 C250 40 290 170 370 105" stroke="#ffd166" stroke-width="3" fill="none" stroke-dasharray="10 8" stroke-linecap="round">
                        <animate attributeName="stroke-dashoffset" values="100;0" dur="4s" repeatCount="indefinite"/>
                    </path>
                    <!-- Titik Stasiun Periode -->
                    <g transform="translate(45, 85)">
                        <circle cx="0" cy="0" r="10" fill="#e63946"/>
                        <circle cx="0" cy="0" r="16" fill="none" stroke="#e63946" opacity="0.6">
                            <animate attributeName="r" values="10;20;10" dur="2s" repeatCount="indefinite"/>
                            <animate attributeName="opacity" values="0.8;0;0.8" dur="2s" repeatCount="indefinite"/>
                        </circle>
                        <text x="0" y="24" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">1945</text>
                    </g>
                    <g transform="translate(110, 130)">
                        <circle cx="0" cy="0" r="9" fill="#457b9d"/>
                        <text x="0" y="22" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">RIS 49</text>
                    </g>
                    <g transform="translate(190, 105)">
                        <circle cx="0" cy="0" r="9" fill="#06d6a0"/>
                        <text x="0" y="22" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">1950</text>
                    </g>
                    <g transform="translate(265, 75)">
                        <circle cx="0" cy="0" r="9" fill="#e76f51"/>
                        <text x="0" y="22" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">1959</text>
                    </g>
                    <g transform="translate(325, 135)">
                        <circle cx="0" cy="0" r="9" fill="#f4a261"/>
                        <text x="0" y="22" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">ORBA</text>
                    </g>
                    <g transform="translate(370, 105)">
                        <circle cx="0" cy="0" r="11" fill="#ffd166"/>
                        <circle cx="0" cy="0" r="18" fill="none" stroke="#ffd166" opacity="0.8">
                            <animate attributeName="r" values="11;22;11" dur="1.8s" repeatCount="indefinite"/>
                            <animate attributeName="opacity" values="0.9;0;0.9" dur="1.8s" repeatCount="indefinite"/>
                        </circle>
                        <text x="0" y="24" fill="#ffd166" font-size="7" font-weight="bold" text-anchor="middle">1999-KINI</text>
                    </g>
                </svg>
            """
        },
        2: {
            "title": "SUPREMASI HUKUM: TIMBANGAN KEADILAN BERAYUN",
            "tag": "SIMULASI YURIDIS • RECHTSSTAAT",
            "badge_color": "#06d6a0",
            "time": "PASAL 1 AYAT (3) UUD 1945",
            "desc": "Animasi dinamis neraca keadilan berayun melambangkan kedudukan hukum tertinggi yang menyeimbangkan kekuasaan negara dengan hak asasi rakyat.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#0b132b"/>
                    <!-- Tiang Pusat -->
                    <rect x="196" y="35" width="8" height="145" fill="#ffd166" rx="3"/>
                    <rect x="150" y="175" width="100" height="12" fill="#1c2541" stroke="#ffd166" stroke-width="2" rx="4"/>
                    <circle cx="200" cy="40" r="9" fill="#e63946" stroke="#ffd166" stroke-width="2"/>
                    <!-- Lengan Neraca Berayun Harmonik -->
                    <g>
                        <animateTransform attributeName="transform" type="rotate" values="-6 200 40; 6 200 40; -6 200 40" dur="4s" repeatCount="indefinite" ease="ease-in-out"/>
                        <line x1="80" y1="40" x2="320" y2="40" stroke="#ffd166" stroke-width="5" stroke-linecap="round"/>
                        <!-- Cawan Kiri (Kekuasaan Negara) -->
                        <line x1="100" y1="40" x2="80" y2="105" stroke="#a8dadc" stroke-width="1.8"/>
                        <line x1="100" y1="40" x2="120" y2="105" stroke="#a8dadc" stroke-width="1.8"/>
                        <path d="M70 105 Q100 135 130 105 Z" fill="#e63946" opacity="0.85"/>
                        <text x="100" y="125" fill="#ffffff" font-size="6" font-weight="bold" text-anchor="middle">KEKUASAAN</text>
                        <!-- Cawan Kanan (Kedaulatan Rakyat) -->
                        <line x1="300" y1="40" x2="280" y2="105" stroke="#a8dadc" stroke-width="1.8"/>
                        <line x1="300" y1="40" x2="320" y2="105" stroke="#a8dadc" stroke-width="1.8"/>
                        <path d="M270 105 Q300 135 330 105 Z" fill="#06d6a0" opacity="0.85"/>
                        <text x="300" y="125" fill="#070d1e" font-size="6" font-weight="bold" text-anchor="middle">HAK RAKYAT</text>
                    </g>
                    <text x="200" y="200" fill="#ffd166" font-size="8" font-family="'Cinzel', serif" font-weight="bold" text-anchor="middle">STAATSFUNDAMENTALNORM & RECHTSSTAAT</text>
                </svg>
            """
        },
        3: {
            "title": "ARSIP PPKI: PENGESAHAN DOKUMEN UUD 1945",
            "tag": "REPLIKA DOKUMEN SEJARAH",
            "badge_color": "#e63946",
            "time": "18 AGUSTUS 1945",
            "desc": "Simulasi efek pembukaan lembaran naskah konstitusi pertama di Gedung Chuo Sangi In (Gedung Pancasila).",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#0d1b2a"/>
                    <!-- Buku Naskah UUD 1945 Terbuka -->
                    <g transform="translate(100, 30)">
                        <rect x="0" y="0" width="95" height="135" rx="4" fill="#f8edeb" stroke="#ffd166" stroke-width="2"/>
                        <rect x="105" y="0" width="95" height="135" rx="4" fill="#f8edeb" stroke="#ffd166" stroke-width="2"/>
                        <rect x="94" y="0" width="12" height="135" fill="#b08968"/>
                        <!-- Garis Teks Naskah Bergetar Tinta Emas -->
                        <line x1="12" y1="20" x2="82" y2="20" stroke="#e63946" stroke-width="3"/>
                        <line x1="15" y1="35" x2="80" y2="35" stroke="#415a77" stroke-width="1.8"/>
                        <line x1="15" y1="48" x2="80" y2="48" stroke="#415a77" stroke-width="1.8"/>
                        <line x1="15" y1="61" x2="75" y2="61" stroke="#415a77" stroke-width="1.8"/>
                        <line x1="15" y1="74" x2="80" y2="74" stroke="#415a77" stroke-width="1.8"/>
                        <line x1="15" y1="87" x2="65" y2="87" stroke="#415a77" stroke-width="1.8"/>
                        <!-- Halaman Kanan -->
                        <line x1="117" y1="20" x2="187" y2="20" stroke="#e63946" stroke-width="3"/>
                        <line x1="120" y1="35" x2="185" y2="35" stroke="#415a77" stroke-width="1.8"/>
                        <line x1="120" y1="48" x2="185" y2="48" stroke="#415a77" stroke-width="1.8"/>
                        <line x1="120" y1="61" x2="175" y2="61" stroke="#415a77" stroke-width="1.8"/>
                        <circle cx="152" cy="100" r="16" fill="#e63946" opacity="0.8">
                            <animate attributeName="r" values="14;18;14" dur="2.5s" repeatCount="indefinite"/>
                        </circle>
                        <text x="152" y="103" fill="#ffffff" font-size="5" font-weight="bold" text-anchor="middle">PPKI 1945</text>
                    </g>
                    <text x="200" y="195" fill="#ffd166" font-size="8" font-family="'Cinzel', serif" font-weight="bold" text-anchor="middle">PENETAPAN 37 PASAL & ATURAN PERALIHAN</text>
                </svg>
            """
        },
        4: {
            "title": "PERALIHAN SISTEM: PRESIDENSIAL KE PARLEMENTER",
            "tag": "DIALEKTIKA STRATEGI DIPLOMASI",
            "badge_color": "#f4a261",
            "time": "OKTOBER - NOVEMBER 1945",
            "desc": "Simulasi perpindahan kendali eksekutif dari Dwi Tunggal Soekarno-Hatta kepada Perdana Menteri Sutan Sjahrir melalui Maklumat No. X.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#14213d"/>
                    <!-- Kotak Presidensial -->
                    <rect x="40" y="55" width="120" height="90" rx="8" fill="#1b263b" stroke="#e63946" stroke-width="2"/>
                    <text x="100" y="85" fill="#e63946" font-size="8" font-weight="bold" text-anchor="middle">PRESIDENSIAL</text>
                    <text x="100" y="105" fill="#a8dadc" font-size="6" text-anchor="middle">Menteri Bertanggung</text>
                    <text x="100" y="117" fill="#a8dadc" font-size="6" text-anchor="middle">Jawab ke Presiden</text>
                    <!-- Panah Transformasi Animasi Berdenyut -->
                    <g transform="translate(180, 90)">
                        <path d="M0 10 L30 10 L30 0 L48 15 L30 30 L30 20 L0 20 Z" fill="#ffd166">
                            <animate attributeName="transform" type="translate" values="0,0; 8,0; 0,0" dur="1.5s" repeatCount="indefinite"/>
                        </path>
                        <text x="24" y="-8" fill="#ffd166" font-size="6" font-weight="bold" text-anchor="middle">Maklumat 14 Nov</text>
                    </g>
                    <!-- Kotak Parlementer -->
                    <rect x="240" y="55" width="120" height="90" rx="8" fill="#1b263b" stroke="#06d6a0" stroke-width="2"/>
                    <text x="300" y="85" fill="#06d6a0" font-size="8" font-weight="bold" text-anchor="middle">PARLEMENTER</text>
                    <text x="300" y="105" fill="#a8dadc" font-size="6" text-anchor="middle">Perdana Menteri</text>
                    <text x="300" y="117" fill="#a8dadc" font-size="6" text-anchor="middle">& Kabinet BP-KNIP</text>
                    <text x="200" y="185" fill="#e2e8f0" font-size="7" text-anchor="middle">KONVENSI KETATANEGARAAN TANPA MERUBAH TEKS UUD</text>
                </svg>
            """
        },
        5: {
            "title": "PECAH BELAH FEDERALISME: ERA KONSTITUSI RIS",
            "tag": "STRATEGI DEVIDE ET IMPERA",
            "badge_color": "#e76f51",
            "time": "27 DESEMBER 1949",
            "desc": "Simulasi pemecahan kepulauan Nusantara menjadi 16 negara bagian/satuan otonom ciptaan Van Mook pasca KMB Den Haag.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#0f172a"/>
                    <!-- Peta Kepulauan Indonesia Terbelah Puzzle -->
                    <g opacity="0.85">
                        <path d="M50 110 Q90 80 130 115 T170 110" stroke="#e63946" stroke-width="8" stroke-linecap="round" fill="none"/>
                        <text x="90" y="80" fill="#e63946" font-size="6" font-weight="bold">Negara Sumatra Timur</text>
                        <path d="M140 145 Q170 135 210 150 T250 145" stroke="#ffd166" stroke-width="8" stroke-linecap="round" fill="none"/>
                        <text x="180" y="175" fill="#ffd166" font-size="6" font-weight="bold">Negara Pasundan / Madura</text>
                        <path d="M210 95 Q240 70 270 100 T290 85" stroke="#457b9d" stroke-width="9" stroke-linecap="round" fill="none"/>
                        <path d="M280 115 Q320 85 350 120 T380 110" stroke="#06d6a0" stroke-width="8" stroke-linecap="round" fill="none"/>
                        <text x="325" y="75" fill="#06d6a0" font-size="6" font-weight="bold">Negara Indonesia Timur</text>
                    </g>
                    <!-- Tanda Seru Bahaya Disintegrasi -->
                    <circle cx="200" cy="50" r="15" fill="#e63946">
                        <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite"/>
                    </circle>
                    <text x="200" y="55" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">!</text>
                    <text x="200" y="198" fill="#ffd166" font-size="8" font-family="'Cinzel', serif" font-weight="bold" text-anchor="middle">REPUBLIK INDONESIA SERIKAT HANYA BERTAHAN 8 BULAN</text>
                </svg>
            """
        },
        6: {
            "title": "MOSI INTEGRAL NATSIR: KEMBALINYA PERSATUAN NKRI",
            "tag": "DIPLOMASI PEMERSATU BANGSA",
            "badge_color": "#06d6a0",
            "time": "3 APRIL - 17 AGUSTUS 1950",
            "desc": "Simulasi penyatuan kembali kepingan negara-negara bagian melebur kembali ke dalam wadah tunggal Republik Indonesia.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#081c15"/>
                    <!-- Efek Lingkaran Medan Magnet Penyatuan -->
                    <circle cx="200" cy="95" r="55" fill="none" stroke="#2d6a4f" stroke-width="2" stroke-dasharray="6 4">
                        <animate attributeName="r" values="30;75;30" dur="3s" repeatCount="indefinite"/>
                        <animate attributeName="opacity" values="1;0.2;1" dur="3s" repeatCount="indefinite"/>
                    </circle>
                    <!-- Pusat NKRI -->
                    <circle cx="200" cy="95" r="28" fill="#e63946" stroke="#ffd166" stroke-width="2.5"/>
                    <text x="200" y="98" fill="#ffffff" font-size="9" font-weight="bold" text-anchor="middle">NKRI</text>
                    <!-- Satelit Bagian yang Masuk Kembali -->
                    <g>
                        <circle cx="110" cy="65" r="14" fill="#1b4332" stroke="#52b788"/>
                        <text x="110" y="67" fill="#d8f3dc" font-size="5" text-anchor="middle">NIT</text>
                        <animateTransform attributeName="transform" type="translate" values="0,0; 30,12; 0,0" dur="2.5s" repeatCount="indefinite"/>
                    </g>
                    <g>
                        <circle cx="290" cy="65" r="14" fill="#1b4332" stroke="#52b788"/>
                        <text x="290" y="67" fill="#d8f3dc" font-size="5" text-anchor="middle">Pasundan</text>
                        <animateTransform attributeName="transform" type="translate" values="0,0; -30,12; 0,0" dur="2.5s" repeatCount="indefinite"/>
                    </g>
                    <g>
                        <circle cx="200" cy="165" r="14" fill="#1b4332" stroke="#52b788"/>
                        <text x="200" y="167" fill="#d8f3dc" font-size="5" text-anchor="middle">Sumatra</text>
                        <animateTransform attributeName="transform" type="translate" values="0,0; 0,-24; 0,0" dur="2.5s" repeatCount="indefinite"/>
                    </g>
                    <text x="200" y="200" fill="#ffd166" font-size="8" font-family="'Cinzel', serif" font-weight="bold" text-anchor="middle">17 AGUSTUS 1950 • PROKLAMASI PEMBUBARAN RIS</text>
                </svg>
            """
        },
        7: {
            "title": "DEMOKRASI LIBERAL: KRONIK JATUH BANGUN KABINET",
            "tag": "INSTABILITAS SISTEM PARLEMENTER",
            "badge_color": "#f4a261",
            "time": "1950 - 1959 (UUDS 1950)",
            "desc": "Simulasi rotasi 7 kabinet dalam 9 tahun akibat mosi tidak percaya di parlemen yang menghambat stabilitas nasional.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#1d2d44"/>
                    <!-- Roda Gerigi Berputar Kabinet -->
                    <g transform="translate(130, 95)">
                        <circle cx="0" cy="0" r="45" fill="none" stroke="#ffd166" stroke-width="4" stroke-dasharray="14 10">
                            <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/>
                        </circle>
                        <circle cx="0" cy="0" r="28" fill="#0d1b2a" stroke="#e63946" stroke-width="2"/>
                        <text x="0" y="3" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">7 KABINET</text>
                    </g>
                    <!-- Info Pemilu 1955 -->
                    <rect x="230" y="45" width="130" height="100" rx="8" fill="#0d1b2a" stroke="#06d6a0" stroke-width="1.8"/>
                    <text x="295" y="70" fill="#06d6a0" font-size="8" font-weight="bold" text-anchor="middle">PEMILU 1955</text>
                    <line x1="245" y1="80" x2="345" y2="80" stroke="#415a77" stroke-width="1"/>
                    <text x="295" y="98" fill="#e2e8f0" font-size="6.5" text-anchor="middle">Prestasi Terbesar:</text>
                    <text x="295" y="112" fill="#ffd166" font-size="6.5" text-anchor="middle">Pemilu Paling Jujur</text>
                    <text x="295" y="128" fill="#a8dadc" font-size="6" text-anchor="middle">PNI, Masyumi, NU, PKI</text>
                    <text x="200" y="195" fill="#f1faee" font-size="7.5" text-anchor="middle">RATA-RATA USIA KABINET HANYA BERTAHAN 1 TAHUN</text>
                </svg>
            """
        },
        8: {
            "title": "TITIK BALIK KRUSIAL: DEKRIT PRESIDEN 5 JULI 1959",
            "tag": "PENYELAMATAN NEGARA DARURAT",
            "badge_color": "#e63946",
            "time": "5 JULI 1959 • 17.00 WIB",
            "desc": "Simulasi pembacaan titah sakral Presiden Soekarno membubarkan Konstituante dan mengumumkan kembali berlakunya UUD 1945.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#2b0908"/>
                    <circle cx="200" cy="100" r="85" fill="#e63946" opacity="0.15">
                        <animate attributeName="r" values="70;95;70" dur="3s" repeatCount="indefinite"/>
                    </circle>
                    <!-- Lembar Dekrit dengan Segel Lilin Merah Menyala -->
                    <g transform="translate(135, 25)">
                        <rect x="0" y="0" width="130" height="145" rx="5" fill="#fefae0" stroke="#ffd166" stroke-width="2.5"/>
                        <line x1="20" y1="25" x2="110" y2="25" stroke="#9d0208" stroke-width="3"/>
                        <line x1="25" y1="40" x2="105" y2="40" stroke="#333333" stroke-width="1.5"/>
                        <line x1="20" y1="52" x2="110" y2="52" stroke="#333333" stroke-width="1.5"/>
                        <line x1="20" y1="64" x2="110" y2="64" stroke="#333333" stroke-width="1.5"/>
                        <line x1="20" y1="76" x2="90" y2="76" stroke="#333333" stroke-width="1.5"/>
                        <circle cx="65" cy="110" r="16" fill="#d90429"/>
                        <path d="M58 110 L63 115 L73 103" stroke="#ffffff" stroke-width="2.5" fill="none"/>
                    </g>
                    <text x="200" y="195" fill="#ffd166" font-size="8.5" font-family="'Cinzel', serif" font-weight="bold" text-anchor="middle">KEMBALI KE UUD 1945 ATAS DASAR STAATSNOODRECHT</text>
                </svg>
            """
        },
        9: {
            "title": "DEMOKRASI TERPIMPIN: SENTRALISME ORDE LAMA",
            "tag": "ANALISIS PENYIMPANGAN HUKUM",
            "badge_color": "#e63946",
            "time": "1959 - 1966",
            "desc": "Simulasi pemusatan kekuasaan eksekutif, pembubaran parlemen hasil pemilu, dan doktrin Nasakom / Manipol USDEK.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#1a0000"/>
                    <!-- Piramida Sentralistik -->
                    <polygon points="200,30 110,165 290,165" fill="#370617" stroke="#e63946" stroke-width="2"/>
                    <!-- Puncak Kekuasaan -->
                    <circle cx="200" cy="50" r="12" fill="#ffd166"/>
                    <text x="200" y="53" fill="#000000" font-size="6" font-weight="bold" text-anchor="middle">PEMIMPIN</text>
                    <!-- Pilar Bawah Tersubordinasi -->
                    <rect x="135" y="105" width="40" height="20" rx="3" fill="#6a040f"/>
                    <text x="155" y="117" fill="#ffffff" font-size="5" text-anchor="middle">MPRS</text>
                    <rect x="180" y="105" width="40" height="20" rx="3" fill="#6a040f"/>
                    <text x="200" y="117" fill="#ffffff" font-size="5" text-anchor="middle">DPR-GR</text>
                    <rect x="225" y="105" width="40" height="20" rx="3" fill="#6a040f"/>
                    <text x="245" y="117" fill="#ffffff" font-size="5" text-anchor="middle">MA</text>
                    <!-- Garis Peringatan Penyimpangan -->
                    <text x="200" y="150" fill="#ffd166" font-size="6.5" font-weight="bold" text-anchor="middle">TAP MPRS No. III/1963</text>
                    <text x="200" y="195" fill="#ffb703" font-size="7.5" text-anchor="middle">SUBORDINASI LEMBAGA TINGGI NEGARA DI BAWAH EKSEKUTIF</text>
                </svg>
            """
        },
        10: {
            "title": "ORDE BARU: HEGEMONI EKSEKUTIF 32 TAHUN",
            "tag": "SAKRALISASI & EXECUTIVE HEAVY",
            "badge_color": "#d4a373",
            "time": "1966 - 1998",
            "desc": "Simulasi doktrin stabilisasi politik, penataran P4/BP-7, fusi partai politik, dan hegemoni kekuasaan yang terkunci rapat.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#1b1d28"/>
                    <!-- Gembok Raksasa Sakralisasi UUD 1945 -->
                    <g transform="translate(170, 35)">
                        <path d="M15 50 V25 C15 5 45 5 45 25 V50" fill="none" stroke="#ffd166" stroke-width="6"/>
                        <rect x="0" y="45" width="60" height="55" rx="6" fill="#343a40" stroke="#ffd166" stroke-width="2"/>
                        <circle cx="30" cy="70" r="6" fill="#ffd166"/>
                        <line x1="30" y1="74" x2="30" y2="85" stroke="#ffd166" stroke-width="3"/>
                    </g>
                    <!-- 3 Fraksi Hasil Fusi -->
                    <rect x="70" y="130" width="60" height="24" rx="4" fill="#2b9348"/>
                    <text x="100" y="145" fill="#ffffff" font-size="6.5" font-weight="bold" text-anchor="middle">PPP</text>
                    <rect x="170" y="125" width="60" height="30" rx="4" fill="#ffb703"/>
                    <text x="200" y="143" fill="#000000" font-size="7.5" font-weight="bold" text-anchor="middle">GOLKAR</text>
                    <rect x="270" y="130" width="60" height="24" rx="4" fill="#d90429"/>
                    <text x="300" y="145" fill="#ffffff" font-size="6.5" font-weight="bold" text-anchor="middle">PDI</text>
                    <text x="200" y="195" fill="#ffd166" font-size="7.5" text-anchor="middle">UU NO. 5/1985 TENTANG REFERENDUM MENYAKRALKAN UUD</text>
                </svg>
            """
        },
        11: {
            "title": "GELOMBANG REFORMASI: 4 TAHAP AMANDEMEN",
            "tag": "TRANSFORMASI KONSTITUSI MODERN",
            "badge_color": "#06d6a0",
            "time": "1999 - 2002 (SIDANG UMUM/TAHUNAN MPR)",
            "desc": "Simulasi pembaruan 4 etape konstitusi secara bertahap menjaga keutuhan Pembukaan dan bentuk NKRI.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#0b092b"/>
                    <!-- Diagram 4 Etape Amandemen -->
                    <g transform="translate(45, 90)">
                        <circle cx="40" cy="0" r="22" fill="#1d3557" stroke="#e63946" stroke-width="2.5"/>
                        <text x="40" y="-3" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">TAHAP I</text>
                        <text x="40" y="9" fill="#ffd166" font-size="6" text-anchor="middle">1999</text>
                        <line x1="62" y1="0" x2="108" y2="0" stroke="#ffd166" stroke-width="2" stroke-dasharray="4 2"/>
                        <circle cx="130" cy="0" r="22" fill="#1d3557" stroke="#ffd166" stroke-width="2.5"/>
                        <text x="130" y="-3" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">TAHAP II</text>
                        <text x="130" y="9" fill="#ffd166" font-size="6" text-anchor="middle">2000</text>
                        <line x1="152" y1="0" x2="198" y2="0" stroke="#ffd166" stroke-width="2" stroke-dasharray="4 2"/>
                        <circle cx="220" cy="0" r="22" fill="#1d3557" stroke="#06d6a0" stroke-width="2.5"/>
                        <text x="220" y="-3" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">TAHAP III</text>
                        <text x="220" y="9" fill="#ffd166" font-size="6" text-anchor="middle">2001</text>
                        <line x1="242" y1="0" x2="288" y2="0" stroke="#ffd166" stroke-width="2" stroke-dasharray="4 2"/>
                        <circle cx="310" cy="0" r="22" fill="#1d3557" stroke="#3a86ff" stroke-width="2.5"/>
                        <text x="310" y="-3" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">TAHAP IV</text>
                        <text x="310" y="9" fill="#ffd166" font-size="6" text-anchor="middle">2002</text>
                    </g>
                    <text x="200" y="185" fill="#ffd166" font-size="8" font-family="'Cinzel', serif" font-weight="bold" text-anchor="middle">DARI 37 PASAL MENJADI 73 PASAL & ADENDUM RESMI</text>
                </svg>
            """
        },
        12: {
            "title": "LEMBAGA BARU: MAHKAMAH KONSTITUSI & DPD RI",
            "tag": "CHECK AND BALANCES HORIZONTAL",
            "badge_color": "#3a86ff",
            "time": "PASCA AMANDEMEN 2002",
            "desc": "Simulasi kesetaraan cabang kekuasaan trias politika modern dilengkapi Mahkamah Konstitusi sebagai penjaga gawang konstitusi.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#03071e"/>
                    <!-- Segitiga Keseimbangan Lembaga -->
                    <circle cx="200" cy="50" r="24" fill="#370617" stroke="#ffd166" stroke-width="2"/>
                    <text x="200" y="48" fill="#ffd166" font-size="6" font-weight="bold" text-anchor="middle">PRESIDEN</text>
                    <text x="200" y="58" fill="#ffffff" font-size="5" text-anchor="middle">Max 2 Periode</text>
                    <circle cx="95" cy="140" r="24" fill="#1d3557" stroke="#06d6a0" stroke-width="2"/>
                    <text x="95" y="138" fill="#06d6a0" font-size="6" font-weight="bold" text-anchor="middle">DPR & DPD</text>
                    <text x="95" y="148" fill="#ffffff" font-size="5" text-anchor="middle">Bikameral</text>
                    <circle cx="305" cy="140" r="24" fill="#1d3557" stroke="#3a86ff" stroke-width="2"/>
                    <text x="305" y="138" fill="#3a86ff" font-size="6" font-weight="bold" text-anchor="middle">MK & MA & KY</text>
                    <text x="305" y="148" fill="#ffffff" font-size="5" text-anchor="middle">Judicial Power</text>
                    <!-- Garis Hubungan Timbal Balik -->
                    <line x1="180" y1="65" x2="115" y2="120" stroke="#ffd166" stroke-width="1.5" stroke-dasharray="3 2"/>
                    <line x1="220" y1="65" x2="285" y2="120" stroke="#ffd166" stroke-width="1.5" stroke-dasharray="3 2"/>
                    <line x1="120" y1="140" x2="280" y2="140" stroke="#ffd166" stroke-width="1.5" stroke-dasharray="3 2"/>
                    <text x="200" y="195" fill="#a8dadc" font-size="7.5" text-anchor="middle">TIDAK ADA LAGI LEMBAGA TERTINGGI NEGARA • SEJAJAR HORIZONTAL</text>
                </svg>
            """
        },
        13: {
            "title": "TATA KELOLA KONTEMPORER: INDEPENDENSI & RUANG DIGITAL",
            "tag": "TANTANGAN ERA MODERN",
            "badge_color": "#ff006e",
            "time": "ERA DISRUPSI DIGITAL & POLITIK",
            "desc": "Simulasi tantangan menjaga benteng independensi peradilan di tengah arus polarisasi siber dan tuntutan partisipasi bermakna.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="400" height="210" fill="#0b091a"/>
                    <!-- Jaring Gelombang Digital / Cyber Network -->
                    <path d="M20 100 Q100 40 200 100 T380 100" stroke="#3a86ff" stroke-width="2" fill="none" opacity="0.4"/>
                    <path d="M20 120 Q100 180 200 120 T380 120" stroke="#ff006e" stroke-width="2" fill="none" opacity="0.4"/>
                    <!-- Perisai Perlindungan Konstitusi -->
                    <g transform="translate(170, 40)">
                        <path d="M30 10 L60 20 V60 C60 90 30 110 30 110 C30 110 0 90 0 60 V20 Z" fill="#1d3557" stroke="#ffd166" stroke-width="3"/>
                        <circle cx="30" cy="50" r="14" fill="#ffd166"/>
                        <text x="30" y="53" fill="#000000" font-size="6" font-weight="bold" text-anchor="middle">MK</text>
                    </g>
                    <!-- Satelit Tantangan -->
                    <rect x="35" y="75" width="95" height="30" rx="4" fill="#161a2e" stroke="#06d6a0" stroke-width="1.5"/>
                    <text x="82" y="93" fill="#06d6a0" font-size="5.5" font-weight="bold" text-anchor="middle">Public Participation</text>
                    <rect x="270" y="75" width="95" height="30" rx="4" fill="#161a2e" stroke="#ff006e" stroke-width="1.5"/>
                    <text x="317" y="93" fill="#ff006e" font-size="5.5" font-weight="bold" text-anchor="middle">Etika & Polarisasi</text>
                    <text x="200" y="185" fill="#ffd166" font-size="7.5" text-anchor="middle">MENJAGA MURWAH THE GUARDIAN OF CONSTITUTION</text>
                </svg>
            """
        },
        14: {
            "title": "REFLEKSI PANCASILA: MENUJU INDONESIA EMAS 2045",
            "tag": "SINTESIS FINAL KELOMPOK",
            "badge_color": "#ffd166",
            "time": "1945 - 2045 (100 TAHUN MERDEKA)",
            "desc": "Simulasi harmoni 5 Bintang Pancasila yang bersinar menopang Konstitusi UUD 1945 menuju satu abad kemerdekaan Indonesia.",
            "svg": """
                <svg viewBox="0 0 400 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <radialGradient id="goldGlow" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#ffd166" stop-opacity="0.3"/>
                        <stop offset="100%" stop-color="#ffd166" stop-opacity="0"/>
                    </radialGradient>
                    <rect width="400" height="210" fill="#070a1e"/>
                    <circle cx="200" cy="95" r="80" fill="url(#goldGlow)"/>
                    <!-- Bintang Emas Utama -->
                    <polygon points="200,45 208,68 232,68 213,82 220,105 200,91 180,105 187,82 168,68 192,68" fill="#ffd166" filter="drop-shadow(0 0 10px #ffd166)">
                        <animateTransform attributeName="transform" type="scale" values="1;1.08;1" origin="200 95" dur="3s" repeatCount="indefinite"/>
                    </polygon>
                    <!-- Teks Sumpah Integritas Mahasiswa -->
                    <text x="200" y="145" fill="#ffffff" font-size="10" font-family="'Cinzel', serif" font-weight="bold" text-anchor="middle" letter-spacing="1">INDONESIA EMAS 2045</text>
                    <text x="200" y="165" fill="#a8dadc" font-size="6.5" text-anchor="middle">Konstitusi yang Hidup Adalah Konstitusi yang Diamalkan</text>
                    <text x="200" y="195" fill="#e63946" font-size="8" font-weight="bold" text-anchor="middle">SEKIAN & TERIMA KASIH • SESI TANYA JAWAB</text>
                </svg>
            """
        }
    }
    
    v = videos.get(slide_id, videos[0])
    
    return f'''
        <div style="background: rgba(16, 29, 66, 0.7); border: 1px solid rgba(255, 209, 102, 0.35); border-radius: 14px; padding: 16px; margin-top: 18px; box-shadow: 0 10px 25px rgba(0,0,0,0.4);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="background: {v['badge_color']}; color: #ffffff; font-size: 0.72rem; font-weight: 800; padding: 3px 10px; border-radius: 999px; letter-spacing: 0.8px;">
                    ▶️ {v['tag']}
                </span>
                <span style="color: #ffd166; font-size: 0.75rem; font-weight: 700;">
                    ⏱️ {v['time']}
                </span>
            </div>
            <div style="width: 100%; border-radius: 10px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); background: #000000; line-height: 0;">
                {v['svg']}
            </div>
            <div style="margin-top: 10px;">
                <p style="color: #ffffff; font-size: 0.88rem; font-weight: 700; margin: 0 0 4px 0; font-family: 'Cinzel', serif;">
                    🎬 {v['title']}
                </p>
                <p style="color: #a8dadc; font-size: 0.78rem; margin: 0; line-height: 1.5;">
                    {v['desc']}
                </p>
            </div>
        </div>
    '''


# 15 Slides Definition
SLIDES = [
    {
        "id": 0,
        "badge": "COVER PRESENTASI • MATA KULIAH PENDIDIKAN PANCASILA",
        "title": "DINAMIKA PELAKSANAAN UUD 1945",
        "subtitle": "Kajian Historis, Yuridis, dan Sosiologis Perjalanan Konstitusi Negara Kesatuan Republik Indonesia",
        "type": "cover"
    },
    {
        "id": 1,
        "badge": "AGENDA & PETA KONSEP • 15 MENU SLIDE",
        "title": "PETA STRUKTUR PEMBAHASAN",
        "subtitle": "Alur Menyeluruh Dinamika Konstitusi Indonesia dari Awal Kemerdekaan Hingga Era Kontemporer",
        "type": "agenda"
    },
    {
        "id": 2,
        "badge": "PONDASI KONSTITUSI • HUKUM DASAR TERTINGGI",
        "title": "HAKIKAT & KEDUDUKAN UUD 1945",
        "subtitle": "UUD 1945 sebagai Staatsfundamentalnorm dan Sumber dari Segala Sumber Hukum Nasional",
        "type": "content"
    },
    {
        "id": 3,
        "badge": "PERIODE I • 18 AGUSTUS 1945 - 27 DESEMBER 1949",
        "title": "UUD 1945 ERA AWAL KEMERDEKAAN",
        "subtitle": "Pengesahan oleh PPKI, Penerapan Awal, dan Pergeseran ke Sistem Parlementer",
        "type": "content"
    },
    {
        "id": 4,
        "badge": "ANALISIS KRITIS • TANTANGAN AWAL KEMERDEKAAN",
        "title": "DINAMIKA & PENYIMPANGAN AWAL",
        "subtitle": "Maklumat No. X 1945 dan Maklumat 14 November 1945 Mengubah Desain Konstitusional",
        "type": "content"
    },
    {
        "id": 5,
        "badge": "PERIODE II • 27 DESEMBER 1949 - 17 AGUSTUS 1950",
        "title": "KONSTITUSI REPUBLIK INDONESIA SERIKAT (RIS)",
        "subtitle": "Konferensi Meja Bundar (KMB) dan Transformasi dari Negara Kesatuan Menjadi Federal",
        "type": "content"
    },
    {
        "id": 6,
        "badge": "INTEGRASI BANGSA • PERIODE RIS 1949-1950",
        "title": "TUNTUTAN KEMBALI KE NEGARA KESATUAN",
        "subtitle": "Kegagalan Desain Federalisme Belanda dan Mosi Integral Mohammad Natsir",
        "type": "content"
    },
    {
        "id": 7,
        "badge": "PERIODE III • 17 AGUSTUS 1950 - 5 JULI 1959",
        "title": "UUD SEMENTARA (UUDS) 1950 & DEMOKRASI LIBERAL",
        "subtitle": "Sistem Multi-Partai Ekstrem, Jatuh Bangun 7 Kabinet, dan Sukses Pemilu 1955",
        "type": "content"
    },
    {
        "id": 8,
        "badge": "TITIK BALIK SEJARAH • 5 JULI 1959",
        "title": "KEBUNTUAN KONSTITUANTE & DEKRIT PRESIDEN",
        "subtitle": "Kegagalan Merumuskan UUD Definitif dan Penyelamatan Negara Melalui Staatsnoodrecht",
        "type": "content"
    },
    {
        "id": 9,
        "badge": "PERIODE IV • 1959 - 1966",
        "title": "UUD 1945 MASA ORDE LAMA (DEMOKRASI TERPIMPIN)",
        "subtitle": "Sentralisasi Kekuasaan Eksekutif, Manipol USDEK, dan Pelanggaran Norma Konstitusi",
        "type": "content"
    },
    {
        "id": 10,
        "badge": "PERIODE V • 1966 - 1998",
        "title": "UUD 1945 MASA ORDE BARU (DEMOKRASI PANCASILA)",
        "subtitle": "Tekad Pelaksanaan Murni & Konsekuen Berujung pada Sakralisasi dan Hegemoni Eksekutif",
        "type": "content"
    },
    {
        "id": 11,
        "badge": "PERIODE VI • ERA REFORMASI 1999 - 2002",
        "title": "GELOMBANG AMANDEMEN UUD 1945",
        "subtitle": "Empat Tahap Perubahan UUD 1945 dan 5 Kesepakatan Dasar Fraksi MPR RI",
        "type": "content"
    },
    {
        "id": 12,
        "badge": "RESTRUKTURISASI KETATANEGARAAN • PASCA AMANDEMEN",
        "title": "IMPLIKASI HUKUM & LEMBAGA NEGARA BARU",
        "subtitle": "Lahirnya MK, DPD, KY, Pembatasan Jabatan Presiden, dan Bab Khusus Hak Asasi Manusia",
        "type": "content"
    },
    {
        "id": 13,
        "badge": "TANTANGAN MODERN • DISRUPSI & TATA KELOLA",
        "title": "DINAMIKA KONSTITUSI DI ERA KONTEMPORER",
        "subtitle": "Ujian Independensi Peradilan, Demokrasi Digital, Polarisasi, dan Meaningful Participation",
        "type": "content"
    },
    {
        "id": 14,
        "badge": "KESIMPULAN & REFLEKSI • PENDIDIKAN PANCASILA",
        "title": "REFLEKSI NILAI PANCASILA & PENUTUP",
        "subtitle": "Menjaga Konstitusi sebagai Jiwa Bangsa Menuju Indonesia Emas 2045",
        "type": "content"
    }
]

# Helper SVG Generator for Replicas & Animations
def get_svg_garuda():
    return """
    <svg width="140" height="140" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" class="cover-garuda">
        <circle cx="50" cy="50" r="46" stroke="#ffd166" stroke-width="1.5" stroke-dasharray="4 2" opacity="0.6"/>
        <circle cx="50" cy="50" r="40" fill="radial-gradient(circle, #e63946 0%, #101d42 85%)" opacity="0.4"/>
        <path d="M50 15 L58 35 L78 35 L62 48 L68 68 L50 56 L32 68 L38 48 L22 35 L42 35 Z" fill="#ffd166" filter="drop-shadow(0 0 8px #ffd166)"/>
        <rect x="42" y="44" width="16" height="18" rx="2" fill="#e63946" stroke="#ffffff" stroke-width="1.2"/>
        <path d="M42 53 H58" stroke="#ffffff" stroke-width="1.2"/>
        <circle cx="50" cy="53" r="2.5" fill="#ffd166"/>
        <path d="M30 78 C40 73 60 73 70 78" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
        <text x="50" y="87" fill="#ffd166" font-size="5.5" font-weight="bold" text-anchor="middle" letter-spacing="0.5">BHINNEKA TUNGGAL IKA</text>
    </svg>
    """

def get_svg_timbangan():
    return """
    <svg width="180" height="150" viewBox="0 0 100 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M50 10 L50 65" stroke="#ffd166" stroke-width="3" stroke-linecap="round"/>
        <path d="M30 65 L70 65" stroke="#ffd166" stroke-width="3.5" stroke-linecap="round"/>
        <path d="M50 14 L20 22 M50 14 L80 22" stroke="#e63946" stroke-width="2" stroke-linecap="round"/>
        <circle cx="50" cy="14" r="3.5" fill="#ffd166"/>
        <path d="M20 22 L12 42 M20 22 L28 42" stroke="#a8dadc" stroke-width="1"/>
        <path d="M80 22 L72 42 M80 22 L88 42" stroke="#a8dadc" stroke-width="1"/>
        <path d="M10 42 C10 48 30 48 30 42 Z" fill="#ffd166" opacity="0.8"/>
        <path d="M70 42 C70 48 90 48 90 42 Z" fill="#ffd166" opacity="0.8"/>
        <text x="50" y="75" fill="#a8dadc" font-size="5" text-anchor="middle" font-weight="bold">SUPREMASI HUKUM</text>
    </svg>
    """

def get_svg_dekrit():
    return """
    <svg width="170" height="160" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="20" y="10" width="60" height="80" rx="4" fill="#f8edeb" stroke="#ffd166" stroke-width="2"/>
        <line x1="28" y1="22" x2="72" y2="22" stroke="#e63946" stroke-width="2.5"/>
        <line x1="32" y1="30" x2="68" y2="30" stroke="#1d3557" stroke-width="1.5"/>
        <line x1="28" y1="38" x2="72" y2="38" stroke="#457b9d" stroke-width="1.2"/>
        <line x1="28" y1="45" x2="72" y2="45" stroke="#457b9d" stroke-width="1.2"/>
        <line x1="28" y1="52" x2="72" y2="52" stroke="#457b9d" stroke-width="1.2"/>
        <line x1="28" y1="59" x2="55" y2="59" stroke="#457b9d" stroke-width="1.2"/>
        <circle cx="50" cy="74" r="9" fill="#e63946" opacity="0.85"/>
        <path d="M47 74 L49 76 L54 71" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/>
        <text x="50" y="97" fill="#ffd166" font-size="5.5" font-weight="bold" text-anchor="middle">5 JULI 1959</text>
    </svg>
    """

def get_svg_parliament():
    return """
    <svg width="180" height="140" viewBox="0 0 100 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 30 C20 18 80 18 80 30 Z" fill="#ffd166" opacity="0.75"/>
        <rect x="15" y="30" width="70" height="5" fill="#e63946"/>
        <rect x="22" y="35" width="4" height="28" fill="#ffffff" opacity="0.9"/>
        <rect x="36" y="35" width="4" height="28" fill="#ffffff" opacity="0.9"/>
        <rect x="50" y="35" width="4" height="28" fill="#ffffff" opacity="0.9"/>
        <rect x="64" y="35" width="4" height="28" fill="#ffffff" opacity="0.9"/>
        <rect x="74" y="35" width="4" height="28" fill="#ffffff" opacity="0.9"/>
        <rect x="12" y="63" width="76" height="7" fill="#1d3557" stroke="#ffd166" stroke-width="1"/>
        <text x="50" y="77" fill="#a8dadc" font-size="5" text-anchor="middle" font-weight="bold">GEDUNG PARLEMEN / DPR-MPR</text>
    </svg>
    """

def get_svg_amendments():
    return """
    <svg width="190" height="150" viewBox="0 0 100 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="40" r="14" fill="#e63946" stroke="#ffd166" stroke-width="1.5"/>
        <text x="50" y="42" fill="#ffffff" font-size="4" font-weight="bold" text-anchor="middle">UUD 1945</text>
        <!-- 4 Nodes -->
        <circle cx="20" cy="20" r="9" fill="#1d3557" stroke="#ffd166" stroke-width="1"/>
        <text x="20" y="21.5" fill="#ffd166" font-size="3.5" font-weight="bold" text-anchor="middle">1999</text>
        <circle cx="80" cy="20" r="9" fill="#1d3557" stroke="#ffd166" stroke-width="1"/>
        <text x="80" y="21.5" fill="#ffd166" font-size="3.5" font-weight="bold" text-anchor="middle">2000</text>
        <circle cx="20" cy="60" r="9" fill="#1d3557" stroke="#ffd166" stroke-width="1"/>
        <text x="20" y="61.5" fill="#ffd166" font-size="3.5" font-weight="bold" text-anchor="middle">2001</text>
        <circle cx="80" cy="60" r="9" fill="#1d3557" stroke="#ffd166" stroke-width="1"/>
        <text x="80" y="61.5" fill="#ffd166" font-size="3.5" font-weight="bold" text-anchor="middle">2002</text>
        <!-- Lines -->
        <line x1="28" y1="25" x2="40" y2="33" stroke="#ffd166" stroke-width="1" stroke-dasharray="2 1"/>
        <line x1="72" y1="25" x2="60" y2="33" stroke="#ffd166" stroke-width="1" stroke-dasharray="2 1"/>
        <line x1="28" y1="55" x2="40" y2="47" stroke="#ffd166" stroke-width="1" stroke-dasharray="2 1"/>
        <line x1="72" y1="55" x2="60" y2="47" stroke="#ffd166" stroke-width="1" stroke-dasharray="2 1"/>
        <text x="50" y="75" fill="#a8dadc" font-size="4.8" font-weight="bold" text-anchor="middle">4 TAHAP AMANDEMEN</text>
    </svg>
    """


# Navigation Callbacks for 100% Reliability
def next_slide():
    if st.session_state.slide < len(SLIDES) - 1:
        st.session_state.slide += 1

def prev_slide():
    if st.session_state.slide > 0:
        st.session_state.slide -= 1

def jump_to_slide(i):
    st.session_state.slide = i

def on_sidebar_change():
    st.session_state.slide = st.session_state.sidebar_picker

def on_bottom_change():
    st.session_state.slide = st.session_state.bottom_picker

# ==========================================
# SIDEBAR NAVIGATION & TEAM PROFILE
# ==========================================
with st.sidebar:
    render_html("""
        <div style="text-align: center; padding: 12px 0;">
            <div style="font-size: 2.2rem; margin-bottom: 6px;">🏛️ 🇮🇩</div>
            <h3 style="color: #ffd166; margin: 0; font-family: 'Cinzel', serif; font-size: 1.15rem;">DINAMIKA UUD 1945</h3>
            <p style="color: #a8dadc; font-size: 0.8rem; margin-top: 4px;">Pendidikan Pancasila Berbasis Web</p>
        </div>
    """)
    
    render_html("---")
    
    # Slide Selection
    slide_titles = [f"{i+1}. {s['title'][:28]}..." for i, s in enumerate(SLIDES)]
    st.selectbox(
        "📑 Pilih Halaman Menu:",
        options=range(len(SLIDES)),
        format_func=lambda x: slide_titles[x],
        index=st.session_state.slide,
        key="sidebar_picker",
        on_change=on_sidebar_change
    )

    # Progress bar
    progress = (st.session_state.slide + 1) / len(SLIDES)
    st.progress(progress)
    st.caption(f"📍 Halaman {st.session_state.slide + 1} dari 15 Menu Slide")

    st.markdown("---")
    
    # Team Roster in Sidebar
    render_html("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px;">
            <p style="color: #ffd166; font-size: 0.82rem; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">👥 Anggota Kelompok:</p>
            <ol style="color: #f1faee; font-size: 0.78rem; padding-left: 18px; margin: 0; line-height: 1.8;">
                <li><b>RANDI PRASETYO</b></li>
                <li><b>M. SAID HAYKAL</b></li>
                <li><b>RAGIL PRAKHOSO</b></li>
                <li><b>M. SYAUQI ALFA ILLIYIN</b></li>
                <li><b>HARLAND RAMADHAN</b></li>
                <li><b>DAFFA DWI AMANDA</b></li>
            </ol>
        </div>
    """)

    render_html("---")
    
    # Speaker Notes Toggle
    st.session_state.show_notes = st.toggle("🎙️ Tampilkan Catatan Presenter", value=st.session_state.show_notes)
    
    # Quick Timeline Jump
    render_html("<p style='font-size: 0.8rem; font-weight: 700; color: #a8dadc; margin-top: 10px;'>⚡ Pintasan Periode:</p>")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.button("🇮🇩 1945-1949", on_click=jump_to_slide, args=(3,), key="btn_p1", use_container_width=True)
        st.button("⚖️ UUDS 1950", on_click=jump_to_slide, args=(7,), key="btn_p3", use_container_width=True)
        st.button("🦅 Orde Baru", on_click=jump_to_slide, args=(10,), key="btn_p5", use_container_width=True)
    with col_sb2:
        st.button("🌐 RIS 1949", on_click=jump_to_slide, args=(5,), key="btn_p2", use_container_width=True)
        st.button("📜 Orde Lama", on_click=jump_to_slide, args=(9,), key="btn_p4", use_container_width=True)
        st.button("✨ Reformasi", on_click=jump_to_slide, args=(11,), key="btn_p6", use_container_width=True)

# ==========================================
# MAIN SLIDE DISPLAY LOGIC
# ==========================================

curr = SLIDES[st.session_state.slide]

# TOP PROGRESS INDICATOR BAR
col_nav_l, col_nav_m, col_nav_r = st.columns([1, 4, 1])
with col_nav_l:
    st.button("◀️ Mundur", disabled=(st.session_state.slide == 0), on_click=prev_slide, key="btn_top_prev", use_container_width=True)
with col_nav_m:
    render_html(f"""
        <div style="text-align: center; padding: 4px;">
            <span style="background: rgba(230, 57, 70, 0.2); border: 1px solid rgba(230, 57, 70, 0.4); color: #ffd166; font-size: 0.85rem; font-weight: 700; padding: 4px 18px; border-radius: 999px;">
                SLIDE {st.session_state.slide + 1} / 15: {curr['title']}
            </span>
        </div>
    """)
with col_nav_r:
    st.button("Maju ▶️", disabled=(st.session_state.slide == len(SLIDES) - 1), on_click=next_slide, key="btn_top_next", use_container_width=True)

# SLIDE CONTENT CONTAINER
render_html('<div class="slide-wrapper">')

# ----------------------------------------------------
# SLIDE 1: COVER / HALAMAN UTAMA
# ----------------------------------------------------
if curr["id"] == 0:
    render_html(f"""
        <div class="cover-hero">
            {get_svg_garuda()}
            <div class="slide-badge">MATA KULIAH PENDIDIKAN PANCASILA & KEWARGANEGARAAN</div>
            <h1 class="cover-main-title">DINAMIKA PELAKSANAAN UUD 1945</h1>
            <p class="cover-tagline">
                Menelusuri Perjalanan Historis, Bentuk Negara, Sistem Pemerintahan, Serta Dialektika Ketatanegaraan Republik Indonesia Menuju Demokrasi Konstitusional Berkeadilan
            </p>
            <div style="display: flex; justify-content: center; gap: 10px; margin-bottom: 24px;">
                <span class="badge-highlight">📜 UUD 1945 Awal</span>
                <span class="badge-highlight">🌐 Konstitusi RIS 1949</span>
                <span class="badge-highlight">⚖️ UUDS 1950</span>
                <span class="badge-highlight">🏛️ Orde Lama</span>
                <span class="badge-highlight">🦅 Orde Baru</span>
                <span class="badge-highlight">🇮🇩 Reformasi 1999-2002</span>
            </div>
            
            <p style="color: #ffd166; font-size: 0.95rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-top: 30px;">
                ✨ DISUSUN OLEH KELOMPOK:
            </p>
            
            <div class="member-grid">
                <div class="member-chip">
                    <div class="member-number">1</div>
                    <div>
                        <div class="member-name">RANDI PRASETYO</div>
                        <div class="member-role">Presenter & Analis Materi</div>
                    </div>
                </div>
                <div class="member-chip">
                    <div class="member-number">2</div>
                    <div>
                        <div class="member-name">M. SAID HAYKAL</div>
                        <div class="member-role">Presenter & Riset Sejarah</div>
                    </div>
                </div>
                <div class="member-chip">
                    <div class="member-number">4</div>
                    <div>
                        <div class="member-name">RAGIL PRAKHOSO</div>
                        <div class="member-role">Presenter & Kompilasi Regulasi</div>
                    </div>
                </div>
                <div class="member-chip">
                    <div class="member-number">5</div>
                    <div>
                        <div class="member-name">M. SYAUQI ALFA ILLIYIN</div>
                        <div class="member-role">Presenter & Analisis Amandemen</div>
                    </div>
                </div>
                <div class="member-chip">
                    <div class="member-number">6</div>
                    <div>
                        <div class="member-name">HARLAND RAMADHAN</div>
                        <div class="member-role">Presenter & Telaah Kasus Modern</div>
                    </div>
                </div>
                <div class="member-chip">
                    <div class="member-number">7</div>
                    <div>
                        <div class="member-name">DAFFA DWI AMANDA</div>
                        <div class="member-role">Presenter & Sintesis Refleksi</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 40px;">
                <p style="font-size: 0.85rem; color: #a8dadc;">Gunakan tombol navigasi di atas/bawah atau menu di samping untuk berpindah antar slide presentasi.</p>
            </div>
        </div>
    """)

# ----------------------------------------------------
# SLIDE 2: DAFTAR ISI / AGENDA 15 SLIDE
# ----------------------------------------------------
elif curr["id"] == 1:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_ag1, col_ag2, col_ag3 = st.columns(3)
    with col_ag1:
        render_html("""
            <div class="content-card">
                <div class="card-icon">1️⃣</div>
                <div class="card-title">Fase Fondasi & Awal (1945)</div>
                <div class="card-text">
                    • <b>Slide 1:</b> Cover & Susunan Kelompok<br>
                    • <b>Slide 2:</b> Agenda Pembahasan<br>
                    • <b>Slide 3:</b> Hakikat & Kedudukan UUD 1945<br>
                    • <b>Slide 4:</b> Periode I: UUD 1945 Awal Kemerdekaan<br>
                    • <b>Slide 5:</b> Analisis Kritis & Maklumat 1945
                </div>
            </div>
        """)
    with col_ag2:
        render_html("""
            <div class="content-card">
                <div class="card-icon">2️⃣</div>
                <div class="card-title">Fase Turbulensi (1949-1959)</div>
                <div class="card-text">
                    • <b>Slide 6:</b> Periode II: Konstitusi RIS 1949<br>
                    • <b>Slide 7:</b> Dinamika Tuntutan Kembali ke NKRI<br>
                    • <b>Slide 8:</b> Periode III: UUDS 1950 & Demokrasi Liberal<br>
                    • <b>Slide 9:</b> Kebuntuan Konstituante & Dekrit 5 Juli 1959<br>
                    • <b>Slide 10:</b> Periode IV: Demokrasi Terpimpin (Orla)
                </div>
            </div>
        """)
    with col_ag3:
        render_html("""
            <div class="content-card">
                <div class="card-icon">3️⃣</div>
                <div class="card-title">Fase Orba & Reformasi (1966-Kini)</div>
                <div class="card-text">
                    • <b>Slide 11:</b> Periode V: UUD 1945 Masa Orde Baru<br>
                    • <b>Slide 12:</b> Periode VI: 4 Tahap Amandemen 1999-2002<br>
                    • <b>Slide 13:</b> Implikasi Lembaga Baru & HAM<br>
                    • <b>Slide 14:</b> Tantangan Konstitusi Kontemporer<br>
                    • <b>Slide 15:</b> Refleksi Nilai Pancasila & Penutup
                </div>
            </div>
        """)
    
    render_html("""
        <div class="quote-box">
            💡 <b>Catatan Analitis:</b> Dinamika UUD 1945 bukanlah sekadar pergantian teks hukum formal, melainkan dialektika mencari keseimbangan antara stabilitas pemerintahan, kedaulatan rakyat, dan kemurnian cita-cita kemerdekaan bangsa Indonesia.
        </div>
    """)

# ----------------------------------------------------
# SLIDE 3: HAKIKAT & KEDUDUKAN UUD 1945
# ----------------------------------------------------
elif curr["id"] == 2:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s3_l, col_s3_r = st.columns([3, 2])
    with col_s3_l:
        render_html("""
            <div class="card-grid">
                <div class="content-card">
                    <div class="card-icon">📜</div>
                    <div class="card-title">Hukum Dasar Tertinggi</div>
                    <div class="card-text">
                        UUD 1945 menempati puncak hierarki tata perundang-undangan Indonesia (sesuai UU No. 12 Tahun 2011). Setiap undang-undang dan peraturan di bawahnya tidak boleh bertentangan dengan norma konstitusi.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">⭐</div>
                    <div class="card-title">Staatsfundamentalnorm</div>
                    <div class="card-text">
                        <b>Pembukaan UUD 1945</b> memuat kaidah pokok fundamental negara yang tidak dapat diubah oleh siapapun, termasuk MPR hasil pemilu, karena mengubahnya sama halnya membubarkan negara proklamasi.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">⚖️</div>
                    <div class="card-title">Fungsi Pembatas Kekuasaan</div>
                    <div class="card-text">
                        Prinsip konstitusionalisme bertujuan membatasi kesewenang-wenangan penguasa, menjamin hak asasi warga negara, serta membagi kekuasaan negara secara berimbang (*checks and balances*).
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">🇮🇩</div>
                    <div class="card-title">Jiwa dan Falsafah Bangsa</div>
                    <div class="card-text">
                        UUD 1945 adalah manifestasi yuridis dari <b>Pancasila</b>. Setiap pasal dalam batang tubuh merupakan penjabaran nilai ketuhanan, kemanusiaan, persatuan, kerakyatan, dan keadilan sosial.
                    </div>
                </div>
            </div>
        """)
    with col_s3_r:
        render_html(f"""
            <div class="replica-graphic-box">
                {get_svg_timbangan()}
                <h4 style="color: #ffd166; margin-top: 14px;">PRINSIP SUPREMASI HUKUM</h4>
                <p style="font-size: 0.85rem; color: #e2e8f0; line-height: 1.5;">
                    <i>"Negara Indonesia adalah negara hukum (Rechtsstaat), bukan negara berdasarkan kekuasaan belaka (Machtsstaat)."</i>
                </p>
                <div style="margin-top: 10px; width: 100%; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px;">
                    <span class="badge-highlight">Pasal 1 Ayat (2)</span>
                    <span class="badge-highlight">Pasal 1 Ayat (3)</span>
                </div>
            </div>
        """)

# ----------------------------------------------------
# SLIDE 4: PERIODE I (18 AGUSTUS 1945 - 27 DES 1949)
# ----------------------------------------------------
elif curr["id"] == 3:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s4_1, col_s4_2 = st.columns([3, 2])
    with col_s4_1:
        render_html("""
            <div class="card-grid">
                <div class="content-card">
                    <div class="card-icon">🏛️</div>
                    <div class="card-title">Pengesahan Dokumen Konstitusi</div>
                    <div class="card-text">
                        Pada <b>18 Agustus 1945</b>, Panitia Persiapan Kemerdekaan Indonesia (PPKI) menetapkan dan mengesahkan UUD 1945, memilih Ir. Soekarno sebagai Presiden dan Drs. Mohammad Hatta sebagai Wakil Presiden.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">📜</div>
                    <div class="card-title">Aturan Peralihan Pasal IV</div>
                    <div class="card-text">
                        Sebelum MPR, DPR, dan DPA dibentuk menurut UUD, segala kekuasaan dijalankan oleh <b>Presiden</b> dengan bantuan sebuah <b>Komite Nasional (KNIP)</b> untuk mencegah kekosongan hukum darurat.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">🔄</div>
                    <div class="card-title">Sistem Pemerintahan Awal</div>
                    <div class="card-text">
                        Dirancang menganut sistem <b>Presidensial</b> murni di mana menteri bertanggung jawab kepada Presiden, dengan struktur yang lugas dan fleksibel (terdiri atas 37 pasal).
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">⚔️</div>
                    <div class="card-title">Situasi Perang Kemerdekaan</div>
                    <div class="card-text">
                        UUD 1945 belum dapat dilaksanakan secara menyeluruh karena segenap daya bangsa dicurahkan untuk mempertahankan kemerdekaan dari Agresi Militer Belanda I & II.
                    </div>
                </div>
            </div>
        """)
    with col_s4_2:
        render_html(f"""
            <div class="replica-graphic-box">
                {get_svg_parliament()}
                <h4 style="color: #ffd166; margin-top: 14px;">STRUKTUR KEKUASAAN TRANSISIONAL</h4>
                <div style="text-align: left; font-size: 0.85rem; color: #f1faee; line-height: 1.7; width: 100%;">
                    🔹 <b>Kepala Negara & Pemerintahan:</b> Presiden Ir. Soekarno<br>
                    🔹 <b>Wakil Presiden:</b> Drs. Mohammad Hatta<br>
                    🔹 <b>Badan Pembantu Legislatif:</b> KNIP (Kasman Singodimedjo)<br>
                    🔹 <b>Ibukota Sempat Pindah:</b> Jakarta ke Yogyakarta (1946)
                </div>
            </div>
        """)

# ----------------------------------------------------
# SLIDE 5: DINAMIKA & PENYIMPANGAN PERIODE I
# ----------------------------------------------------
elif curr["id"] == 4:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s5_1, col_s5_2, col_s5_3 = st.columns(3)
    with col_s5_1:
        render_html("""
            <div class="content-card" style="border-top: 3px solid #e63946;">
                <div class="card-icon">📄</div>
                <div class="card-title">Maklumat Wakil Presiden No. X</div>
                <div class="card-text">
                    <b>Tanggal: 16 Oktober 1945</b><br>
                    Mengubah kedudukan KNIP dari sekadar pembantu presiden menjadi badan yang diserahi <b>kekuasaan legislatif</b> dan ikut menetapkan GBHN bersama Presiden sebelum terbentuknya DPR/MPR.
                </div>
            </div>
        """)
    with col_s5_2:
        render_html("""
            <div class="content-card" style="border-top: 3px solid #ffd166;">
                <div class="card-icon">👥</div>
                <div class="card-title">Maklumat Pemerintah 3 Nov 1945</div>
                <div class="card-text">
                    <b>Anjuran Pembentukan Partai Politik</b><br>
                    Dikeluarkan guna mempertegas citra Indonesia sebagai negara demokratis di mata dunia internasional, memicu lahirnya sistem multi-partai yang sangat dinamis.
                </div>
            </div>
        """)
    with col_s5_3:
        render_html("""
            <div class="content-card" style="border-top: 3px solid #06d6a0;">
                <div class="card-icon">🔄</div>
                <div class="card-title">Maklumat 14 November 1945</div>
                <div class="card-text">
                    <b>Peralihan ke Sistem Parlementer</b><br>
                    Pertanggungjawaban menteri dialihkan dari Presiden kepada Parlemen/Badan Pekerja KNIP. Sutan Sjahrir diangkat menjadi Perdana Menteri pertama RI.
                </div>
            </div>
        """)
        
    render_html("""
        <div class="quote-box">
            ⚠️ <b>Telaah Konstitusional:</b> Terjadi pergeseran konstitusional (constitutional convention) dari sistem <b>Presidensial</b> ke sistem <b>Parlementer</b> tanpa melalui amandemen teks resmi UUD 1945. Hal ini merupakan strategi diplomatik meyakinkan Sekutu bahwa Indonesia bukan negara fasis bentukan Jepang.
        </div>
    """)

# ----------------------------------------------------
# SLIDE 6: PERIODE II - KONSTITUSI RIS 1949
# ----------------------------------------------------
elif curr["id"] == 5:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s6_l, col_s6_r = st.columns([3, 2])
    with col_s6_l:
        render_html("""
            <div class="card-grid">
                <div class="content-card">
                    <div class="card-icon">🤝</div>
                    <div class="card-title">Konferensi Meja Bundar (KMB)</div>
                    <div class="card-text">
                        Hasil kesepakatan KMB di Den Haag (23 Ags - 2 Nov 1949) memaksa Belanda mengakui kedaulatan Indonesia dengan syarat pembentukan negara federasi <b>Republik Indonesia Serikat (RIS)</b>.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">🗺️</div>
                    <div class="card-title">Negara Federasi / Serikat</div>
                    <div class="card-text">
                        Wilayah RI terbagi menjadi 7 Negara Bagian (seperti Negara Pasundan, Negara Indonesia Timur, Negara Madura) dan 9 Satuan Kenegaraan otonom. Republik Indonesia (Yogyakarta) hanya berstatus salah satu negara bagian.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">🏛️</div>
                    <div class="card-title">Sistem Parlementer Semu</div>
                    <div class="card-text">
                        Menganut sistem parlementer kabinet semu (<i>Quasi-Parlementer</i>). Kabinet dipimpin oleh Perdana Menteri (Mohammad Hatta) yang bertanggung jawab kepada Parlemen (DPR dan Senat RIS).
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">👑</div>
                    <div class="card-title">Kedudukan Presiden RIS</div>
                    <div class="card-text">
                        Ir. Soekarno dipilih sebagai Presiden RIS, berkedudukan sebagai Kepala Negara yang tidak dapat diganggu gugat, sementara kekuasaan pemerintahan dijalankan oleh kabinet.
                    </div>
                </div>
            </div>
        """)
    with col_s6_r:
        render_html("""
            <div class="replica-graphic-box">
                <div style="font-size: 2.8rem; margin-bottom: 8px;">🌐 🧩</div>
                <h4 style="color: #ffd166;">REPUBLIK INDONESIA SERIKAT</h4>
                <p style="font-size: 0.85rem; color: #a8dadc; margin-bottom: 12px;">27 Desember 1949 – 17 Agustus 1950</p>
                <div style="text-align: left; font-size: 0.82rem; color: #e2e8f0; width: 100%;">
                    🚩 <b>Bentuk Negara:</b> Federal / Serikat<br>
                    🚩 <b>Konstitusi:</b> Konstitusi RIS 1949<br>
                    🚩 <b>Lembaga Legislatif:</b> DPR RIS & Senat RIS<br>
                    🚩 <b>Perdana Menteri:</b> Drs. Mohammad Hatta<br>
                    🚩 <b>Taktik Penjajah:</b> Politik Devide et Impera
                </div>
            </div>
        """)

# ----------------------------------------------------
# SLIDE 7: DINAMIKA & PENOLAKAN NEGARA RIS
# ----------------------------------------------------
elif curr["id"] == 6:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    render_html("""
        <div class="card-grid">
            <div class="content-card">
                <div class="card-icon">❌</div>
                <div class="card-title">Penolakan Bentuk Federal</div>
                <div class="card-text">
                    Rakyat di berbagai negara bagian menganggap bentuk federal hanyalah rekayasa kolonial Belanda untuk memecah belah persatuan bangsa. Muncul aksi demonstrasi menuntut pembubaran negara boneka.
                </div>
            </div>
            <div class="content-card">
                <div class="card-icon">📜</div>
                <div class="card-title">Mosi Integral Mohammad Natsir</div>
                <div class="card-text">
                    Pada <b>3 April 1950</b>, Fraksi Masyumi melalui Mohammad Natsir memprakarsai <i>Mosi Integral</i> di parlemen RIS, mengajak seluruh negara bagian melebur kembali ke pangkuan Negara Kesatuan Republik Indonesia.
                </div>
            </div>
            <div class="content-card">
                <div class="card-icon">🇮🇩</div>
                <div class="card-title">Proklamasi Kembali ke NKRI</div>
                <div class="card-text">
                    Pada <b>17 Agustus 1950</b>, tepat HUT RI ke-5, Presiden Soekarno mengumumkan pembubaran RIS dan kembalinya bentuk Negara Kesatuan Republik Indonesia dengan memberlakukan UUDS 1950.
                </div>
            </div>
        </div>
        
        <div class="quote-box" style="margin-top: 24px;">
            💬 <b>Hikmah Sejarah:</b> Eksistensi Konstitusi RIS yang hanya bertahan selama <b>8 bulan</b> membuktikan bahwa konsep negara federal bertentangan dengan semangat Sumpah Pemuda 1928 dan jiwa persatuan Pancasila Sila ke-3.
        </div>
    """)

# ----------------------------------------------------
# SLIDE 8: PERIODE III - UUDS 1950 & DEMOKRASI LIBERAL
# ----------------------------------------------------
elif curr["id"] == 7:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s8_1, col_s8_2 = st.columns([3, 2])
    with col_s8_1:
        render_html("""
            <div class="card-grid">
                <div class="content-card">
                    <div class="card-icon">🔄</div>
                    <div class="card-title">Demokrasi Parlementer Liberal</div>
                    <div class="card-text">
                        Berdasarkan UUDS 1950, kabinet bertanggung jawab kepada Dewan Perwakilan Rakyat. Parlemen memiliki wewenang menjatuhkan kabinet melalui <b>Mosi Tidak Percaya</b>.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">⚡</div>
                    <div class="card-title">Ketidakstabilan Eksekutif</div>
                    <div class="card-text">
                        Terjadi pergantian <b>7 kabinet dalam rentang 9 tahun</b> (Kabinet Natsir, Sukiman, Wilopo, Ali Sastroamidjojo I, Burhanuddin Harahap, Ali Sastroamidjojo II, dan Djuanda). Rata-rata kabinet hanya bertahan 1 tahun.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">🗳️</div>
                    <div class="card-title">Prestasi Pemilu 1955</div>
                    <div class="card-text">
                        Berhasil menyelenggarakan Pemilu pertama yang paling demokratis, jujur, dan adil untuk memilih anggota DPR dan anggota Konstituante pembuat UUD tetap.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">⚠️</div>
                    <div class="card-title">Dampak Politik Sektoral</div>
                    <div class="card-text">
                        Program pembangunan jangka panjang terbengkalai akibat persaingan ideologis sengit antar partai politik, serta timbulnya pergolakan daerah (PRRI/Permesta).
                    </div>
                </div>
            </div>
        """)
    with col_s8_2:
        render_html("""
            <div class="replica-graphic-box">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">⏳ 🔄 ⚡</div>
                <h4 style="color: #ffd166;">KRONIK 7 KABINET UUDS 1950</h4>
                <div style="font-size: 0.8rem; text-align: left; color: #f1faee; width: 100%; line-height: 1.8;">
                    1. <b>Natsir</b> (Sep 1950 - Mar 1951)<br>
                    2. <b>Sukiman</b> (Apr 1951 - Feb 1952)<br>
                    3. <b>Wilopo</b> (Apr 1952 - Jun 1953)<br>
                    4. <b>Ali Sastroamidjojo I</b> (Jul 1953 - Jul 1955)<br>
                    5. <b>Burhanuddin Harahap</b> (Ags 1955 - Mar 1956)<br>
                    6. <b>Ali Sastroamidjojo II</b> (Mar 1956 - Mar 1957)<br>
                    7. <b>Djuanda / Karya</b> (Apr 1957 - Jul 1959)
                </div>
            </div>
        """)

# ----------------------------------------------------
# SLIDE 9: KEBUNTUAN KONSTITUANTE & DEKRIT PRESIDEN 1959
# ----------------------------------------------------
elif curr["id"] == 8:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s9_l, col_s9_r = st.columns([3, 2])
    with col_s9_l:
        render_html("""
            <div class="card-grid">
                <div class="content-card">
                    <div class="card-icon">🛑</div>
                    <div class="card-title">Kebuntuan Konstituante</div>
                    <div class="card-text">
                        Badan Konstituante hasil Pemilu 1955 gagal merumuskan konstitusi baru karena perselisihan tajam terkait <b>dasar negara</b> antara blok Nasionalis (Pancasila) dan blok Islam (Piagam Jakarta), tidak pernah mencapai kuorum 2/3 suara.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">🚨</div>
                    <div class="card-title">Ancaman Disintegrasi Bangsa</div>
                    <div class="card-text">
                        Kondisi keamanan nasional terancam parah dengan maraknya pemberontakan bersenjata di daerah dan mandeknya roda pemerintahan di pusat.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">📜</div>
                    <div class="card-title">Tiga Titah Dekrit 5 Juli 1959</div>
                    <div class="card-text">
                        1. <b>Pembubaran Badan Konstituante</b>.<br>
                        2. <b>Berlakunya kembali UUD 1945</b> dan tidak berlakunya UUDS 1950.<br>
                        3. <b>Pembentukan MPRS dan DPAS</b> dalam waktu sesingkat-singkatnya.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">⚖️</div>
                    <div class="card-title">Landasan Hukum Staatsnoodrecht</div>
                    <div class="card-text">
                        Dekrit Presiden diambil berdasar pada doktrin hukum darurat negara (<i>noodstaatsrecht</i>) demi menyelamatkan eksistensi Republik Indonesia dari kehancuran total.
                    </div>
                </div>
            </div>
        """)
    with col_s9_r:
        render_html(f"""
            <div class="replica-graphic-box">
                {get_svg_dekrit()}
                <h4 style="color: #ffd166; margin-top: 10px;">DEKRIT PRESIDEN 5 JULI 1959</h4>
                <p style="font-size: 0.85rem; color: #e2e8f0; line-height: 1.5;">
                    <i>"Kami Presiden Republik Indonesia/Panglima Tertinggi Angkatan Perang... dengan ini menyatakan berlakunya kembali Undang-Undang Dasar 1945..."</i>
                </p>
            </div>
        """)

# ----------------------------------------------------
# SLIDE 10: PERIODE IV - ORDE LAMA / DEMOKRASI TERPIMPIN
# ----------------------------------------------------
elif curr["id"] == 9:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    render_html("""
        <div class="card-grid">
            <div class="content-card" style="border-left: 4px solid #e63946;">
                <div class="card-icon">👑</div>
                <div class="card-title">Presiden Seumur Hidup</div>
                <div class="card-text">
                    Ketetapan MPRS No. III/MPRS/1963 mengangkat Ir. Soekarno sebagai <b>Presiden Seumur Hidup</b>. Ini bertentangan terang-terangan dengan Pasal 7 UUD 1945 asli yang membatasi masa jabatan presiden per 5 tahunan.
                </div>
            </div>
            <div class="content-card" style="border-left: 4px solid #e63946;">
                <div class="card-icon">🏛️</div>
                <div class="card-title">Pembubaran DPR Hasil Pemilu</div>
                <div class="card-text">
                    Tahun 1960, Presiden membubarkan DPR hasil Pemilu 1955 karena menolak menyetujui RAPBN yang diajukan pemerintah, lalu menggantinya secara sepihak dengan <b>DPR-Gotong Royong (DPR-GR)</b>.
                </div>
            </div>
            <div class="content-card" style="border-left: 4px solid #e63946;">
                <div class="card-icon">⚡</div>
                <div class="card-title">Perangkapan Jabatan & Subordinasi</div>
                <div class="card-text">
                    Ketua MPRS, Ketua DPR-GR, dan Ketua Mahkamah Agung (MA) diangkat berkedudukan setingkat Menteri Negara, sehingga lembaga yudikatif dan legislatif tersubordinasi di bawah eksekutif.
                </div>
            </div>
            <div class="content-card" style="border-left: 4px solid #e63946;">
                <div class="card-icon">🚩</div>
                <div class="card-title">Hegemoni Doktrin NASAKOM</div>
                <div class="card-text">
                    Penyeragaman ideologi melalui konsep Nasionalis, Agama, dan Komunis (NASAKOM) serta Manipol-USDEK, yang mengaburkan kemurnian falsafah Pancasila dan berujung pada tragedi G30S/PKI 1965.
                </div>
            </div>
        </div>
        
        <div class="quote-box">
            📌 <b>Kesimpulan Evaluatif:</b> Niat mulia kembali ke UUD 1945 terdistorsi menjadi sentralisme kekuasaan absolut pada figur pemimpin besar revolusi, mengabaikan mekanisme pembatasan kekuasaan (*constitutional limits*).
        </div>
    """)

# ----------------------------------------------------
# SLIDE 11: PERIODE V - UUD 1945 MASA ORDE BARU
# ----------------------------------------------------
elif curr["id"] == 10:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s11_1, col_s11_2 = st.columns([3, 2])
    with col_s11_1:
        render_html("""
            <div class="card-grid">
                <div class="content-card">
                    <div class="card-icon">🎯</div>
                    <div class="card-title">Semboyan Murni & Konsekuen</div>
                    <div class="card-text">
                        Orde Baru di bawah Presiden Soeharto lahir dengan komitmen melaksanakan Pancasila dan UUD 1945 secara murni dan konsekuen sebagai koreksi total terhadap penyimpangan Orde Lama.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">🔒</div>
                    <div class="card-title">Sakralisasi Dokumen Konstitusi</div>
                    <div class="card-text">
                        UUD 1945 disakralkan dan dianggap tabu untuk diubah. Diterbitkan UU No. 5 Tahun 1985 tentang Referendum yang menetapkan syarat yang nyaris mustahil untuk mengamandemen pasal UUD.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">🏛️</div>
                    <div class="card-title">Executive Heavy & Sentralisme</div>
                    <div class="card-text">
                        Kekuasaan Presiden menjadi terlampau dominan (<i>Executive Heavy</i>). Masa jabatan presiden tanpa batasan tegas memungkinkan kekuasaan otoriter bertahan selama <b>32 tahun</b>.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">📉</div>
                    <div class="card-title">Krisis Multidimensi & Tuntutan Reformasi</div>
                    <div class="card-text">
                        Monopoli tafsir Pancasila (Penataran P4), pembungkaman pers, dan lemahnya kontrol lembaga peradilan memicu krisis moneter dan gerakan Reformasi 1998 yang menuntut amandemen konstitusi.
                    </div>
                </div>
            </div>
        """)
    with col_s11_2:
        render_html("""
            <div class="replica-graphic-box">
                <div style="font-size: 2.8rem; margin-bottom: 8px;">🦅 🔒 📉</div>
                <h4 style="color: #ffd166;">KARAKTERISTIK ORDE BARU</h4>
                <div style="font-size: 0.82rem; text-align: left; color: #f1faee; width: 100%; line-height: 1.8;">
                    🔸 <b>Stabilitas Politik:</b> Ditekan lewat pendekatan keamanan<br>
                    🔸 <b>Fusi Partai:</b> Disederhanakan menjadi 3 fraksi (Golkar, PPP, PDI)<br>
                    🔸 <b>Dwi Fungsi ABRI:</b> Militer dominan di ranah sipil/birokrasi<br>
                    🔸 <b>Tafsir Tunggal:</b> Doktrin BP-7 & Pedoman P4<br>
                    🔸 <b>Akhir Era:</b> 21 Mei 1998 Lengsernya Soeharto
                </div>
            </div>
        """)

# ----------------------------------------------------
# SLIDE 12: PERIODE VI - ERA REFORMASI & 4 AMANDEMEN
# ----------------------------------------------------
elif curr["id"] == 11:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s12_l, col_s12_r = st.columns([3, 2])
    with col_s12_l:
        render_html("""
            <div class="card-grid">
                <div class="content-card">
                    <div class="card-icon">1️⃣</div>
                    <div class="card-title">Amandemen I (1999)</div>
                    <div class="card-text">
                        <b>Sidang Umum MPR 1999:</b> Membatasi kekuasaan Presiden, terutama masa jabatan maksimal 2 periode (Pasal 7), dan mengembalikan fungsi pembentukan UU ke tangan DPR (Pasal 20).
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">2️⃣</div>
                    <div class="card-title">Amandemen II (2000)</div>
                    <div class="card-text">
                        <b>Sidang Tahunan MPR 2000:</b> Mengatur Otonomi Daerah (Pasal 18), Penguatan fungsi DPR, pemisahan TNI dan POLRI (Pasal 30), serta pengadopsian piagam luas <b>Hak Asasi Manusia (Pasal 28A-28J)</b>.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">3️⃣</div>
                    <div class="card-title">Amandemen III (2001)</div>
                    <div class="card-text">
                        <b>Sidang Tahunan MPR 2001:</b> Penegasan kedaulatan rakyat melalui UUD, pembentukan lembaga baru <b>Mahkamah Konstitusi (MK)</b>, <b>Komisi Yudisial (KY)</b>, dan <b>Dewan Perwakilan Daerah (DPD)</b>.
                    </div>
                </div>
                <div class="content-card">
                    <div class="card-icon">4️⃣</div>
                    <div class="card-title">Amandemen IV (2002)</div>
                    <div class="card-text">
                        <b>Sidang Tahunan MPR 2002:</b> Pemilihan Presiden langsung oleh rakyat, penghapusan DPA, alokasi anggaran pendidikan minimal 20% APBN (Pasal 31), dan sistem perekonomian nasional (Pasal 33).
                    </div>
                </div>
            </div>
        """)
    with col_s12_r:
        render_html(f"""
            <div class="replica-graphic-box">
                {get_svg_amendments()}
                <h4 style="color: #ffd166; margin-top: 10px;">5 KESEPAKATAN DASAR AMANDEMEN</h4>
                <div style="font-size: 0.8rem; text-align: left; color: #e2e8f0; width: 100%; line-height: 1.6;">
                    1. Tidak mengubah Pembukaan UUD 1945.<br>
                    2. Tetap mempertahankan bentuk NKRI.<br>
                    3. Mempertegas sistem presidensial.<br>
                    4. Memasukkan penjelasan ke dalam pasal-pasal.<br>
                    5. Perubahan dilakukan secara adendum.
                </div>
            </div>
        """)

# ----------------------------------------------------
# SLIDE 13: RESTRUKTURISASI KELEMBAGAAN PASCA AMANDEMEN
# ----------------------------------------------------
elif curr["id"] == 12:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s13_1, col_s13_2, col_s13_3 = st.columns(3)
    with col_s13_1:
        render_html("""
            <div class="content-card" style="border-top: 3px solid #e63946;">
                <div class="card-icon">⚖️</div>
                <div class="card-title">Mahkamah Konstitusi (MK)</div>
                <div class="card-text">
                    Hadir sebagai <i>The Guardian of Constitution</i> dan pelindung hak asasi warga negara. Berwenang menguji UU terhadap UUD, memutus sengketa kewenangan lembaga negara, memutus pembubaran parpol, dan sengketa hasil Pemilu.
                </div>
            </div>
        """)
    with col_s13_2:
        render_html("""
            <div class="content-card" style="border-top: 3px solid #ffd166;">
                <div class="card-icon">🌐</div>
                <div class="card-title">Bikameral & DPD RI</div>
                <div class="card-text">
                    Parlemen bertransformasi menjadi bikameral lunak (<i>soft bicameralism</i>), di mana MPR terdiri atas anggota DPR (representasi politik rakyat) dan anggota DPD (representasi daerah kepulauan dan provinsi).
                </div>
            </div>
        """)
    with col_s13_3:
        render_html("""
            <div class="content-card" style="border-top: 3px solid #06d6a0;">
                <div class="card-icon">🛡️</div>
                <div class="card-title">Penguatan Piagam HAM</div>
                <div class="card-text">
                    Konstitusi kini memuat 10 pasal rincian HAM (Pasal 28A hingga 28J) yang menjamin hak hidup, berkeluarga, kepastian hukum yang adil, kebebasan berekspresi, hingga perlindungan dari diskriminasi.
                </div>
            </div>
        """)

    render_html("""
        <div class="content-card" style="margin-top: 20px;">
            <div class="card-title" style="color: #ffd166;">🔄 MATRIKS PERUBAHAN ANATOMI UUD 1945</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-top: 10px; font-size: 0.88rem;">
                <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px;">
                    <b style="color: #e63946;">Sebelum Amandemen:</b><br>
                    • 16 Bab<br>
                    • 37 Pasal<br>
                    • 49 Ayat<br>
                    • 4 Pasal Aturan Peralihan<br>
                    • 2 Ayat Aturan Tambahan<br>
                    • Disertai Penjelasan Resmi
                </div>
                <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px;">
                    <b style="color: #06d6a0;">Setelah 4 Amandemen:</b><br>
                    • 21 Bab (bertambah 5 bab)<br>
                    • 73 Pasal (bertambah 36 pasal)<br>
                    • 170 Ayat (bertambah 121 ayat)<br>
                    • 3 Pasal Aturan Peralihan<br>
                    • 2 Pasal Aturan Tambahan<br>
                    • Tanpa Bagian Penjelasan (masuk pasal)
                </div>
                <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px;">
                    <b style="color: #ffd166;">Prinsip Kekuasaan:</b><br>
                    • Tidak ada lagi "Lembaga Tertinggi Negara"<br>
                    • Hubungan antar lembaga sejajar koordinatif<br>
                    • Checks and balances aktif<br>
                    • Pemilu langsung Presiden & Kepala Daerah
                </div>
            </div>
        </div>
    """)

# ----------------------------------------------------
# SLIDE 14: TANTANGAN KONSTITUSI DI ERA KONTEMPORER
# ----------------------------------------------------
elif curr["id"] == 13:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    render_html("""
        <div class="card-grid">
            <div class="content-card">
                <div class="card-icon">⚖️</div>
                <div class="card-title">1. Independensi & Etika Peradilan</div>
                <div class="card-text">
                    Tantangan menjaga murwah Mahkamah Konstitusi dan lembaga peradilan agar bebas dari intervensi konflik kepentingan politik kekuasaan demi kepastian hukum yang berkeadilan.
                </div>
            </div>
            <div class="content-card">
                <div class="card-icon">🌐</div>
                <div class="card-title">2. Kebebasan Digital & Polarisasi</div>
                <div class="card-text">
                    Mengimbangi perlindungan kebebasan berpendapat di ruang digital (Pasal 28E) dengan penindakan disinformasi dan ujaran kebencian tanpa memberangus hak-hak sipil warga negara.
                </div>
            </div>
            <div class="content-card">
                <div class="card-icon">📜</div>
                <div class="card-title">3. Meaningful Public Participation</div>
                <div class="card-text">
                    Tuntutan keterlibatan masyarakat yang bermakna dalam proses legislasi (seperti putusan MK terkait UU Cipta Kerja), bukan sekadar formalitas rapat dengar pendapat.
                </div>
            </div>
            <div class="content-card">
                <div class="card-icon">🔮</div>
                <div class="card-title">4. Wacana Amandemen ke-5</div>
                <div class="card-text">
                    Perdebatan publik mengenai perlunya Pokok-Pokok Haluan Negara (PPHN), penataan ulang kewenangan DPD RI, hingga risiko terbukanya kembali wacana perpanjangan masa jabatan.
                </div>
            </div>
        </div>
        
        <div class="quote-box" style="margin-top: 24px;">
            💬 <b>Refleksi Kritis:</b> Konstitusi yang kokoh bukan hanya diukur dari indahnya redaksional pasal-pasal di atas kertas, melainkan sejauh mana budaya hukum (<i>legal culture</i>) dan integritas moral para penyelenggara negara mampu menjunjung nilai-nilai kejujuran dan keadilan konstitusional.
        </div>
    """)

# ----------------------------------------------------
# SLIDE 15: KESIMPULAN, REFLEKSI PANCASILA & PENUTUP
# ----------------------------------------------------
elif curr["id"] == 14:
    render_html(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """)
    
    col_s15_1, col_s15_2 = st.columns([3, 2])
    with col_s15_1:
        render_html("""
            <div class="content-card" style="border-left: 4px solid #ffd166; margin-bottom: 16px;">
                <div class="card-title" style="color: #ffd166; font-size: 1.25rem;">✨ Sintesis Akhir Kelompok</div>
                <div class="card-text" style="font-size: 0.95rem; line-height: 1.7;">
                    Dinamika pelaksanaan UUD 1945 membuktikan bahwa bangsa Indonesia selalu memiliki daya lentur dan ketahanan konstitusional dalam menghadapi krisis. Dari masa revolusi, federalisme RIS, liberalisme UUDS 1950, otoritarianisme Orde Baru, hingga era Reformasi saat ini, UUD 1945 telah bertransformasi menjadi <b>konstitusi modern yang demokratis</b> dengan tetap memegang teguh Pancasila sebagai panduan moral abadi.
                </div>
            </div>
            
            <div class="card-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
                <div class="content-card">
                    <div style="color: #ffd166; font-weight: 700; font-size: 0.88rem;">SILA 1 & 2</div>
                    <div class="card-text" style="font-size: 0.82rem; margin-top: 4px;">Etika religiusitas & penghormatan martabat HAM setiap anak bangsa.</div>
                </div>
                <div class="content-card">
                    <div style="color: #ffd166; font-weight: 700; font-size: 0.88rem;">SILA 3</div>
                    <div class="card-text" style="font-size: 0.82rem; margin-top: 4px;">Komitmen final menjaga keutuhan Negara Kesatuan Republik Indonesia.</div>
                </div>
                <div class="content-card">
                    <div style="color: #ffd166; font-weight: 700; font-size: 0.88rem;">SILA 4 & 5</div>
                    <div class="card-text" style="font-size: 0.82rem; margin-top: 4px;">Demokrasi permusyawaratan demi mewujudkan keadilan sosial merata.</div>
                </div>
            </div>
        """)
    with col_s15_2:
        render_html("""
            <div class="replica-graphic-box" style="border: 1px solid rgba(255,209,102,0.3); background: rgba(255,209,102,0.04);">
                <div style="font-size: 3rem; margin-bottom: 8px;">🙏 🇮🇩 🎓</div>
                <h3 style="color: #ffd166; font-family: 'Cinzel', serif; margin-bottom: 6px;">TERIMA KASIH!</h3>
                <p style="font-size: 0.88rem; color: #a8dadc; margin-bottom: 14px;">Sesi Tanya Jawab & Diskusi Terbuka</p>
                <div style="font-size: 0.82rem; color: #f1faee; width: 100%; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 12px; line-height: 1.8;">
                    <b>Kelompok Presentasi:</b><br>
                    1. Randi Prasetyo • 2. M. Said Haykal<br>
                    4. Ragil Prakhoso • 5. M. Syauqi Alfa Illiyin<br>
                    6. Harland Ramadhan • 7. Daffa Dwi Amanda<br>
                    <i>Mata Kuliah: Pendidikan Pancasila</i>
                </div>
            </div>
        """)

# REPLIKA VIDEO ANIMASI UNTUK SETIAP SLIDE (15 SLIDE)
render_html(get_replica_video_card(curr["id"]))

render_html('</div>') # End slide-wrapper

# ==========================================
# SPEAKER / PRESENTER NOTES (IF TOGGLED)
# ==========================================
SPEAKER_NOTES = [
    "Selamat pagi/siang dosen pengampu dan rekan-rekan mahasiswa. Pada kesempatan ini kelompok kami mempresentasikan dinamika pelaksanaan UUD 1945, diawali perkenalan anggota kelompok 1 sampai 7.",
    "Pada slide agenda, jelaskan alur presentasi yang kita bagi menjadi 3 babak besar: fase fondasi kemerdekaan, fase turbulensi politik RIS & UUDS, serta era Orde Baru hingga Reformasi.",
    "Tegaskan konsep dasar UUD 1945 sebagai hukum dasar tertinggi dan mengapa Pembukaan UUD 1945 berkedudukan sebagai staatsfundamentalnorm yang tidak boleh diubah.",
    "Jelaskan bahwa UUD 1945 awal disahkan sehari setelah proklamasi. Mengapa strukturnya ringkas dan ada aturan peralihan pasal IV yang memusatkan kekuasaan sementara di tangan Presiden.",
    "Jelaskan kontroversi dan strategi di balik Maklumat Wapres No. X dan Maklumat 14 November 1945 yang mengubah sistem Presidensial menjadi Parlementer tanpa amandemen teks.",
    "Poin penting: RIS adalah hasil kompromi KMB. Paparkan bagaimana bentuk federasi dipaksakan oleh Belanda untuk melemahkan RI melalui negara-negara boneka.",
    "Garis bawahi Mosi Integral Mohammad Natsir 3 April 1950 yang menjadi tonggak kembalinya negara-negara bagian ke pangkuan NKRI pada 17 Agustus 1950.",
    "Uraikan fakta menarik era Demokrasi Liberal: keberhasilan gemilang Pemilu 1955, namun diwarnai instabilitas ekstrem di mana 7 kabinet jatuh-bangun dalam tempo 9 tahun.",
    "Soroti momen krusial 5 Juli 1959: Mengapa Presiden Soekarno mengeluarkan dekrit? Jelaskan kebuntuan Konstituante dan doktrin hukum darurat negara (staatsnoodrecht).",
    "Analisis kritis Orde Lama: Niat menyelamatkan negara justru bergeser menjadi sentralisme dan penyimpangan konstitusi seperti pengangkatan presiden seumur hidup dan pembubaran DPR.",
    "Paparkan kontras Orde Baru: Berjanji melaksanakan UUD 1945 secara murni dan konsekuen, namun berujung pada sakralisasi konstitusi, executive heavy, dan krisis 1998.",
    "Jelaskan 4 gelombang amandemen UUD 1945 (1999-2002) dan sebutkan 5 kesepakatan dasar MPR agar audiens memahami batasan perubahan yang dilakukan.",
    "Uraikan lembaga-lembaga baru pasca amandemen (MK, KY, DPD) dan tegaskan pembatasan masa jabatan presiden maksimal 2 periode untuk mencegah kekuasaan otoriter berulang.",
    "Bahas tantangan masa kini: Independensi MK, polarisasi di era media sosial digital, pentingnya meaningful participation, dan sikap kritis terhadap wacana amandemen ke-5.",
    "Tutup presentasi dengan merangkum bahwa dinamika UUD 1945 adalah proses pematangan bangsa, serta hubungkan dengan pengamalan 5 Sila Pancasila sebelum membuka sesi tanya jawab."
]

if st.session_state.show_notes:
    render_html(f"""
        <div class="speaker-notes">
            <b>🎙️ Panduan Narasi Presenter (Slide {st.session_state.slide + 1}):</b><br>
            <i>"{SPEAKER_NOTES[st.session_state.slide]}"</i>
        </div>
    """)

# ==========================================
# BOTTOM CONTROLS & INTERACTIVE FEATURES
# ==========================================
render_html("<br>")
col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns([1, 1, 2, 1, 1])

with col_b1:
    st.button("⏮️ Cover", on_click=jump_to_slide, args=(0,), key="btn_bot_cover", use_container_width=True)

with col_b2:
    st.button("⬅️ Sebelumnya", disabled=(st.session_state.slide == 0), on_click=prev_slide, key="btn_bot_prev", use_container_width=True)

with col_b3:
    # Dropdown Direct Nav
    st.selectbox(
        "Pilih Menu Cepat:",
        options=range(len(SLIDES)),
        format_func=lambda i: f"Slide {i+1}: {SLIDES[i]['title'][:32]}...",
        index=st.session_state.slide,
        key="bottom_picker",
        on_change=on_bottom_change,
        label_visibility="collapsed"
    )

with col_b4:
    st.button("Berikutnya ➡️", disabled=(st.session_state.slide == len(SLIDES) - 1), on_click=next_slide, key="btn_bot_next", use_container_width=True)

with col_b5:
    st.button("⏭️ Akhir", on_click=jump_to_slide, args=(len(SLIDES) - 1,), key="btn_bot_end", use_container_width=True)

# ==========================================
# INTERACTIVE MINI-QUIZ / KNOWLEDGE CHECK MODAL (EXPANDER)
# ==========================================
st.markdown("---")
with st.expander("🧠 Kuis Interaktif Pemahaman Konstitusi (Uji Pengetahuan Audiens)"):
    st.markdown("Uji pemahaman audiens atau rekan kelas setelah menyimak presentasi Dinamika UUD 1945:")
    q1 = st.radio(
        "1. Maklumat manakah yang mengalihkan sistem Presidensial ke Parlementer pada masa awal kemerdekaan?",
        ["Maklumat Pemerintah 14 November 1945", "Maklumat No. X 16 Oktober 1945", "Maklumat 3 November 1945"],
        index=None,
        key="quiz_q1"
    )
    if q1:
        if q1 == "Maklumat Pemerintah 14 November 1945":
            st.success("✅ Tepat sekali! Maklumat 14 November 1945 menetapkan pertanggungjawaban menteri kepada Parlemen/BP-KNIP.")
        else:
            st.error("❌ Belum tepat. Maklumat yang mengalihkan tanggung jawab kabinet adalah Maklumat Pemerintah 14 November 1945.")

    q2 = st.radio(
        "2. Tokoh nasional yang memprakarsai Mosi Integral 1950 untuk membubarkan RIS dan kembali ke NKRI adalah...",
        ["Mohammad Natsir", "Sutan Sjahrir", "Kasman Singodimedjo"],
        index=None,
        key="quiz_q2"
    )
    if q2:
        if q2 == "Mohammad Natsir":
            st.success("✅ Tepat sekali! Mohammad Natsir memprakarsai Mosi Integral pada 3 April 1950.")
        else:
            st.error("❌ Belum tepat. Tokoh tersebut adalah Mohammad Natsir dari Masyumi.")

    q3 = st.radio(
        "3. Berapa kali UUD 1945 diamandemen pada era Reformasi?",
        ["4 Tahap (1999, 2000, 2001, 2002)", "3 Tahap (1999, 2001, 2003)", "5 Tahap (1998 - 2004)"],
        index=None,
        key="quiz_q3"
    )
    if q3:
        if q3 == "4 Tahap (1999, 2000, 2001, 2002)":
            st.success("✅ Benar! Amandemen UUD 1945 dilaksanakan secara bertahap sebanyak 4 kali oleh MPR.")
        else:
            st.error("❌ Belum tepat. Amandemen UUD 1945 berlangsung 4 tahap (1999-2002).")

# ==========================================
# DOWNLOAD HANDOUT SUMMARY
# ==========================================
summary_md = f"""# RINGKASAN PRESENTASI: DINAMIKA PELAKSANAAN UUD 1945
Mata Kuliah: Pendidikan Pancasila & Kewarganegaraan

## Tim Penyusun:
1. RANDI PRASETYO
2. M. SAID HAYKAL
4. RAGIL PRAKHOSO
5. M. SYAUQI ALFA ILLIYIN
6. HARLAND RAMADHAN
7. DAFFA DWI AMANDA

---

## Kronologi & Periode Konstitusi:
1. **UUD 1945 Awal Kemerdekaan (18 Ags 1945 - 27 Des 1949)**
   - Pengesahan oleh PPKI.
   - Pergeseran Presidensial ke Parlementer via Maklumat 14 Nov 1945.
2. **Konstitusi RIS 1949 (27 Des 1949 - 17 Ags 1950)**
   - Bentuk negara Federal / Serikat hasil KMB di Den Haag.
   - Sistem Quasi-Parlementer.
3. **UUDS 1950 (17 Ags 1950 - 5 Juli 1959)**
   - Kembali ke NKRI berkat Mosi Integral Mohammad Natsir.
   - Demokrasi Liberal dengan 7 kali pergantian kabinet.
   - Sukses Pemilu 1955, namun kebuntuan di Badan Konstituante.
4. **Dekrit Presiden 5 Juli 1959 & Orde Lama (1959 - 1966)**
   - Dekrit pembubaran Konstituante & berlakunya kembali UUD 1945.
   - Demokrasi Terpimpin yang diwarnai penyimpangan konstitusi.
5. **UUD 1945 Masa Orde Baru (1966 - 1998)**
   - Tekad pelaksanaan murni & konsekuen.
   - Mengalami sakralisasi dan dominasi Executive Heavy selama 32 tahun.
6. **Era Reformasi & 4 Tahap Amandemen (1999 - 2002)**
   - Pembatasan jabatan Presiden (Pasal 7).
   - Lembaga baru: Mahkamah Konstitusi, Komisi Yudisial, DPD RI.
   - Bab khusus penegasan Hak Asasi Manusia (Pasal 28A-28J).
"""

st.download_button(
    label="📥 Unduh Rangkuman Materi PPT (Handout .md)",
    data=summary_md,
    file_name="Handout_Dinamika_UUD_1945.md",
    mime="text/markdown"
)
