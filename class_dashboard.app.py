import streamlit as st
import datetime
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="우리 반 스마트 대시보드",
    page_icon="🏫",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization for data persistence within session
if 'assessments' not in st.session_state:
    st.session_state.assessments = [
        {"subject": "국어", "title": "토론 수행평가", "date": datetime.date(2026, 6, 15), "status": "진행중"},
        {"subject": "수학", "title": "단원평가 (함수)", "date": datetime.date(2026, 6, 20), "status": "예정"},
        {"subject": "영어", "title": "말하기 발표", "date": datetime.date(2026, 6, 25), "status": "예정"},
    ]

if 'events' not in st.session_state:
    st.session_state.events = [
        {"title": "체육대회", "date": datetime.date(2026, 6, 18), "desc": "운동장에서 반티 착용 후 집결"},
        {"title": "현장체험학습", "date": datetime.date(2026, 6, 28), "desc": "서울랜드 방문"},
    ]

if 'supplies' not in st.session_state:
    st.session_state.supplies = [
        {"item": "실내화", "date": datetime.date.today(), "done": False},
        {"item": "미술 도구 (수채화 물감)", "date": datetime.date.today(), "done": False},
        {"item": "역사 부교재", "date": datetime.date.today(), "done": True},
    ]

if 'gallery' not in st.session_state:
    st.session_state.gallery = [
        {"caption": "봄 소풍 단체 사진", "tag": "일상"},
        {"caption": "체육대회 연습 중", "tag": "체육대회"},
    ]

# Sidebar Navigation
st.sidebar.markdown("# 🏫 우리 반 메뉴")
menu = st.sidebar.radio(
    "이동할 메뉴를 선택하세요:",
    ["🏠 홈 (대시보드)", "📋 수행평가 일정", "🎒 준비물 체크리스트", "📅 학급 행사 일정", "🖼️ 우리 반 갤러리"]
)

# ----------------- HOME / DASHBOARD -----------------
if menu == "🏠 홈 (대시보드)":
    st.markdown('<div class="main-header">🏫 2학년 3반 스마트 대시보드</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">우리 반의 모든 일정과 추억을 한눈에 확인하세요!</div>', unsafe_allow_html=True)

    # Top D-day banner
    today = datetime.date.today()
    upcoming_events = sorted([e for e in st.session_state.events if e['date'] >= today], key=lambda x: x['date'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="오늘의 날짜", value=today.strftime("%Y년 %m월 %d일"))
    with col2:
        if upcoming_events:
            next_event = upcoming_events[0]
            d_day = (next_event['date'] - today).days
            st.metric(label=f"다음 행사: {next_event['title']}", value=f"D-{d_day}", delta=str(next_event['date']))
        else:
            st.metric(label="예정된 행사", value="없음")
    with col3:
        pending_supplies = sum(1 for s in st.session_state.supplies if not s['done'])
        st.metric(label="챙겨야 할 준비물", value=f"{pending_supplies}개")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📌 다가오는 수행평가 요약")
        sorted_assessments = sorted([a for a in st.session_state.assessments if a['date'] >= today], key=lambda x: x['date'])
        if sorted_assessments:
            for asm in sorted_assessments[:3]:
                st.info(f"**[{asm['subject']}] {asm['title']}** — 📅 {asm['date']}")
        else:
            st.write("등록된 다가오는 수행평가가 없습니다.")

    with col_right:
        st.subheader("⭐ 학급 대표 사진")
        # Placeholder or uploaded gallery preview
        st.image("https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80", caption="우리 반 단체 사진 (샘플)")

# ----------------- ASSESSMENTS -----------------
elif menu == "📋 수행평가 일정":
    st.markdown('<div class="main-header">📋 수행평가 및 과제 일정</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">과목별 수행평가 일정을 확인하고 준비하세요.</div>', unsafe_allow_html=True)

    # Add new assessment expander
    with st.expander("➕ 새로운 수행평가 추가하기"):
        with st.form("add_assessment_form"):
            new_subject = st.text_input("과목명 (예: 국어, 수학)")
            new_title = st.text_input("수행평가 제목/내용")
            new_date = st.date_input("제출/평가일")
            submit_asm = st.form_submit_button("추가")
            if submit_asm and new_subject and new_title:
                st.session_state.assessments.append({
                    "subject": new_subject,
                    "title": new_title,
                    "date": new_date,
                    "status": "예정"
                })
                st.success("수행평가 일정이 추가되었습니다!")
                st.rerun()

    st.divider()

    # Display list
    subject_filter = st.selectbox("과목 필터링", ["전체"] + list(set(a['subject'] for a in st.session_state.assessments)))
    
    for asm in st.session_state.assessments:
        if subject_filter == "전체" or asm['subject'] == subject_filter:
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                st.badge = st.markdown(f"**{asm['subject']}**")
            with col2:
                st.write(f"{asm['title']}")
            with col3:
                st.write(f"📅 {asm['date']}")
            st.divider()

# ----------------- SUPPLIES -----------------
elif menu == "🎒 준비물 체크리스트":
    st.markdown('<div class="main-header">🎒 준비물 체크리스트</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">오늘과 내일 잊지 말고 챙겨야 할 준비물입니다.</div>', unsafe_allow_html=True)

    with st.form("add_supply_form"):
        new_item = st.text_input("준비물 내용 입력")
        item_date = st.date_input("필요한 날짜", datetime.date.today())
        submit_sup = st.form_submit_button("준비물 추가")
        if submit_sup and new_item:
            st.session_state.supplies.append({"item": new_item, "date": item_date, "done": False})
            st.success("준비물이 추가되었습니다!")
            st.rerun()

    st.divider()

    for idx, sup in enumerate(st.session_state.supplies):
        col1, col2 = st.columns([4, 1])
        with col1:
            done = st.checkbox(f"{sup['item']} (날짜: {sup['date']})", value=sup['done'], key=f"sup_{idx}")
            if done != sup['done']:
                st.session_state.supplies[idx]['done'] = done
        with col2:
            if st.button("삭제", key=f"del_sup_{idx}"):
                st.session_state.supplies.pop(idx)
                st.rerun()

# ----------------- EVENTS -----------------
elif menu == "📅 학급 행사 일정":
    st.markdown('<div class="main-header">📅 학급 및 학교 행사 일정</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">이번 달 주요 행사 일정을 확인하세요.</div>', unsafe_allow_html=True)

    with st.expander("➕ 행사 추가하기"):
        with st.form("add_event_form"):
            evt_title = st.text_input("행사 명칭")
            evt_date = st.date_input("행사 날짜")
            evt_desc = st.text_area("행사 설명 및 안내사항")
            submit_evt = st.form_submit_button("행사 등록")
            if submit_evt and evt_title:
                st.session_state.events.append({"title": evt_title, "date": evt_date, "desc": evt_desc})
                st.success("행사가 등록되었습니다!")
                st.rerun()

    st.divider()

    sorted_events = sorted(st.session_state.events, key=lambda x: x['date'])
    for evt in sorted_events:
        with st.container():
            st.markdown(f"### 🗓️ {evt['title']}")
            st.write(f"**날짜:** {evt['date']}")
            st.write(f"**안내:** {evt['desc']}")
            st.divider()

# ----------------- GALLERY -----------------
elif menu == "🖼️ 우리 반 갤러리":
    st.markdown('<div class="main-header">🖼️ 우리 반 갤러리</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">우리들의 소중한 추억을 공유하는 공간입니다.</div>', unsafe_allow_html=True)

    with st.expander("📤 사진 업로드하기"):
        with st.form("upload_photo_form"):
            caption = st.text_input("사진 설명 (캡션)")
            tag = st.selectbox("카테고리", ["일상", "체육대회", "현장체험학습", "축제/기타"])
            uploaded_file = st.file_uploader("이미지 파일 선택", type=["jpg", "jpeg", "png"])
            submit_photo = st.form_submit_button("업로드")
            if submit_photo and uploaded_file and caption:
                st.session_state.gallery.append({"caption": caption, "tag": tag})
                st.success("사진이 성공적으로 업로드되었습니다!")
                st.rerun()

    st.divider()

    # Grid layout for gallery
    cols = st.columns(2)
    sample_images = [
        "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=600&q=80",
    ]
    
    for idx, item in enumerate(st.session_state.gallery):
        img_url = sample_images[idx % len(sample_images)]
        with cols[idx % 2]:
            st.image(img_url, caption=f"[{item['tag']}] {item['caption']}", use_column_width=True)
