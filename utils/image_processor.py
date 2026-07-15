import io
from PIL import Image, ImageChops
import numpy as np
import streamlit as st


@st.cache_data
def load_image(image_file):
    """Загружает изображение и конвертирует в RGB."""
    try:
        image = Image.open(image_file).convert('RGB')
        return image
    except Exception as e:
        st.error(f"❌ Ошибка загрузки изображения: {e}")
        return None


def prepare_images(img1: Image.Image, img2: Image.Image):
    """Приводит изображения к одному размеру."""
    if img1.size != img2.size:
        st.warning(f"⚠️ Изображения разного размера. Второе будет масштабировано до {img1.size}")
        img2 = img2.resize(img1.size)
    return img1, img2


def calculate_difference(img1: Image.Image, img2: Image.Image):
    """Вычисляет разницу между двумя изображениями."""
    diff = ImageChops.difference(img1, img2).convert('L')
    diff_array = np.array(diff)
    
    change_percent = (np.mean(diff_array) / 255.0) * 100
    similarity = 100 - change_percent
    
    return diff, diff_array, change_percent, similarity


def create_heatmap(diff: Image.Image, diff_array: np.ndarray):
    """Создаёт цветную тепловую карту изменений."""
    heatmap = diff.convert('RGB')
    heatmap_array = np.array(heatmap)
    heatmap_array[:, :, 0] = np.clip(diff_array * 2, 0, 255)
    return Image.fromarray(heatmap_array)


def image_to_bytes(image: Image.Image, format: str = 'PNG') -> bytes:
    """Конвертирует PIL Image в байты для скачивания."""
    buf = io.BytesIO()
    image.save(buf, format=format)
    return buf.getvalue()