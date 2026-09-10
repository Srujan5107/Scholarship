import base64
import os
import urllib.parse
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Scholarship Matching & Discovery Portal",
    page_icon="🎓",
    layout="wide"
)

# --- Multilingual Localization Dictionary ---
TRANSLATIONS = {
    "English": {
        "yt_lang_suffix": "in english step by step",
        "title": "🎓 Scholarship Matching & Discovery Portal",
        "caption": "A centralized gateway to discover matching scholarships, verify eligibility, and organize required paperwork.",
        "lang_select": "🌐 Select Language / भाषा चुनें",
        "profile_header": "Student Profile",
        "course_label": "Course of Study",
        "marks_label": "Previous Qualifying Score (%)",
        "income_label": "Annual Household Income (₹)",
        "category_label": "Category",
        "female_label": "Candidate is Female",
        "tab_matched": "🎯 Recommended Schemes",
        "tab_checklist": "📋 Document Checklist",
        "tab_directory": "📚 Complete Directory",
        "schemes_found": "Eligible & Verified Schemes ({count} Found)",
        "no_match_warn": "No schemes match your exact profile. Adjust your income range or qualifying score to discover alternative schemes.",
        "issued_by": "Issued By",
        "trust_status": "Trust Status",
        "financial_assistance": "Financial Assistance",
        "deadline": "Application Deadline",
        "portal_link": "Official Application Portal",
        "video_guide": "How to Apply (YouTube Video)",
        "match_prob": "Match Probability",
        "high_rec": "High Recommendation",
        "eligible": "Eligible to Apply",
        "checklist_header": "Document Readiness Checklist",
        "checklist_sub": "Keep track of required paperwork across all eligible scholarships:",
        "readiness_level": "Readiness Level",
        "docs_prepared": "{ready} of {total} mandatory items prepared.",
        "no_matched_docs": "Match with at least one scholarship above to view required paperwork.",
        "dir_header": "Complete Directory",
        "col_scholarship": "Scholarship",
        "col_org": "Issuing Body",
        "col_income": "Max Income (₹)",
        "col_marks": "Min Marks (%)",
        "col_deadline": "Deadline",
        "col_guide": "Video Tutorial",
        "col_cat": "Eligible Categories"
    },
    "हिंदी (Hindi)": {
        "yt_lang_suffix": "in hindi full process",
        "title": "🎓 छात्रवृत्ति मिलान एवं खोज पोर्टल",
        "caption": "पात्र छात्रवृत्तियों की खोज, पात्रता सत्यापन और आवश्यक दस्तावेजों को व्यवस्थित करने का मंच।",
        "lang_select": "🌐 भाषा चुनें (Select Language)",
        "profile_header": "विद्यार्थी विवरण (Student Profile)",
        "course_label": "अध्ययन पाठ्यक्रम (Course)",
        "marks_label": "पिछला योग्यता अंक (%)",
        "income_label": "वार्षिक पारिवारिक आय (₹)",
        "category_label": "वर्ग (Category)",
        "female_label": "उम्मीदवार महिला है",
        "tab_matched": "🎯 अनुशंसित योजनाएं",
        "tab_checklist": "📋 आवश्यक दस्तावेज सूची",
        "tab_directory": "📚 संपूर्ण निर्देशिका",
        "schemes_found": "पात्र एवं सत्यापित योजनाएं ({count} उपलब्ध)",
        "no_match_warn": "आपकी प्रोफ़ाइल से मेल खाती कोई योजना नहीं मिली। कृपया आय सीमा या अंकों में बदलाव करें।",
        "issued_by": "जारीकर्ता",
        "trust_status": "सत्यापन स्थिति",
        "financial_assistance": "वित्तीय सहायता",
        "deadline": "आवेदन की अंतिम तिथि",
        "portal_link": "आधिकारिक आवेदन पोर्टल",
        "video_guide": "आवेदन कैसे करें (हिंदी वीडियो)",
        "match_prob": "मिलान प्रतिशत",
        "high_rec": "शीर्ष अनुशंसा",
        "eligible": "आवेदन के पात्र",
        "checklist_header": "दस्तावेज़ तैयारी चेकलिस्ट",
        "checklist_sub": "पात्र योजनाओं के लिए आवश्यक दस्तावेजों की स्थिति जांचें:",
        "readiness_level": "तैयारी स्तर",
        "docs_prepared": "{total} में से {ready} अनिवार्य दस्तावेज़ तैयार हैं।",
        "no_matched_docs": "आवश्यक दस्तावेज़ देखने के लिए कम से कम एक छात्रवृत्ति से मिलान होना आवश्यक है।",
        "dir_header": "संपूर्ण छात्रवृत्ति सूची",
        "col_scholarship": "छात्रवृत्ति",
        "col_org": "संस्था",
        "col_income": "अधिकतम आय (₹)",
        "col_marks": "न्यूनतम अंक (%)",
        "col_deadline": "अंतिम तिथि",
        "col_guide": "वीडियो ट्यूटोरियल",
        "col_cat": "पात्र श्रेणियां"
    },
    "ಕನ್ನಡ (Kannada)": {
        "yt_lang_suffix": "in kannada application process",
        "title": "🎓 ವಿದ್ಯಾರ್ಥಿವೇತನ ಹೊಂದಾಣಿಕೆ ಮತ್ತು ಶೋಧನಾ ಪೋರ್ಟಲ್",
        "caption": "ನಿಮಗೆ ಸೂಕ್ತವಾದ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಲು ಮತ್ತು ದಾಖಲೆಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಲು ಕೇಂದ್ರೀಕೃತ ವೇದಿಕೆ.",
        "lang_select": "🌐 ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ (Select Language)",
        "profile_header": "ವಿದ್ಯಾರ್ಥಿ ವಿವರ (Profile)",
        "course_label": "ಅಧ್ಯಯನ ಕೋರ್ಸ್ (Course)",
        "marks_label": "ಹಿಂದಿನ ಅಂಕಗಳು (%)",
        "income_label": "ವಾರ್ಷಿಕ ಕುಟುಂಬ ಆದಾಯ (₹)",
        "category_label": "ಪ್ರವರ್ಗ (Category)",
        "female_label": "ಅಭ್ಯರ್ಥಿ ಮಹಿಳೆಯಾಗಿದ್ದಾರೆ",
        "tab_matched": "🎯 ಶಿಫಾರಸು ಮಾಡಲಾದ ಯೋಜನೆಗಳು",
        "tab_checklist": "📋 ಅಗತ್ಯ ದಾಖಲೆಗಳ ಪಟ್ಟಿ",
        "tab_directory": "📚 ಸಂಪೂರ್ಣ ಕೋಶ",
        "schemes_found": "ಅರ್ಹ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು ({count} ಲಭ್ಯವಿದೆ)",
        "no_match_warn": "ಯಾವುದೇ ಯೋಜನೆಗಳು ಹೊಂದಿಕೆಯಾಗಿಲ್ಲ. ದಯವಿಟ್ಟು ಆದಾಯ ಅಥವಾ ಅಂಕಗಳ ಮಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "issued_by": "ನೀಡುವ ಸಂಸ್ಥೆ",
        "trust_status": "ಪರಿಶೀಲನೆ ಸ್ಥಿತಿ",
        "financial_assistance": "ಆರ್ಥಿಕ ನೆರವು",
        "deadline": "ಅರ್ಜಿ ಸಲ್ಲಿಸಲು ಕೊನೆಯ ದಿನಾಂಕ",
        "portal_link": "ಅಧಿಕೃತ ಅರ್ಜಿ ಪೋರ್ಟಲ್",
        "video_guide": "ಅರ್ಜಿ ಸಲ್ಲಿಸುವುದು ಹೇಗೆ (ಕನ್ನಡ ವಿಡಿಯೋ)",
        "match_prob": "ಹೊಂದಾಣಿಕೆ ದರ",
        "high_rec": "ಉನ್ನತ ಶಿಫಾರಸು",
        "eligible": "ಅರ್ಜಿ ಸಲ್ಲಿಸಲು ಅರ್ಹರು",
        "checklist_header": "ದಾಖಲೆಗಳ ಸಿದ್ಧತೆಯ ಪರಿಶೀಲನಾ ಪಟ್ಟಿ",
        "checklist_sub": "ನಿಮ್ಮ ಅರ್ಹ ಯೋಜನೆಗಳಿಗೆ ಅಗತ್ಯವಿರುವ ದಾಖಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ:",
        "readiness_level": "ಸಿದ್ಧತೆ ಮಟ್ಟ",
        "docs_prepared": "{total} ರಲ್ಲಿ {ready} ಕಡ್ಡಾಯ ದಾಖಲೆಗಳು ಸಿದ್ಧವಾಗಿವೆ.",
        "no_matched_docs": "ದಾಖಲೆಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಕನಿಷ್ಠ ಒಂದು ವಿದ್ಯಾರ್ಥಿವೇತನ ಹೊಂದಾಣಿಕೆಯಾಗಬೇಕು.",
        "dir_header": "ಸಂಪೂರ್ಣ ವಿದ್ಯಾರ್ಥಿವೇತನ ಡೈರೆಕ್ಟರಿ",
        "col_scholarship": "ವಿದ್ಯಾರ್ಥಿವೇತನ",
        "col_org": "ಸಂಸ್ಥೆ",
        "col_income": "ಗರಿಷ್ಠ ಆದಾಯ (₹)",
        "col_marks": "ಕನಿಷ್ಠ ಅಂಕಗಳು (%)",
        "col_deadline": "ಕೊನೆಯ ದಿನಾಂಕ",
        "col_guide": "ವಿಡಿಯೋ ಮಾರ್ಗದರ್ಶಿ",
        "col_cat": "ಅರ್ಹ ವರ್ಗಗಳು"
    },
    "తెలుగు (Telugu)": {
        "yt_lang_suffix": "in telugu application apply process",
        "title": "🎓 స్కాలర్‌షిప్ మ్యాచింగ్ & పోర్టల్",
        "caption": "మీకు తగిన స్కాలర్‌షిప్‌లను కనుగొనడానికి మరియు పత్రాలను సిద్ధం చేసుకోవడానికి ఒక వేదిక.",
        "lang_select": "🌐 భాషను ఎంచుకోండి (Select Language)",
        "profile_header": "విద్యార్థి ప్రొఫైల్ (Profile)",
        "course_label": "చదువుతున్న కోర్సు (Course)",
        "marks_label": "గత అర్హత మార్కులు (%)",
        "income_label": "వార్షిక కుటుంబ ఆదాయం (₹)",
        "category_label": "వర్గం (Category)",
        "female_label": "అభ్యర్థి మహిళ",
        "tab_matched": "🎯 సిఫార్సు చేసిన పథకాలు",
        "tab_checklist": "📋 పత్రాల చెక్‌లిస్ట్",
        "tab_directory": "📚 పూర్తి డైరెక్టరీ",
        "schemes_found": "అర్హత కలిగిన పథకాలు ({count} లభించాయి)",
        "no_match_warn": "మీ ప్రొఫైల్‌కు సరిపోలే పథకాలు లేవు. దయచేసి ఆదాయం లేదా మార్కుల వివరాలను సవరించండి.",
        "issued_by": "అందించే సంస్థ",
        "trust_status": "ధృవీకరణ స్థితి",
        "financial_assistance": "ఆర్థిక సహాయం",
        "deadline": "దరఖాస్తుకు చివరి తేదీ",
        "portal_link": "అధికారిక దరఖాస్తు పోర్టల్",
        "video_guide": "దరఖాస్తు విధానం (తెలుగు వీడియో)",
        "match_prob": "సరిపోలిక శాతం",
        "high_rec": "ముఖ్య సిఫార్సు",
        "eligible": "దరఖాస్తు చేసుకోవచ్చు",
        "checklist_header": "పత్రాల సన్నద్ధత చెక్‌లిస్ట్",
        "checklist_sub": "అవసరమైన పత్రాలను ఇక్కడ తనిఖీ చేయండి:",
        "readiness_level": "సన్నద్ధత శాతం",
        "docs_prepared": "{total} లో {ready} తప్పనిసరి పత్రాలు సిద్ధంగా ఉన్నాయి.",
        "no_matched_docs": "పత్రాల వివరాల కోసం కనీసం ఒక స్కాలర్‌షిప్‌కు అర్హత పొందండి.",
        "dir_header": "పూర్తి స్కాలర్‌షిప్ వివరాలు",
        "col_scholarship": "స్కాలర్‌షిప్",
        "col_org": "సంస్థ",
        "col_income": "గరిష్ట ఆదాయం (₹)",
        "col_marks": "కనీస మార్కులు (%)",
        "col_deadline": "చివరి తేదీ",
        "col_guide": "వీడియో గైడ్",
        "col_cat": "అర్హతగల వర్గాలు"
    },
    "தமிழ் (Tamil)": {
        "yt_lang_suffix": "in tamil application process",
        "title": "🎓 கல்வி உதவித்தொகை கண்டறிதல் போர்டல்",
        "caption": "தகுதியான கல்வி உதவித்தொகைகளைக் கண்டறிந்து ஆவணங்களை தயார் செய்வதற்கான தளம்.",
        "lang_select": "🌐 மொழியைத் தேர்ந்தெடுக்கவும் (Select Language)",
        "profile_header": "மாணவர் விவரக்குறிப்பு (Profile)",
        "course_label": "படிப்பு (Course)",
        "marks_label": "முந்தைய தகுதி மதிப்பெண் (%)",
        "income_label": "ஆண்டு குடும்ப வருமானம் (₹)",
        "category_label": "பிரிவு (Category)",
        "female_label": "விண்ணப்பதாரர் பெண்",
        "tab_matched": "🎯 பரிந்துரைக்கப்பட்ட திட்டங்கள்",
        "tab_checklist": "📋 ஆவண சரிபார்ப்பு பட்டியல்",
        "tab_directory": "📚 முழு விவரக்குறிப்பு",
        "schemes_found": "தகுதியான உதவித்தொகைகள் ({count} கண்டறியப்பட்டன)",
        "no_match_warn": "பொருத்தமான திட்டங்கள் எதுவும் இல்லை. வருமானம் அல்லது மதிப்பெண் அளவை மாற்றியமைக்கவும்.",
        "issued_by": "வழங்கும் அமைப்பு",
        "trust_status": "சரிபார்ப்பு நிலை",
        "financial_assistance": "நிதி உதவி",
        "deadline": "விண்ணப்பிக்க கடைசி தேதி",
        "portal_link": "அதிகாரப்பூர்வ விண்ணப்ப தளம்",
        "video_guide": "விண்ணப்பிப்பது எப்படி (தமிழ் வீடியோ)",
        "match_prob": "பொருத்த விகிதம்",
        "high_rec": "சிறந்த பரிந்துரை",
        "eligible": "விண்ணப்பிக்க தகுதியுடையவர்",
        "checklist_header": "ஆவண தயார்நிலை சரிபார்ப்பு பட்டியல்",
        "checklist_sub": "தேவையான ஆவணங்களின் நிலையை சரிபார்க்கவும்:",
        "readiness_level": "தயார்நிலை அளவு",
        "docs_prepared": "{total} இல் {ready} கட்டாய ஆவணங்கள் தயாராக உள்ளன.",
        "no_matched_docs": "தேவையான ஆவணங்களைக் காண ஏதேனும் ஒரு உதவித்தொகையுடன் பொருந்த வேண்டும்.",
        "dir_header": "முழு கல்வி உதவித்தொகை அடைவு",
        "col_scholarship": "கல்வி உதவித்தொகை",
        "col_org": "அமைப்பு",
        "col_income": "அதிகபட்ச வருமானம் (₹)",
        "col_marks": "குறைந்தபட்ச மதிப்பெண் (%)",
        "col_deadline": "கடைசி தேதி",
        "col_guide": "வீடியோ கையேடு",
        "col_cat": "தகுதியான பிரிவுகள்"
    }
}

# --- Helper Function: Load Local Image as Base64 ---
def get_base64_image(image_path_or_url: str) -> str:
    if os.path.exists(image_path_or_url):
        with open(image_path_or_url, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            extension = image_path_or_url.split(".")[-1]
            return f"data:image/{extension};base64,{encoded}"
    return image_path_or_url

LOCAL_IMAGE_PATH = "background.jpg" 
FALLBACK_DIRECT_URL = "https://cdn.pixabay.com/photo/2016/06/01/06/26/open-book-1428428_1280.jpg"
bg_source = get_base64_image(LOCAL_IMAGE_PATH) if os.path.exists(LOCAL_IMAGE_PATH) else FALLBACK_DIRECT_URL

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(
            rgba(10, 15, 26, 0.56), 
            rgba(15, 23, 42, 0.68)
        ),
        url('{bg_source}');
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #e5e7eb;
    }}
    [data-testid="stSidebar"] {{
        background: rgba(9, 14, 25, 0.42) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(71, 85, 105, 0.55);
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(17, 24, 39, 0.92) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(251, 191, 36, 0.48) !important;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(251, 191, 36, 0.12);
        padding: 12px 16px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(251, 191, 36, 0.2);
    }}
    h1, h2, h3 {{
        color: #f8fafc;
        font-weight: 700;
    }}
    p, label, [data-testid="stCaptionContainer"] {{
        color: #cbd5e1;
    }}
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input {{
        background: #111827 !important;
        color: #f8fafc !important;
        border-color: #475569 !important;
    }}
    [data-baseweb="popover"] > div,
    [role="listbox"] {{
        background: #1e293b !important;
        color: #f8fafc !important;
    }}
    [data-testid="stTabs"] button {{
        color: #94a3b8;
    }}
    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: #fbbf24;
        border-bottom-color: #fbbf24;
    }}
    [data-testid="stDataFrame"] {{
        border: 1px solid #334155;
        border-radius: 10px;
        overflow: hidden;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Database ---
SCHOLARSHIP_DB = [
    {
        "name": "Reliance Foundation Undergraduate Scholarship",
        "org": "Reliance Foundation (CSR)",
        "search_term": "Reliance Foundation Undergraduate Scholarship apply online",
        "min_marks": 60,
        "max_income": 1500000,
        "categories": ["General", "OBC", "SC", "ST"],
        "courses": ["Engineering", "B.Sc", "Medical", "Arts/Commerce", "Diploma"],
        "gender": "All",
        "award": "Up to ₹2,00,000 over course duration",
        "portal_url": "https://scholarships.reliancefoundation.org",
        "trust_badge": "Verified Corporate CSR",
        "deadline": "2026-10-15",
        "docs": ["12th Marks Card", "Family Income Proof", "College Bonafide Certificate", "Valid Photo ID"]
    },
    {
        "name": "Central Sector Scheme for College Students (CSSS)",
        "org": "Ministry of Education (Govt of India)",
        "search_term": "Central Sector Scheme CSSS NSP scholarship apply",
        "min_marks": 80,
        "max_income": 450000,
        "categories": ["General", "OBC", "SC", "ST"],
        "courses": ["Engineering", "B.Sc", "Medical", "Arts/Commerce"],
        "gender": "All",
        "award": "₹12,000/yr (UG 1-3) & ₹20,000/yr (Professional 4th-5th yr)",
        "portal_url": "https://scholarships.gov.in",
        "trust_badge": "Government of India (NSP)",
        "deadline": "2026-10-31",
        "docs": ["12th Board Marksheet", "Income Certificate", "Bank Passbook with Direct Benefit Seeding", "Bonafide Certificate"]
    },
    {
        "name": "AICTE Pragati Scholarship for Girls",
        "org": "AICTE (Govt of India)",
        "search_term": "AICTE Pragati Scholarship for Girls apply online",
        "min_marks": 60,
        "max_income": 800000,
        "categories": ["General", "OBC", "SC", "ST"],
        "courses": ["Engineering", "Diploma"],
        "gender": "Female",
        "award": "₹50,000 per annum for tuition & contingency",
        "portal_url": "https://scholarships.gov.in",
        "trust_badge": "Statutory Body (AICTE)",
        "deadline": "2026-11-15",
        "docs": ["AICTE Institute Admission Letter", "Family Income Certificate", "Valid Photo ID", "Previous Marksheet"]
    },
    {
        "name": "Foundation for Excellence (FFE) Engineering Scholarship",
        "org": "Foundation for Excellence",
        "search_term": "Foundation for Excellence FFE scholarship apply",
        "min_marks": 70,
        "max_income": 300000,
        "categories": ["General", "OBC", "SC", "ST"],
        "courses": ["Engineering", "Medical"],
        "gender": "All",
        "award": "Full Tuition + Laptop Support + Career Mentorship",
        "portal_url": "https://ffe.org",
        "trust_badge": "Verified NGO Trust",
        "deadline": "2026-12-15",
        "docs": ["Entrance Exam Rank Card", "Admission Letter", "Income Certificate", "Electricity Bill"]
    },
    {
        "name": "ONGC Merit Scholarship",
        "org": "ONGC Foundation (PSU)",
        "search_term": "ONGC Merit Scholarship online application process",
        "min_marks": 60,
        "max_income": 200000,
        "categories": ["SC", "ST", "OBC", "General"],
        "courses": ["Engineering", "Medical"],
        "gender": "All",
        "award": "₹48,000 per annum",
        "portal_url": "https://www.ongcscholar.org",
        "trust_badge": "PSU Foundation",
        "deadline": "2026-11-30",
        "docs": ["Class 12 Marksheet", "Caste Certificate", "Annual Family Income Certificate", "Bank Account Details"]
    },
    {
        "name": "Tata Capital Pankh Scholarship",
        "org": "Tata Capital Foundation",
        "search_term": "Tata Capital Pankh scholarship apply process",
        "min_marks": 60,
        "max_income": 250000,
        "categories": ["General", "OBC", "SC", "ST"],
        "courses": ["Engineering", "B.Sc", "Diploma", "Arts/Commerce"],
        "gender": "All",
        "award": "Up to 80% of Tuition Fees (Max ₹50,000)",
        "portal_url": "https://www.buddy4study.com",
        "trust_badge": "Tata Group CSR",
        "deadline": "2026-10-30",
        "docs": ["Fee Receipt", "Income Certificate", "Previous Year Grade Sheet", "Identity Proof"]
    }
]

# --- Dynamic Language-Specific YouTube URL Generator ---
def get_youtube_guide_url(scheme: dict, lang_key: str) -> str:
    lang_suffix = TRANSLATIONS.get(lang_key, TRANSLATIONS["English"])["yt_lang_suffix"]
    query = f"how to apply {scheme['search_term']} {lang_suffix}"
    encoded_query = urllib.parse.quote_plus(query)
    return f"https://www.youtube.com/results?search_query={encoded_query}"

# --- Match Scoring Engine ---
def compute_match_score(student, scheme):
    if scheme["gender"] == "Female" and not student["is_female"]:
        return 0
    if student["course"] not in scheme["courses"]:
        return 0
    if student["marks"] < scheme["min_marks"]:
        return 0
    if student["income"] > scheme["max_income"]:
        return 0
    if student["category"] not in scheme["categories"]:
        return 0

    marks_margin = student["marks"] - scheme["min_marks"]
    academic_score = min(40, 20 + (marks_margin * 1.0))
    income_ratio = student["income"] / scheme["max_income"]
    need_score = 40 * (1.0 - income_ratio)
    base_score = 20

    return max(1, min(99, int(academic_score + need_score + base_score)))

# --- Sidebar Controls: Language Switcher & Profile ---
st.sidebar.markdown("### 🌐 भाषा / ಭಾಷೆ / Language")
selected_lang = st.sidebar.selectbox(
    "Language",
    options=list(TRANSLATIONS.keys()),
    index=0,
    label_visibility="collapsed"
)
t = TRANSLATIONS[selected_lang]

# --- Page Header ---
st.title(t["title"])
st.caption(t["caption"])

st.sidebar.header(t["profile_header"])
student_profile = {
    "course": st.sidebar.selectbox(t["course_label"], ["Engineering", "Diploma", "B.Sc", "Medical", "Arts/Commerce"]),
    "marks": st.sidebar.slider(t["marks_label"], 40, 100, 75),
    "income": st.sidebar.number_input(t["income_label"], 20000, 2000000, 250000, step=25000),
    "category": st.sidebar.selectbox(t["category_label"], ["General", "OBC", "SC", "ST"]),
    "is_female": st.sidebar.checkbox(t["female_label"])
}

# Match Computation
matched_schemes = []
for scheme in SCHOLARSHIP_DB:
    score = compute_match_score(student_profile, scheme)
    if score > 0:
        matched_schemes.append({**scheme, "match_score": score})

matched_schemes.sort(key=lambda x: x["match_score"], reverse=True)

# --- Navigation Tabs ---
tab_matched, tab_checklist, tab_all = st.tabs([
    t["tab_matched"], 
    t["tab_checklist"], 
    t["tab_directory"]
])

# 1. Matched Schemes Tab
with tab_matched:
    header_text = t["schemes_found"].format(count=len(matched_schemes))
    st.subheader(header_text)
    
    if not matched_schemes:
        st.warning(t["no_match_warn"])
    else:
        for item in matched_schemes:
            # Generate the URL in the selected Indian language
            localized_video_url = get_youtube_guide_url(item, selected_lang)
            
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {item['name']}")
                    st.caption(f"🏛️ **{t['issued_by']}:** {item['org']} | **{t['trust_status']}:** `{item['trust_badge']}`")
                    st.write(f"**{t['financial_assistance']}:** {item['award']}")
                    st.write(f"**{t['deadline']}:** `{item['deadline']}`")
                    
                    link_col1, link_col2 = st.columns([1, 1])
                    with link_col1:
                        st.markdown(f"[🔗 {t['portal_link']}]({item['portal_url']})")
                    with link_col2:
                        st.markdown(f"[▶️ {t['video_guide']}]({localized_video_url})")
                
                with col2:
                    st.metric(label=t["match_prob"], value=f"{item['match_score']}%")
                    if item["match_score"] >= 75:
                        st.success(t["high_rec"])
                    else:
                        st.info(t["eligible"])

# 2. Document Readiness Tracker Tab
with tab_checklist:
    st.subheader(t["checklist_header"])
    st.write(t["checklist_sub"])
    
    if matched_schemes:
        needed_docs = sorted(list({doc for s in matched_schemes for doc in s["docs"]}))
        
        col_list, col_summary = st.columns([2, 1])
        with col_list:
            checklist_state = {doc: st.checkbox(doc, key=f"chk_doc_{doc}") for doc in needed_docs}
        
        ready_docs = sum(checklist_state.values())
        total_docs = max(1, len(needed_docs))
        progress_val = ready_docs / total_docs
        
        with col_summary:
            st.metric(t["readiness_level"], f"{int(progress_val * 100)}%")
            st.progress(progress_val)
            summary_msg = t["docs_prepared"].format(ready=ready_docs, total=len(needed_docs))
            st.write(f"**{summary_msg}**")
    else:
        st.info(t["no_matched_docs"])

# 3. Complete Directory Tab
with tab_all:
    st.subheader(t["dir_header"])
    
    df = pd.DataFrame([
        {
            t["col_scholarship"]: s["name"],
            t["col_org"]: s["org"],
            t["col_income"]: f"₹{s['max_income']:,}",
            t["col_marks"]: f"{s['min_marks']}%",
            t["col_deadline"]: s["deadline"],
            t["col_guide"]: get_youtube_guide_url(s, selected_lang),
            t["col_cat"]: ", ".join(s["categories"])
        }
        for s in SCHOLARSHIP_DB
    ])
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            t["col_guide"]: st.column_config.LinkColumn(
                t["col_guide"],
                display_text="Watch ▶️"
            )
        }
    )