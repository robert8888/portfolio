

PWA_APP_NAME = 'Rkam dev'
PWA_APP_DESCRIPTION = "Robert Kaminski"
PWA_APP_THEME_COLOR = '#158e9e'
PWA_APP_BACKGROUND_COLOR = '#101317'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = '#101317'
PWA_APP_ICONS = [
    {
        'src': '/static/img/pwa-192x192.png',
        'sizes': '192x192'
    },{
        'src': '/static/img/pwa-512x512.png',
        'sizes': '512x512'
    },
    {
        'src': '/static/img/pwa_maskable_icon_192x192.png',
        'sizes': '192x192',
        "type": "image/png",
        "purpose": "any maskable"
    }, {
        'src': '/static/img/pwa_maskable_icon_512x512.png',
        'sizes': '512x512',
        "type": "image/png",
        "purpose": "any maskable"
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/img/pwa-192x192.png',
        'sizes': '192x192'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {'src':'/static/img/splashscreens/iphone5_splash.png','media':'(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'},
    {'src':'/static/img/splashscreens/iphone6_splash.png','media':'(device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2)'},
    {'src':'/static/img/splashscreens/iphoneplus_splash.png','media':'(device-width: 621px) and (device-height: 1104px) and (-webkit-device-pixel-ratio: 3)'},
    {'src':'/static/img/splashscreens/iphonex_splash.png','media':'(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)'},
    {'src':'/static/img/splashscreens/iphonexr_splash.png','media':'(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2)'},
    {'src':'/static/img/splashscreens/iphonexsmax_splash.png','media':'(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3)'},
    {'src':'/static/img/splashscreens/ipad_splash.png','media':'(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2)'},
    {'src':'/static/img/splashscreens/ipadpro1_splash.png','media':'(device-width: 834px) and (device-height: 1112px) and (-webkit-device-pixel-ratio: 2)'},
    {'src':'/static/img/splashscreens/ipadpro3_splash.png','media':'(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2)'},
    {'src':'/static/img/splashscreens/ipadpro2_splash.png','media':'(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2)'}
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

PWA_APP_DEBUG_MODE = False