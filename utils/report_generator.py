from datetime import date
import pandas as pd

def generate_report_text(threshold, analysis_mode, show_heatmap, similarity, change_percent, efficiency, total_pixels, changed_pixels, max_intensity, mean_intensity):
    status = 'АНОМАЛИЯ' if change_percent > threshold else 'НОРМА'
    conclusion = 'Обнаружены значительные изменения, требующие внимания' if change_percent > threshold else 'Значимых изменений не обнаружено, территория стабильна'
    
    return f"""==================================
ОТЧЁТ ОБ АНАЛИЗЕ GEO SCAN PRO
==================================

Дата анализа: {date.today()}
Время анализа: {pd.Timestamp.now().strftime('%H:%M:%S')}

--------------------------------
ПАРАМЕТРЫ АНАЛИЗА:
--------------------------------
• Порог обнаружения: {threshold}%
• Режим анализа: {analysis_mode}
• Тепловая карта: {'Да' if show_heatmap else 'Нет'}

--------------------------------
РЕЗУЛЬТАТЫ:
--------------------------------
• Сходство изображений: {similarity:.1f}%
• Обнаружено изменений: {change_percent:.2f}%
• Статус: {status}
• Эффективность анализа: {efficiency:.1f}%

--------------------------------
ДЕТАЛЬНАЯ СТАТИСТИКА:
--------------------------------
• Всего пикселей: {total_pixels:,}
• Изменённых пikселей: {changed_pixels:,}
• Макс. интенсивность: {max_intensity:.1f}
• Сред. интенсивность: {mean_intensity:.2f}

--------------------------------
ЗАКЛЮЧЕНИЕ:
--------------------------------
{conclusion}

==================================
СИСТЕМА АВТОМАТИЧЕСКОГО МОНИТОРИНГА
© 2026 GEO SCAN PRO
Контакты: yasya.ackerman@gmail.com
=================================="""