[app]
title = Kayış Gergi Hesabı
package.name = beltkayis
package.domain = org.erdem
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# ---- Android Ayarları (ZORUNLU) ----
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
android.build_tools = 33.0.2
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
