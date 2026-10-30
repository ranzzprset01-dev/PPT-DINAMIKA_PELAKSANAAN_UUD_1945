import streamlit as st
import json

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
st.markdown("""
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
""", unsafe_allow_html=True)

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

# ==========================================
# SIDEBAR NAVIGATION & TEAM PROFILE
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 12px 0;">
            <div style="font-size: 2.2rem; margin-bottom: 6px;">🏛️ 🇮🇩</div>
            <h3 style="color: #ffd166; margin: 0; font-family: 'Cinzel', serif; font-size: 1.15rem;">DINAMIKA UUD 1945</h3>
            <p style="color: #a8dadc; font-size: 0.8rem; margin-top: 4px;">Pendidikan Pancasila Berbasis Web</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Slide Selection
    slide_titles = [f"{i+1}. {s['title'][:28]}..." for i, s in enumerate(SLIDES)]
    selected_slide = st.selectbox(
        "📑 Pilih Halaman Menu:",
        options=range(len(SLIDES)),
        format_func=lambda x: slide_titles[x],
        index=st.session_state.slide,
        key="sidebar_select"
    )
    if selected_slide != st.session_state.slide:
        st.session_state.slide = selected_slide
        st.rerun()

    # Progress bar
    progress = (st.session_state.slide + 1) / len(SLIDES)
    st.progress(progress)
    st.caption(f"📍 Halaman {st.session_state.slide + 1} dari 15 Menu Slide")

    st.markdown("---")
    
    # Team Roster in Sidebar
    st.markdown("""
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
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Speaker Notes Toggle
    st.session_state.show_notes = st.toggle("🎙️ Tampilkan Catatan Presenter", value=st.session_state.show_notes)
    
    # Quick Timeline Jump
    st.markdown("<p style='font-size: 0.8rem; font-weight: 700; color: #a8dadc; margin-top: 10px;'>⚡ Pintasan Periode:</p>", unsafe_allow_html=True)
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        if st.button("🇮🇩 1945-1949", use_container_width=True):
            st.session_state.slide = 3
            st.rerun()
        if st.button("⚖️ UUDS 1950", use_container_width=True):
            st.session_state.slide = 7
            st.rerun()
        if st.button("🦅 Orde Baru", use_container_width=True):
            st.session_state.slide = 10
            st.rerun()
    with col_sb2:
        if st.button("🌐 RIS 1949", use_container_width=True):
            st.session_state.slide = 5
            st.rerun()
        if st.button("📜 Orde Lama", use_container_width=True):
            st.session_state.slide = 9
            st.rerun()
        if st.button("✨ Reformasi", use_container_width=True):
            st.session_state.slide = 11
            st.rerun()

# ==========================================
# MAIN SLIDE DISPLAY LOGIC
# ==========================================

curr = SLIDES[st.session_state.slide]

# TOP PROGRESS INDICATOR BAR
col_nav_l, col_nav_m, col_nav_r = st.columns([1, 4, 1])
with col_nav_l:
    if st.button("◀️ Mundur", disabled=(st.session_state.slide == 0), use_container_width=True):
        st.session_state.slide -= 1
        st.rerun()
with col_nav_m:
    st.markdown(f"""
        <div style="text-align: center; padding: 4px;">
            <span style="background: rgba(230, 57, 70, 0.2); border: 1px solid rgba(230, 57, 70, 0.4); color: #ffd166; font-size: 0.85rem; font-weight: 700; padding: 4px 18px; border-radius: 999px;">
                SLIDE {st.session_state.slide + 1} / 15: {curr['title']}
            </span>
        </div>
    """, unsafe_allow_html=True)
with col_nav_r:
    if st.button("Maju ▶️", disabled=(st.session_state.slide == len(SLIDES) - 1), use_container_width=True):
        st.session_state.slide += 1
        st.rerun()

# SLIDE CONTENT CONTAINER
st.markdown('<div class="slide-wrapper">', unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 1: COVER / HALAMAN UTAMA
# ----------------------------------------------------
if curr["id"] == 0:
    st.markdown(f"""
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
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 2: DAFTAR ISI / AGENDA 15 SLIDE
# ----------------------------------------------------
elif curr["id"] == 1:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_ag1, col_ag2, col_ag3 = st.columns(3)
    with col_ag1:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_ag2:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_ag3:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="quote-box">
            💡 <b>Catatan Analitis:</b> Dinamika UUD 1945 bukanlah sekadar pergantian teks hukum formal, melainkan dialektika mencari keseimbangan antara stabilitas pemerintahan, kedaulatan rakyat, dan kemurnian cita-cita kemerdekaan bangsa Indonesia.
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 3: HAKIKAT & KEDUDUKAN UUD 1945
# ----------------------------------------------------
elif curr["id"] == 2:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s3_l, col_s3_r = st.columns([3, 2])
    with col_s3_l:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_s3_r:
        st.markdown(f"""
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
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 4: PERIODE I (18 AGUSTUS 1945 - 27 DES 1949)
# ----------------------------------------------------
elif curr["id"] == 3:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s4_1, col_s4_2 = st.columns([3, 2])
    with col_s4_1:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_s4_2:
        st.markdown(f"""
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
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 5: DINAMIKA & PENYIMPANGAN PERIODE I
# ----------------------------------------------------
elif curr["id"] == 4:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s5_1, col_s5_2, col_s5_3 = st.columns(3)
    with col_s5_1:
        st.markdown("""
            <div class="content-card" style="border-top: 3px solid #e63946;">
                <div class="card-icon">📄</div>
                <div class="card-title">Maklumat Wakil Presiden No. X</div>
                <div class="card-text">
                    <b>Tanggal: 16 Oktober 1945</b><br>
                    Mengubah kedudukan KNIP dari sekadar pembantu presiden menjadi badan yang diserahi <b>kekuasaan legislatif</b> dan ikut menetapkan GBHN bersama Presiden sebelum terbentuknya DPR/MPR.
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_s5_2:
        st.markdown("""
            <div class="content-card" style="border-top: 3px solid #ffd166;">
                <div class="card-icon">👥</div>
                <div class="card-title">Maklumat Pemerintah 3 Nov 1945</div>
                <div class="card-text">
                    <b>Anjuran Pembentukan Partai Politik</b><br>
                    Dikeluarkan guna mempertegas citra Indonesia sebagai negara demokratis di mata dunia internasional, memicu lahirnya sistem multi-partai yang sangat dinamis.
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_s5_3:
        st.markdown("""
            <div class="content-card" style="border-top: 3px solid #06d6a0;">
                <div class="card-icon">🔄</div>
                <div class="card-title">Maklumat 14 November 1945</div>
                <div class="card-text">
                    <b>Peralihan ke Sistem Parlementer</b><br>
                    Pertanggungjawaban menteri dialihkan dari Presiden kepada Parlemen/Badan Pekerja KNIP. Sutan Sjahrir diangkat menjadi Perdana Menteri pertama RI.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        <div class="quote-box">
            ⚠️ <b>Telaah Konstitusional:</b> Terjadi pergeseran konstitusional (constitutional convention) dari sistem <b>Presidensial</b> ke sistem <b>Parlementer</b> tanpa melalui amandemen teks resmi UUD 1945. Hal ini merupakan strategi diplomatik meyakinkan Sekutu bahwa Indonesia bukan negara fasis bentukan Jepang.
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 6: PERIODE II - KONSTITUSI RIS 1949
# ----------------------------------------------------
elif curr["id"] == 5:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s6_l, col_s6_r = st.columns([3, 2])
    with col_s6_l:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_s6_r:
        st.markdown("""
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
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 7: DINAMIKA & PENOLAKAN NEGARA RIS
# ----------------------------------------------------
elif curr["id"] == 6:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
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
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 8: PERIODE III - UUDS 1950 & DEMOKRASI LIBERAL
# ----------------------------------------------------
elif curr["id"] == 7:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s8_1, col_s8_2 = st.columns([3, 2])
    with col_s8_1:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_s8_2:
        st.markdown("""
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
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 9: KEBUNTUAN KONSTITUANTE & DEKRIT PRESIDEN 1959
# ----------------------------------------------------
elif curr["id"] == 8:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s9_l, col_s9_r = st.columns([3, 2])
    with col_s9_l:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_s9_r:
        st.markdown(f"""
            <div class="replica-graphic-box">
                {get_svg_dekrit()}
                <h4 style="color: #ffd166; margin-top: 10px;">DEKRIT PRESIDEN 5 JULI 1959</h4>
                <p style="font-size: 0.85rem; color: #e2e8f0; line-height: 1.5;">
                    <i>"Kami Presiden Republik Indonesia/Panglima Tertinggi Angkatan Perang... dengan ini menyatakan berlakunya kembali Undang-Undang Dasar 1945..."</i>
                </p>
            </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 10: PERIODE IV - ORDE LAMA / DEMOKRASI TERPIMPIN
# ----------------------------------------------------
elif curr["id"] == 9:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
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
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 11: PERIODE V - UUD 1945 MASA ORDE BARU
# ----------------------------------------------------
elif curr["id"] == 10:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s11_1, col_s11_2 = st.columns([3, 2])
    with col_s11_1:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_s11_2:
        st.markdown("""
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
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 12: PERIODE VI - ERA REFORMASI & 4 AMANDEMEN
# ----------------------------------------------------
elif curr["id"] == 11:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s12_l, col_s12_r = st.columns([3, 2])
    with col_s12_l:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_s12_r:
        st.markdown(f"""
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
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 13: RESTRUKTURISASI KELEMBAGAAN PASCA AMANDEMEN
# ----------------------------------------------------
elif curr["id"] == 12:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s13_1, col_s13_2, col_s13_3 = st.columns(3)
    with col_s13_1:
        st.markdown("""
            <div class="content-card" style="border-top: 3px solid #e63946;">
                <div class="card-icon">⚖️</div>
                <div class="card-title">Mahkamah Konstitusi (MK)</div>
                <div class="card-text">
                    Hadir sebagai <i>The Guardian of Constitution</i> dan pelindung hak asasi warga negara. Berwenang menguji UU terhadap UUD, memutus sengketa kewenangan lembaga negara, memutus pembubaran parpol, dan sengketa hasil Pemilu.
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_s13_2:
        st.markdown("""
            <div class="content-card" style="border-top: 3px solid #ffd166;">
                <div class="card-icon">🌐</div>
                <div class="card-title">Bikameral & DPD RI</div>
                <div class="card-text">
                    Parlemen bertransformasi menjadi bikameral lunak (<i>soft bicameralism</i>), di mana MPR terdiri atas anggota DPR (representasi politik rakyat) dan anggota DPD (representasi daerah kepulauan dan provinsi).
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_s13_3:
        st.markdown("""
            <div class="content-card" style="border-top: 3px solid #06d6a0;">
                <div class="card-icon">🛡️</div>
                <div class="card-title">Penguatan Piagam HAM</div>
                <div class="card-text">
                    Konstitusi kini memuat 10 pasal rincian HAM (Pasal 28A hingga 28J) yang menjamin hak hidup, berkeluarga, kepastian hukum yang adil, kebebasan berekspresi, hingga perlindungan dari diskriminasi.
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
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
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 14: TANTANGAN KONSTITUSI DI ERA KONTEMPORER
# ----------------------------------------------------
elif curr["id"] == 13:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
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
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# SLIDE 15: KESIMPULAN, REFLEKSI PANCASILA & PENUTUP
# ----------------------------------------------------
elif curr["id"] == 14:
    st.markdown(f"""
        <div class="slide-badge">{curr['badge']}</div>
        <div class="slide-title">{curr['title']}</div>
        <div class="slide-subtitle">{curr['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    col_s15_1, col_s15_2 = st.columns([3, 2])
    with col_s15_1:
        st.markdown("""
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
        """, unsafe_allow_html=True)
    with col_s15_2:
        st.markdown("""
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
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # End slide-wrapper

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
    st.markdown(f"""
        <div class="speaker-notes">
            <b>🎙️ Panduan Narasi Presenter (Slide {st.session_state.slide + 1}):</b><br>
            <i>"{SPEAKER_NOTES[st.session_state.slide]}"</i>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# BOTTOM CONTROLS & INTERACTIVE FEATURES
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns([1, 1, 2, 1, 1])

with col_b1:
    if st.button("⏮️ Halaman Cover", use_container_width=True):
        st.session_state.slide = 0
        st.rerun()

with col_b2:
    if st.button("⬅️ Sebelumnya", disabled=(st.session_state.slide == 0), use_container_width=True):
        st.session_state.slide -= 1
        st.rerun()

with col_b3:
    # Dropdown Direct Nav
    new_idx = st.selectbox(
        "Pilih Menu Cepat:",
        options=range(len(SLIDES)),
        format_func=lambda i: f"Slide {i+1}: {SLIDES[i]['title'][:32]}...",
        index=st.session_state.slide,
        label_visibility="collapsed"
    )
    if new_idx != st.session_state.slide:
        st.session_state.slide = new_idx
        st.rerun()

with col_b4:
    if st.button("Berikutnya ➡️", disabled=(st.session_state.slide == len(SLIDES) - 1), use_container_width=True):
        st.session_state.slide += 1
        st.rerun()

with col_b5:
    if st.button("⏭️ Halaman Akhir", use_container_width=True):
        st.session_state.slide = len(SLIDES) - 1
        st.rerun()

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
