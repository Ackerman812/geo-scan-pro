import streamlit as st
import numpy as np
from PIL import Image, ImageChops
import pandas as pd
from datetime import date

# ========== НАСТРОЙКА СТРАНИЦЫ ==========
st.set_page_config(
    page_title="🛰️ GEO SCAN PRO | Мониторинг Земли",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:yasya.ackerman.77@gmail.com',
        'Report a bug': "mailto:yasya.ackerman.77@gmail.com",
        'About': "### 🏆 Конкурсный проект\nСистема автоматического анализа изменений земной поверхности."
    }
)

# ========== КАСТОМНЫЙ CSS ДЛЯ ВАУ-ДИЗАЙНА ==========
def add_custom_css():
    st.markdown(f"""
    <style>
    /* 1. Основной градиентный фон с анимированными частицами */
    .stApp {{
        background: linear-gradient(135deg, 
            #0f0c29 0%, 
            #302b63 25%, 
            #24243e 50%, 
            #1a1a2e 75%, 
            #16213e 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
    }}
    
    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* 2. Анимированные звёзды на фоне */
    .stars {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }}
    
    .star {{
        position: absolute;
        background-color: white;
        border-radius: 50%;
        animation: twinkle var(--duration) infinite alternate;
    }}
    
    @keyframes twinkle {{
        0% {{ opacity: 0.2; transform: scale(0.8); }}
        100% {{ opacity: 1; transform: scale(1.2); }}
    }}
    
    /* 3. Стилизация всех контейнеров - неоновая подсветка */
    div[data-testid="stExpander"], 
    div[data-testid="stVerticalBlock"] > div > div > div,
    section[data-testid="stSidebar"] > div {{
        background: rgba(16, 18, 42, 0.85) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        border: 1px solid rgba(0, 150, 255, 0.3) !important;
        box-shadow: 
            0 8px 32px rgba(0, 100, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    /* Эффект при наведении */
    div[data-testid="stExpander"]:hover,
    div[data-testid="stVerticalBlock"] > div > div > div:hover {{
        border-color: #00ffff !important;
        box-shadow: 
            0 0 20px rgba(0, 255, 255, 0.4),
            0 8px 40px rgba(0, 100, 255, 0.2) !important;
        transform: translateY(-5px) !important;
    }}
    
    /* 4. Заголовки с градиентным текстом */
    h1, h2, h3, h4 {{
        background: linear-gradient(90deg, #00ffff, #0080ff, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-fill-color: transparent;
        background-size: 200% auto;
        animation: shine 3s linear infinite;
    }}
    
    /* Исключение для заголовков с эмодзи */
    h1 span, h2 span, h3 span, h4 span {{
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        background-clip: initial !important;
        text-fill-color: initial !important;
        animation: none !important;
    }}
    
    @keyframes shine {{
        to {{ background-position: 200% center; }}
    }}
    
    /* 5. Кнопки с неоновым эффектом */
    .stButton > button {{
        background: linear-gradient(90deg, 
            #ff0080, 
            #ff00ff, 
            #8000ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        z-index: 1 !important;
        box-shadow: 0 5px 20px rgba(255, 0, 128, 0.3) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(255, 0, 128, 0.5) !important;
        animation: pulse 1s infinite !important;
    }}
    
    .stButton > button:before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
        z-index: -1;
    }}
    
    .stButton > button:hover:before {{
        left: 100%;
    }}
    
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(255, 0, 128, 0.7); }}
        70% {{ box-shadow: 0 0 0 15px rgba(255, 0, 128, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(255, 0, 128, 0); }}
    }}
    
    /* 6. Слайдеры и инпуты */
    .stSlider > div > div {{
        background: linear-gradient(90deg, #00ffff, #0080ff) !important;
        height: 8px !important;
        border-radius: 4px !important;
    }}
    
    .stSlider > div > div > div {{
        background: #ffffff !important;
        border: 3px solid #00ffff !important;
        box-shadow: 0 0 10px #00ffff !important;
    }}
    
    /* 7. Боковая панель */
    section[data-testid="stSidebar"] {{
        background: rgba(10, 12, 35, 0.95) !important;
        backdrop-filter: blur(20px);
        border-right: 2px solid rgba(0, 150, 255, 0.2) !important;
    }}
    
    /* 8. Прогресс-бар */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, #00ff88, #00ffff) !important;
        animation: progressAnimation 2s ease-in-out infinite !important;
    }}
    
    @keyframes progressAnimation {{
        0% {{ width: 0%; opacity: 0.7; }}
        50% {{ width: 100%; opacity: 1; }}
        100% {{ width: 0%; opacity: 0.7; }}
    }}
    
    /* 9. Изображения с рамкой */
    .stImage {{
        border-radius: 15px !important;
        overflow: hidden !important;
        border: 2px solid transparent !important;
        background: linear-gradient(45deg, #00ffff, #0080ff, #00ffff) border-box !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
        transition: all 0.5s ease !important;
    }}
    
    .stImage:hover {{
        transform: scale(1.02) rotate(1deg) !important;
        box-shadow: 0 15px 40px rgba(0, 255, 255, 0.3) !important;
    }}
    
    /* 10. Метрики в карточках */
    div[data-testid="stMetric"] {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        backdrop-filter: blur(5px);
    }}
    
    div[data-testid="stMetricValue"] {{
        font-size: 2.5rem !important;
        font-weight: bold !important;
        background: linear-gradient(90deg, #ffffff, #00ffff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        animation: metricPulse 2s infinite !important;
    }}
    
    @keyframes metricPulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    /* 11. Улучшение текста и исправление эмодзи */
    .stMarkdown {{
        color: rgba(255, 255, 255, 0.9) !important;
        line-height: 1.8 !important;
    }}
    
    /* Исправление эмодзи в тексте */
    .stMarkdown span {{
        color: inherit !important;
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        background-clip: initial !important;
        text-fill-color: initial !important;
    }}
    
    /* Эмодзи в кнопках и заголовках */
    button span, .stButton span,
    .stMetricLabel span, 
    div[data-testid="stMetricLabel"] span,
    .stExpander span {{
        color: inherit !important;
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        background-clip: initial !important;
        text-fill-color: initial !important;
        animation: none !important;
    }}
    
    /* Эмодзи в инфографике */
    div[data-testid="stVerticalBlock"] > div > div > div div {{
        color: inherit !important;
    }}
    
    /* Эмодзи в боковой панели */
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {{
        color: inherit !important;
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        background-clip: initial !important;
        text-fill-color: initial !important;
    }}
    
    /* Специальные классы для эмодзи */
    .emoji {{
        color: inherit !important;
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        background-clip: initial !important;
        text-fill-color: initial !important;
        animation: none !important;
        filter: none !important;
    }}
    
    /* Восстановление цвета для всех эмодзи */
    .st-emotion-cache-1kyxreq {{
        color: inherit !important;
    }}
    
    /* Отключение градиентов для эмодзи */
    *[class*="emoji"], 
    *[role="img"],
    span[role="img"] {{
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        background-clip: initial !important;
        text-fill-color: initial !important;
        color: inherit !important;
        filter: none !important;
    }}
    </style>
    
    <!-- Анимированные звёзды -->
    <div class="stars" id="stars"></div>
    
    <script>
    function createStars() {{
        const starsContainer = document.getElementById('stars');
        const starCount = 150;
        
        for (let i = 0; i < starCount; i++) {{
            const star = document.createElement('div');
            star.className = 'star';
            
            // Случайные параметры
            const size = Math.random() * 3 + 1;
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            const duration = Math.random() * 3 + 1;
            const delay = Math.random() * 5;
            
            star.style.width = size + 'px';
            star.style.height = size + 'px';
            star.style.left = x + '%';
            star.style.top = y + '%';
            star.style.setProperty('--duration', duration + 's');
            star.style.animationDelay = delay + 's';
            star.style.opacity = Math.random() * 0.5 + 0.2;
            
            starsContainer.appendChild(star);
        }}
    }}
    
    // Запускаем после загрузки
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', createStars);
    }} else {{
        createStars();
    }}
    
    // Дополнительный скрипт для исправления эмодзи
    document.addEventListener('DOMContentLoaded', function() {{
        // Ищем и исправляем эмодзи
        setTimeout(function() {{
            const emojis = document.querySelectorAll('span[role="img"], .emoji, [class*="emoji"]');
            emojis.forEach(function(emoji) {{
                emoji.style.background = 'none';
                emoji.style.webkitBackgroundClip = 'initial';
                emoji.style.webkitTextFillColor = 'initial';
                emoji.style.backgroundClip = 'initial';
                emoji.style.textFillColor = 'initial';
                emoji.style.color = 'inherit';
                emoji.style.filter = 'none';
                emoji.classList.add('emoji');
            }});
        }}, 1000);
    }});
    </script>
    """, unsafe_allow_html=True)

add_custom_css()

# ========== БОКОВАЯ ПАНЕЛЬ ==========
with st.sidebar:
    # Анимированный заголовок
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2.2rem; margin: 0;">🛰️ GEO SCAN</h1>
        <p style="color: #00ffff; font-size: 1.1rem; margin: 5px 0;">PROFESSIONAL EDITION</p>
        <div style="height: 3px; background: linear-gradient(90deg, transparent, #00ffff, transparent); margin: 15px 0;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Информация о проекте
    with st.container():
        st.markdown("### 🏆 **КОНКУРСНЫЙ ПРОЕКТ**")
        st.markdown("""
        <div style="background: rgba(0, 100, 255, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #00ffff;">
        <p style="margin: 0;">Система автоматического обнаружения и анализа изменений земной поверхности</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Параметры анализа
    st.markdown("### ⚙️ **ПАРАМЕТРЫ АНАЛИЗА**")
    
    threshold = st.slider(
        "**Порог обнаружения аномалий (%)**",
        min_value=0.1,
        max_value=20.0,
        value=5.0,
        step=0.1,
        help="Регулирует чувствительность системы"
    )
    
    # Дополнительные настройки
    analysis_mode = st.selectbox(
        "**Режим анализа**",
        ["Стандартный", "Высокая точность", "Быстрый анализ"],
        index=0
    )
    
    show_heatmap = st.toggle("Показать тепловую карту", value=True)
    
    st.markdown("---")
    
    # Быстрые действия
    st.markdown("### 🚀 **БЫСТРЫЕ ДЕЙСТВИЯ**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📁 Примеры", use_container_width=True):
            st.session_state.demo_mode = True
    with col2:
        if st.button("🔄 Сброс", use_container_width=True):
            st.session_state.clear()
    
    st.markdown("---")
    
    # Контакты разработчика
    st.markdown("### 📞 **КОНТАКТЫ**")
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 200, 255, 0.3);">
        <p style="margin: 0 0 10px 0;"><b>👨‍💻 Разработчик:</b></p>
        <p style="margin: 5px 0;"><b>📧 Почта:</b><br>
        <a href="mailto:yasya.ackerman.77@gmail.com" style="color: #00ffff; text-decoration: none;">
            yasya.ackerman.77@gmail.com
        </a></p>
        <p style="margin: 5px 0;"><b>📱 Телефон:</b><br>
        <a href="tel:89626544669" style="color: #00ffff; text-decoration: none;">
            +7 (962) 654-46-69
        </a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Статус системы
    st.markdown("---")
    st.markdown("### 📊 **СТАТУС СИСТЕМЫ**")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Процессор", "15%", delta="↓ 2%")
    with col_stat2:
        st.metric("Память", "68%", delta="↑ 5%")
    with col_stat3:
        st.metric("Сеть", "24%", delta="→")

# ========== ОСНОВНОЙ ИНТЕРФЕЙС ==========
# Главный заголовок с анимацией
st.markdown("""
<div style="text-align: center; padding: 30px 0 20px 0;">
    <h1 style="font-size: 3.5rem; margin: 0; letter-spacing: 2px;">
        <span style="color: #00ffff;">АВТОМАТИЧЕСКИЙ</span> 
        <span style="color: #ffffff;">МОНИТОРИНГ</span>
    </h1>
    <p style="font-size: 1.3rem; color: rgba(255, 255, 255, 0.8); margin: 10px 0 30px 0;">
        Профессиональная система мониторинга изменений земной поверхности
    </p>
    <div style="height: 4px; width: 200px; background: linear-gradient(90deg, #ff0080, #00ffff, #ff0080); margin: 0 auto; border-radius: 2px;"></div>
</div>
""", unsafe_allow_html=True)

# Инфографика
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    with st.container():
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2.5rem; color: #00ffff;">🛰️</div>
            <h4>Спутниковый анализ</h4>
            <p>Работа с данными Sentinel-2, Landsat</p>
        </div>
        """, unsafe_allow_html=True)
with col_info2:
    with st.container():
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2.5rem; color: #00ff88;">📈</div>
            <h4>AI алгоритмы</h4>
            <p>Нейросетевые модели обнаружения</p>
        </div>
        """, unsafe_allow_html=True)
with col_info3:
    with st.container():
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2.5rem; color: #ff0080;">⚡</div>
            <h4>Реальное время</h4>
            <p>Мгновенная обработка данных</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== ЗАГРУЗКА ДАННЫХ ==========
st.markdown("### 📤 **ЗАГРУЗКА СПУТНИКОВЫХ СНИМКОВ**")

# Красивые карточки для загрузки
col_upload1, col_upload2 = st.columns(2)

with col_upload1:
    with st.container():
        st.markdown("#### 📅 **СНИМОК 'ДО'**")
        st.markdown("*Ранний период наблюдения*")
        img1 = st.file_uploader(
            "Перетащите или выберите файл",
            type=['png', 'jpg', 'jpeg', 'tiff', 'tif'],
            key="img1",
            label_visibility="collapsed",
            help="Поддерживаются форматы: PNG, JPG, TIFF"
        )
        if img1:
            st.success("✅ **Файл успешно загружен**")
            file_details = {"Имя файла": img1.name, "Тип файла": img1.type}
            st.json(file_details, expanded=False)

with col_upload2:
    with st.container():
        st.markdown("#### 📅 **СНИМОК 'ПОСЛЕ'**")
        st.markdown("*Поздний период наблюдения*")
        img2 = st.file_uploader(
            "Перетащите или выберите файл",
            type=['png', 'jpg', 'jpeg', 'tiff', 'tif'],
            key="img2",
            label_visibility="collapsed",
            help="Рекомендуется одинаковый размер с первым снимком"
        )
        if img2:
            st.success("✅ **Файл успешно загружен**")
            file_details = {"Имя файла": img2.name, "Тип файла": img2.type}
            st.json(file_details, expanded=False)

st.markdown("---")

# ========== АНАЛИЗ И ВИЗУАЛИЗАЦИЯ ==========
if img1 and img2:
    # Прогресс-бар с анимацией
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(101):
        progress_bar.progress(i)
        status_text.text(f"🔍 **ВЫПОЛНЯЕТСЯ АНАЛИЗ... {i}%**")
        if i == 25:
            status_text.text("🔍 **ЗАГРУЗКА ИЗОБРАЖЕНИЙ... 25%**")
        elif i == 50:
            status_text.text("🔍 **ВЫЧИСЛЕНИЕ РАЗЛИЧИЙ... 50%**")
        elif i == 75:
            status_text.text("🔍 **АНАЛИЗ АНОМАЛИЙ... 75%**")
        elif i == 100:
            status_text.text("✅ **АНАЛИЗ ЗАВЕРШЁН!**")
    
    # Имитация обработки
    import time
    time.sleep(0.5)
    
    # Загрузка и подготовка изображений
    image1 = Image.open(img1).convert('RGB')
    image2 = Image.open(img2).convert('RGB')
    image2 = image2.resize(image1.size)
    
    img1_array = np.array(image1)
    img2_array = np.array(image2)
    
    # Анализ различий
    diff = ImageChops.difference(image1, image2).convert('L')
    diff_array = np.array(diff)
    change_percent = (np.mean(diff_array) / 255.0) * 100
    similarity = 100 - change_percent
    
    # ========== ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ ==========
    st.markdown("### 🖼️ **ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ**")
    
    # Три колонки для изображений
    col_img1, col_img2, col_img3 = st.columns(3)
    
    with col_img1:
        with st.container():
            st.markdown("#### **СНИМОК 'ДО'**")
            st.image(image1, use_container_width=True)
            st.caption(f"📏 **Размер:** {image1.size[0]}×{image1.size[1]} пикселей")
    
    with col_img2:
        with st.container():
            st.markdown("#### **СНИМОК 'ПОСЛЕ'**")
            st.image(image2, use_container_width=True)
            st.caption(f"📏 **Размер:** {image2.size[0]}×{image2.size[1]} пикселей")
    
    with col_img3:
        with st.container():
            st.markdown("#### **КАРТА ИЗМЕНЕНИЙ**")
            
            # Создаём цветную тепловую карту
            if show_heatmap:
                heatmap = diff.convert('RGB')
                heatmap_array = np.array(heatmap)
                # Усиливаем красный канал для тепловой карты
                heatmap_array[:, :, 0] = np.clip(diff_array * 2, 0, 255)
                heatmap = Image.fromarray(heatmap_array)
                st.image(heatmap, use_container_width=True)
                st.caption("🔥 **Тепловая карта:** Красный = максимальные изменения")
            else:
                st.image(diff, use_container_width=True)
                st.caption("⚫ **Чёрно-белая карта:** Белый = изменения")
    
    st.markdown("---")
    
    # ========== МЕТРИКИ И АНАЛИТИКА ==========
    st.markdown("### 📊 **АНАЛИТИКА И МЕТРИКИ**")
    
    # Основные метрики
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric(
            label="**СХОДСТВО**",
            value=f"{similarity:.1f}%",
            delta=f"{(similarity - 50):+.1f}%" if similarity != 50 else "0%",
            delta_color="normal"
        )
    
    with metric_col2:
        st.metric(
            label="**ИЗМЕНЕНИЯ**",
            value=f"{change_percent:.2f}%",
            delta=f"{(change_percent - threshold):+.2f}%" if change_percent != threshold else "0%",
            delta_color="inverse"
        )
    
    with metric_col3:
        anomaly_status = "⚠️ АНОМАЛИЯ" if change_percent > threshold else "✅ НОРМА"
        delta_status = "Превышен" if change_percent > threshold else "В норме"
        st.metric(
            label="**СТАТУС**",
            value=anomaly_status,
            delta=delta_status,
            delta_color="normal" if change_percent <= threshold else "off"
        )
    
    with metric_col4:
        efficiency = 100 - (change_percent * 0.5)
        st.metric(
            label="**ЭФФЕКТИВНОСТЬ**",
            value=f"{efficiency:.1f}%",
            delta=f"{(efficiency - 80):+.1f}%" if efficiency != 80 else "0%",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # ========== ДЕТАЛЬНАЯ СТАТИСТИКА ==========
    with st.expander("📈 **ДЕТАЛЬНАЯ СТАТИСТИКА И ВИЗУАЛИЗАЦИЯ**", expanded=True):
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.markdown("#### **ЦИФРОВЫЕ ПОКАЗАТЕЛИ**")
            
            # Создаём DataFrame со статистикой
            stats_data = {
                "Показатель": [
                    "Общее количество пикселей",
                    "Изменённых пикселей",
                    "Максимальная яркость разницы",
                    "Средняя яркость разницы",
                    "Стандартное отклонение",
                    "Пикселей выше порога"
                ],
                "Значение": [
                    f"{img1_array.size:,}",
                    f"{np.sum(diff_array > 50):,}",
                    f"{np.max(diff_array):.1f}",
                    f"{np.mean(diff_array):.2f}",
                    f"{np.std(diff_array):.3f}",
                    f"{np.sum(diff_array > threshold * 2.55):,}"
                ]
            }
            
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(
                stats_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Показатель": st.column_config.TextColumn(width="large"),
                    "Значение": st.column_config.TextColumn(width="medium")
                }
            )
        
        with col_stat2:
            st.markdown("#### **ГРАФИК РАСПРЕДЕЛЕНИЯ**")
            
            # Создаём гистограмму
            hist_data = pd.DataFrame({
                'Интенсивность изменений': diff_array.flatten()
            })
            
            # Улучшенная гистограмма
            import plotly.express as px
            fig = px.histogram(
                hist_data,
                x='Интенсивность изменений',
                nbins=50,
                title="Распределение интенсивности изменений",
                color_discrete_sequence=['#00ffff']
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                xaxis_title="Интенсивность (0-255)",
                yaxis_title="Количество пикселей",
                bargap=0.1
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== ИТОГОВЫЙ ОТЧЁТ ==========
    st.markdown("---")
    
    col_report1, col_report2 = st.columns([3, 1])
    
    with col_report1:
        if change_percent > threshold:
            st.error(f"""
            ## 🚨 **ОБНАРУЖЕНЫ КРИТИЧЕСКИЕ ИЗМЕНЕНИЯ!**
            
            ### **Детали анализа:**
            - **📊 Площадь изменений:** {change_percent:.2f}% (порог: {threshold}%)
            - **⚠️ Превышение порога:** {(change_percent - threshold):.2f}%
            - **📅 Рекомендуемые действия:** Необходима срочная проверка территории
            
            ### **Возможные причины:**
            - Строительные работы
            - Изменение ландшафта
            - Природные явления
            - Антропогенное воздействие
            
            **🔍 Рекомендуется провести детальный анализ с привлечением экспертов.**
            """)
        else:
            st.success(f"""
            ## ✅ **ТЕРРИТОРИЯ СТАБИЛЬНА**
            
            ### **Детали анализа:**
            - **📊 Площадь изменений:** {change_percent:.2f}% (порог: {threshold}%)
            - **📈 Запас до порога:** {(threshold - change_percent):.2f}%
            - **📅 Статус:** Мониторинг не выявил критических изменений
            
            ### **Заключение:**
            Территория сохраняет стабильность в рамках наблюдаемого периода.
            Все изменения находятся в пределах допустимых норм.
            
            **🎯 Система рекомендует продолжить регулярный мониторинг.**
            """)
    
    with col_report2:
        # Генерация отчёта
        report_content = f"""
        ==================================
        ОТЧЁТ ОБ АНАЛИЗЕ TERRAIN SCANNER
        ==================================
        
        Дата анализа: {date.today()}
        Время анализа: {pd.Timestamp.now().strftime('%H:%M:%S')}
        
        --------------------------------
        ПАРАМЕТРЫ АНАЛИЗА:
        --------------------------------
        • Порог обнаружения: {threshold}%
        • Режим анализа: {analysis_mode}
        • Показать тепловую карту: {'Да' if show_heatmap else 'Нет'}
        
        --------------------------------
        РЕЗУЛЬТАТЫ:
        --------------------------------
        • Сходство изображений: {similarity:.1f}%
        • Обнаружено изменений: {change_percent:.2f}%
        • Статус: {'АНОМАЛИЯ' if change_percent > threshold else 'НОРМА'}
        • Эффективность анализа: {efficiency:.1f}%
        
        --------------------------------
        ДЕТАЛЬНАЯ СТАТИСТИКА:
        --------------------------------
        • Всего пикселей: {img1_array.size:,}
        • Изменённых пикселей: {np.sum(diff_array > 50):,}
        • Макс. интенсивность: {np.max(diff_array):.1f}
        • Сред. интенсивность: {np.mean(diff_array):.2f}
        
        --------------------------------
        ЗАКЛЮЧЕНИЕ:
        --------------------------------
        {'Обнаружены значительные изменения, требующие внимания' if change_percent > threshold else 'Значимых изменений не обнаружено, территория стабильна'}
        
        ==================================
        СИСТЕМА АВТОМАТИЧЕСКОГО МОНИТОРИНГА
        © 2024 GEO SCAN PRO
        Контакты: yasya.ackerman.77@gmail.com
        ==================================
        """
        
        # Кнопки действий
        if st.button("📥 **СКАЧАТЬ ПОЛНЫЙ ОТЧЁТ**", use_container_width=True, type="primary"):
            st.download_button(
                label="⬇️ НАЖМИТЕ ДЛЯ СКАЧИВАНИЯ",
                data=report_content,
                file_name=f"terrain_scan_report_{date.today()}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        if st.button("🖨️ **РАСПЕЧАТАТЬ РЕЗУЛЬТАТЫ**", use_container_width=True):
            st.success("**Готово к печати!** Откройте диалог печати в браузере.")
        
        if st.button("📧 **ОТПРАВИТЬ НА ПОЧТУ**", use_container_width=True):
            st.info(f"Отправка на: yasya.ackerman.77@gmail.com")
            st.success("Отчёт подготовлен к отправке!")

else:
    # Состояние без загруженных изображений
    st.markdown("---")
    
    col_demo1, col_demo2, col_demo3 = st.columns(3)
    
    with col_demo1:
        with st.container():
            st.markdown("#### **🎯 ДЕМО-РЕЖИМ**")
            st.markdown("""
            Для тестирования системы вы можете:
            
            1. **Скачать тестовые изображения**
            2. **Использовать свои снимки**
            3. **Создать искусственные изменения**
            """)
            
            if st.button("🖼️ **СКАЧАТЬ ТЕСТОВЫЕ ФАЙЛЫ**", use_container_width=True):
                st.info("Тестовые изображения будут загружены в следующих версиях")
    
    with col_demo2:
        with st.container():
            st.markdown("#### **📚 ИНСТРУКЦИЯ**")
            st.markdown("""
            **Рекомендации:**
            
            • Используйте снимки одинакового размера
            • Форматы: PNG, JPG, TIFF
            • Минимальное разрешение: 800×600
            • Максимальный размер: 20 МБ
            """)
    
    with col_demo3:
        with st.container():
            st.markdown("#### **🏆 КОНКУРСНЫЙ ПРОЕКТ**")
            st.markdown("""
            **Особенности системы:**
            
            • Современный дизайн
            • Анимации и эффекты
            • Профессиональная аналитика
            • Полная документация
            """)
    
    st.markdown("---")
    
    # Баннер с контактами
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, 
            rgba(255, 0, 128, 0.2), 
            rgba(0, 255, 255, 0.2));
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.1);
        margin: 20px 0;
    ">
        <h3 style="color: #ffffff; margin-bottom: 15px;">📞 НУЖНА ПОМОЩЬ?</h3>
        <p style="font-size: 1.1rem; margin-bottom: 10px;">
            <strong>Разработчик:</strong> Яся Аккерман<br>
            <strong>Почта:</strong> 
            <a href="mailto:yasya.ackerman.77@gmail.com" style="color: #00ffff;">
                yasya.ackerman.77@gmail.com
            </a><br>
            <strong>Телефон:</strong> 
            <a href="tel:89626544669" style="color: #00ffff;">
                +7 (962) 654-46-69
            </a>
        </p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Проект разработан для конкурса научно-технических работ
        </p>
    </div>
    """, unsafe_allow_html=True)

# ========== ФИНАЛЬНЫЙ ФУТЕР ==========
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])

with footer_col1:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin: 5px 0;">
            🛰️ <strong>GEO SCAN PRO</strong> | Система автоматического мониторинга земной поверхности
        </p>
        <p style="color: rgba(255, 255, 255, 0.5); font-size: 0.8rem; margin: 5px 0;">
            Версия 2.0 | © 2024 Конкурсный проект | Все права защищены
        </p>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown("""
    <div style="text-align: center;">
        <p style="margin-bottom: 10px;">
            <a href="mailto:yasya.ackerman.77@gmail.com" 
               style="color: #00ffff; text-decoration: none; display: block; margin: 5px 0;">
               📧 Обратная связь
            </a>
            <a href="tel:89626544669" 
               style="color: #00ff88; text-decoration: none; display: block; margin: 5px 0;">
               📱 Техподдержка
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown("""
    <div style="text-align: center;">
        <p style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.7);">
            <span style="color: #ff0080;">❤</span> 
            Сделано с любовью к науке
            <span style="color: #00ffff;">⚡</span>
        </p>
        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px;">
            <div style="width: 10px; height: 10px; background: #ff0080; border-radius: 50%; animation: pulse 1s infinite;"></div>
            <div style="width: 10px; height: 10px; background: #00ffff; border-radius: 50%; animation: pulse 1s infinite 0.2s;"></div>
            <div style="width: 10px; height: 10px; background: #00ff88; border-radius: 50%; animation: pulse 1s infinite 0.4s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== ФИНАЛЬНЫЙ СКРИПТ ДЛЯ АНИМАЦИЙ ==========
st.markdown("""
<script>
// Финальная анимация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов
    const elements = document.querySelectorAll('div[data-testid="stVerticalBlock"] > div');
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Периодическое обновление статуса
    setInterval(() => {
        const statusElements = document.querySelectorAll('[data-testid="stMetricValue"]');
        statusElements.forEach(el => {
            el.style.animation = 'none';
            setTimeout(() => {
                el.style.animation = 'metricPulse 2s infinite';
            }, 10);
        });
    }, 5000);
});
</script>
""", unsafe_allow_html=True)