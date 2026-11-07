# Dispositivos e resoluções (Nome — Resolução):
#   Desktop     (1920x1080)
#   Smartphone  (360x800)
#   Tablet      (768x1024)
#   iPhone 17   (402x874)
#
# A área visível de cada dispositivo é aplicada pelo protocolo do Chrome (CDP),
# com largura, altura, densidade de pixels, toque e user agent exatos.

DESKTOP_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
ANDROID_USER_AGENT = 'Mozilla/5.0 (Linux; Android 14; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36'
IPHONE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'

DEVICES = {
    'desktop': {'width': 1920, 'height': 1080, 'pixel_ratio': 1, 'mobile': False, 'touch': False, 'user_agent': DESKTOP_USER_AGENT},
    'mobile': {'width': 360, 'height': 800, 'pixel_ratio': 2.75, 'mobile': True, 'touch': True, 'user_agent': ANDROID_USER_AGENT},
    'tablet': {'width': 768, 'height': 1024, 'pixel_ratio': 1, 'mobile': False, 'touch': False, 'user_agent': DESKTOP_USER_AGENT},
    'iphone17': {'width': 402, 'height': 874, 'pixel_ratio': 3, 'mobile': True, 'touch': True, 'user_agent': IPHONE_USER_AGENT},
}

DEVICE_LABELS = {
    'desktop': '🖥️  DESKTOP (1920x1080)',
    'mobile': '📱 RESPONSIVO — Smartphone (360x800)',
    'tablet': '📐 RESPONSIVO — Tablet (768x1024)',
    'iphone17': '📱 RESPONSIVO — iPhone 17 (402x874)',
}

SUMMARY_LABELS = {
    'desktop': 'Desktop (1920x1080)',
    'mobile': 'Smartphone (360x800)',
    'tablet': 'Tablet (768x1024)',
    'iphone17': 'iPhone 17 (402x874)',
}
