import streamlit as st

def render_sidebar():
    with st.sidebar:
        # Заголовок
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 2rem; margin: 0; color: #00ffff;">GEO SCAN</h1>
            <p style="color: #00ffff; font-size: 0.8rem; margin: 5px 0; text-transform: uppercase;">Professional Edition</p>
            <div style="height: 2px; background: linear-gradient(90deg, transparent, #00ffff, transparent); margin: 15px 0;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # О проекте
        st.markdown("### О проекте")
        st.info("Система автоматического обнаружения и анализа изменений земной поверхности", icon="ℹ️")
        
        st.markdown("---")
        
        # Параметры анализа
        st.markdown("### Настройки")
        
        threshold = st.slider(
            "Порог обнаружения (%)",
            min_value=0.1, max_value=20.0, value=5.0, step=0.1
        )
        
        analysis_mode = st.selectbox(
            "Режим анализа",
            ["Стандартный", "Высокая точность", "Быстрый анализ"],
            index=0
        )
        
        st.markdown("---")
        
        # === ВОЗВРАЩАЕМ РАБОЧУЮ КНОПКУ СБРОСА ===
        st.markdown("### Действия")
        if st.button("🔄 Сбросить и загрузить новые фото", use_container_width=True):
            # Очищаем файлы из памяти приложения
            if 'img1' in st.session_state:
                del st.session_state['img1']
            if 'img2' in st.session_state:
                del st.session_state['img2']
            # Перезапускаем приложение, чтобы интерфейс обновился
            st.rerun()
        
        st.markdown("---")
        
        # Контакты
        st.markdown("### Контакты")
        st.markdown("""
        **Разработчик:** Яся Аккерман  
        **Email:** yasya.ackerman@gmail.com
        """)
    
    # Возвращаем 3 значения, чтобы не ломать main.py. 
    # Тепловую карту делаем всегда включенной (True), так как кнопка убрана.
    return threshold, analysis_mode, True