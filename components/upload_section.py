import os
import streamlit as st


def render_upload_section():
    """Рендерит блок загрузки изображений и возвращает пару (img1, img2) или None."""
    st.markdown("### 📤 **ЗАГРУЗКА СПУТНИКОВЫХ СНИМКОВ**")
    
    col1, col2 = st.columns(2)
    
    with col1:
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
    
    with col2:
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
    
    # Кнопки скачивания тестовых изображений
    st.markdown("---")
    st.markdown("### 🖼️ **ТЕСТОВЫЕ ИЗОБРАЖЕНИЯ ДЛЯ ПРОВЕРКИ**")
    st.info("💡 Скачай готовые примеры, чтобы сразу протестировать систему")
    
    tc1, tc2 = st.columns(2)
    
    # Тестовое изображение "ДО"
    with tc1:
        test_before_path = os.path.join('assets', 'images', 'test_before.png')
        if os.path.exists(test_before_path):
            with open(test_before_path, 'rb') as f:
                test_before_bytes = f.read()
            st.download_button(
                label="📥 Скачать тестовое фото 'ДО'",
                data=test_before_bytes,
                file_name="test_before.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            st.warning("⚠️ Файл `assets/images/test_before.png` не найден")
    
    # Тестовое изображение "ПОСЛЕ"
    with tc2:
        test_after_path = os.path.join('assets', 'images', 'test_after.png')
        if os.path.exists(test_after_path):
            with open(test_after_path, 'rb') as f:
                test_after_bytes = f.read()
            st.download_button(
                label="📥 Скачать тестовое фото 'ПОСЛЕ'",
                data=test_after_bytes,
                file_name="test_after.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            st.warning("⚠️ Файл `assets/images/test_after.png` не найден")
    
    st.markdown("---")
    
    if img1 and img2:
        return img1, img2
    return None