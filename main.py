import streamlit as st
from utils.style import add_custom_css
from components.sidebar import render_sidebar
from components.upload_section import render_upload_section
from components.results_section import render_results_section


# ========== НАСТРОЙКА СТРАНИЦЫ ==========
st.set_page_config(
    page_title="🛰️ GEO SCAN PRO | Мониторинг Земли",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:yasya.ackerman@gmail.com',
        'Report a bug': "mailto:yasya.ackerman@gmail.com",
        'About': "### 🏆 Конкурсный проект\nСистема автоматического анализа изменений земной поверхности."
    }
)

# Подключаем стили
add_custom_css()

# Инициализация session_state
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False

# ========== БОКОВАЯ ПАНЕЛЬ ==========
threshold, analysis_mode, show_heatmap = render_sidebar()

# ========== ГЛАВНЫЙ ЗАГОЛОВОК ==========
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
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 2.5rem; color: #00ffff;">🛰️</div>
        <h4>Спутниковый анализ</h4>
        <p>Работа с данными Sentinel-2, Landsat</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 2.5rem; color: #00ff88;">📈</div>
        <h4>AI алгоритмы</h4>
        <p>Нейросетевые модели обнаружения</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 2.5rem; color: #ff0080;">⚡</div>
        <h4>Реальное время</h4>
        <p>Мгновенная обработка данных</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========== ЗАГРУЗКА ИЗОБРАЖЕНИЙ ==========
uploaded = render_upload_section()

# ========== АНАЛИЗ ==========
if uploaded:
    img1_file, img2_file = uploaded
    render_results_section(img1_file, img2_file, threshold, analysis_mode, show_heatmap)
else:
    # Состояние без загруженных изображений
    st.markdown("---")
    
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("#### **🎯 ДЕМО-РЕЖИМ**")
        st.markdown("""
        Для тестирования системы:
        1. Скачай тестовые изображения выше
        2. Загрузи их в поля 'ДО' и 'ПОСЛЕ'
        3. Получи мгновенный анализ
        """)
    
    with d2:
        st.markdown("#### **📚 ИНСТРУКЦИЯ**")
        st.markdown("""
        **Рекомендации:**
        - Снимки одинакового размера
        - Форматы: PNG, JPG, TIFF
        - Мин. разрешение: 800×600
        - Макс. размер: 20 МБ
        """)
    
    with d3:
        st.markdown("#### **🏆 КОНКУРСНЫЙ ПРОЕКТ**")
        st.markdown("""
        **Особенности системы:**
        - Современный неоновый дизайн
        - Анимации и эффекты
        - Профессиональная аналитика
        - Экспорт отчётов
        """)
    
    st.markdown("---")
    
    # Баннер с контактами
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, rgba(255, 0, 128, 0.2), rgba(0, 255, 255, 0.2));
        border-radius: 15px; padding: 25px; text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.1); margin: 20px 0;">
        <h3 style="color: #ffffff; margin-bottom: 15px;">📞 НУЖНА ПОМОЩЬ?</h3>
        <p style="font-size: 1.1rem; margin-bottom: 10px;">
            <strong>Разработчик:</strong> Яся Аккерман<br>
            <strong>Почта:</strong> 
            <a href="mailto:yasya.ackerman@gmail.com" style="color: #00ffff;">yasya.ackerman@gmail.com</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ========== ФУТЕР ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;">
        🛰️ <strong>GEO SCAN PRO</strong> | Система автоматического мониторинга земной поверхности
    </p>
    <p style="color: rgba(255, 255, 255, 0.5); font-size: 0.8rem;">
        Версия 3.0 | © 2026 Конкурсный проект | Все права защищены
    </p>
</div>
""", unsafe_allow_html=True)