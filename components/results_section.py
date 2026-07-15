import streamlit as st
import pandas as pd
import plotly.express as px
from utils.image_processor import (
    load_image, prepare_images, calculate_difference,
    create_heatmap, image_to_bytes
)
from utils.report_generator import generate_report_text


def render_results_section(img1_file, img2_file, threshold, analysis_mode, show_heatmap):
    """Рендерит блок с результатами анализа."""
    
    # Прогресс-бар имитации
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(101):
        progress_bar.progress(i)
        if i == 25:
            status_text.text("🔍 **ЗАГРУЗКА ИЗОБРАЖЕНИЙ... 25%**")
        elif i == 50:
            status_text.text("🔍 **ВЫЧИСЛЕНИЕ РАЗЛИЧИЙ... 50%**")
        elif i == 75:
            status_text.text("🔍 **АНАЛИЗ АНОМАЛИЙ... 75%**")
        elif i == 100:
            status_text.text("✅ **АНАЛИЗ ЗАВЕРШЁН!**")
    
    # Загрузка и подготовка
    image1 = load_image(img1_file)
    image2 = load_image(img2_file)
    if not image1 or not image2:
        return
    image1, image2 = prepare_images(image1, image2)
    
    # Анализ
    diff, diff_array, change_percent, similarity = calculate_difference(image1, image2)
    efficiency = 100 - (change_percent * 0.5)
    
    # === Визуализация ===
    st.markdown("### 🖼️ **ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ**")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### **СНИМОК 'ДО'**")
        st.image(image1, use_container_width=True)
        st.caption(f"📏 **Размер:** {image1.size[0]}×{image1.size[1]} px")
        
        # Кнопка скачивания оригинала
        st.download_button(
            "📥 Скачать 'ДО'",
            data=image_to_bytes(image1),
            file_name="image_before.png",
            mime="image/png",
            use_container_width=True
        )
    
    with c2:
        st.markdown("#### **СНИМОК 'ПОСЛЕ'**")
        st.image(image2, use_container_width=True)
        st.caption(f"📏 **Размер:** {image2.size[0]}×{image2.size[1]} px")
        
        st.download_button(
            "📥 Скачать 'ПОСЛЕ'",
            data=image_to_bytes(image2),
            file_name="image_after.png",
            mime="image/png",
            use_container_width=True
        )
    
    with c3:
        st.markdown("#### **КАРТА ИЗМЕНЕНИЙ**")
        if show_heatmap:
            heatmap = create_heatmap(diff, diff_array)
            st.image(heatmap, use_container_width=True)
            st.caption("🔥 **Тепловая карта:** Красный = максимальные изменения")
            st.download_button(
                "📥 Скачать карту",
                data=image_to_bytes(heatmap),
                file_name="change_heatmap.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            st.image(diff, use_container_width=True)
            st.caption("⚫ **Ч/Б карта:** Белый = изменения")
            st.download_button(
                "📥 Скачать карту",
                data=image_to_bytes(diff),
                file_name="change_map.png",
                mime="image/png",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # === Метрики ===
    st.markdown("### 📊 **АНАЛИТИКА И МЕТРИКИ**")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("**СХОДСТВО**", f"{similarity:.1f}%",
                  delta=f"{(similarity - 50):+.1f}%" if similarity != 50 else "0%")
    with m2:
        st.metric("**ИЗМЕНЕНИЯ**", f"{change_percent:.2f}%",
                  delta=f"{(change_percent - threshold):+.2f}%",
                  delta_color="inverse")
    with m3:
        status = "⚠️ АНОМАЛИЯ" if change_percent > threshold else "✅ НОРМА"
        st.metric("**СТАТУС**", status,
                  delta="Превышен" if change_percent > threshold else "В норме")
    with m4:
        st.metric("**ЭФФЕКТИВНОСТЬ**", f"{efficiency:.1f}%",
                  delta=f"{(efficiency - 80):+.1f}%" if efficiency != 80 else "0%")
    
    st.markdown("---")
    
    # === Детальная статистика ===
    with st.expander("📈 **ДЕТАЛЬНАЯ СТАТИСТИКА И ГРАФИКИ**", expanded=True):
        sc1, sc2 = st.columns(2)
        
        with sc1:
            st.markdown("#### **ЦИФРОВЫЕ ПОКАЗАТЕЛИ**")
            stats_df = pd.DataFrame({
                "Показатель": [
                    "Общее количество пикселей",
                    "Изменённых пикселей",
                    "Максимальная яркость разницы",
                    "Средняя яркость разницы",
                    "Стандартное отклонение",
                    "Пикселей выше порога"
                ],
                "Значение": [
                    f"{diff_array.size:,}",
                    f"{int((diff_array > 50).sum()):,}",
                    f"{diff_array.max():.1f}",
                    f"{diff_array.mean():.2f}",
                    f"{diff_array.std():.3f}",
                    f"{int((diff_array > threshold * 2.55).sum()):,}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with sc2:
            st.markdown("#### **ГРАФИК РАСПРЕДЕЛЕНИЯ**")
            hist_df = pd.DataFrame({'Интенсивность': diff_array.flatten()})
            fig = px.histogram(
                hist_df, x='Интенсивность', nbins=50,
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
    
    st.markdown("---")
    
    # === Итоговый отчёт ===
    rc1, rc2 = st.columns([3, 1])
    
    with rc1:
        if change_percent > threshold:
            st.error(f"""
            ## 🚨 **ОБНАРУЖЕНЫ КРИТИЧЕСКИЕ ИЗМЕНЕНИЯ!**
            
            - **📊 Площадь изменений:** {change_percent:.2f}% (порог: {threshold}%)
            - **⚠️ Превышение порога:** {(change_percent - threshold):.2f}%
            - **📅 Рекомендуемые действия:** Срочная проверка территории
            
            **Возможные причины:** строительные работы, изменение ландшафта, природные явления.
            """)
        else:
            st.success(f"""
            ## ✅ **ТЕРРИТОРИЯ СТАБИЛЬНА**
            
            - **📊 Площадь изменений:** {change_percent:.2f}% (порог: {threshold}%)
            - **📈 Запас до порога:** {(threshold - change_percent):.2f}%
            - **📅 Статус:** Мониторинг не выявил критических изменений
            
            **🎯 Система рекомендует продолжить регулярный мониторинг.**
            """)
    
    with rc2:
        report_text = generate_report_text(
            threshold=threshold,
            analysis_mode=analysis_mode,
            show_heatmap=show_heatmap,
            similarity=similarity,
            change_percent=change_percent,
            efficiency=efficiency,
            total_pixels=int(diff_array.size),
            changed_pixels=int((diff_array > 50).sum()),
            max_intensity=float(diff_array.max()),
            mean_intensity=float(diff_array.mean()),
        )
        
        st.download_button(
            "📥 **СКАЧАТЬ ОТЧЁТ**",
            data=report_text,
            file_name=f"geo_scan_report.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )