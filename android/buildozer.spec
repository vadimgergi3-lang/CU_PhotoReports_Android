[app]

# Имя приложения и пакет
title = CONTROL UNION Reports
package.name = fotoreportcu
package.domain = ua.controlunion

# Каталог с исходниками
source.dir = .
source.include_exts = py,png,jpg,jpeg,txt,md,yaml,ttf
source.include_patterns = assets/*

version = 2.0.0

# Важно: lxml и python-docx фиксируются на совместимых версиях для Python 3.11/Android-target.
# Невязка между Cython 0.29.x и новой lxml на p4a оборачивается в ошибку компиляции
# src/lxml/etree.c: incomplete definition of type 'struct _frame'.
requirements = python3,kivy==2.3.0,pyjnius,android,pillow,lxml==5.2.2,python-docx==1.1.2,plyer

orientation = portrait
fullscreen = 0

# Android 13+ (min API 33) / target API 34
android.api = 34
android.minapi = 33
android.ndk_api = 33
# arm64-v8a покрывает все современные телефоны на Android 13+ и ускоряет сборку.
# Чтобы собрать и под старые 32-битные устройства, добавьте armeabi-v7a.
android.archs = arm64-v8a
android.accept_sdk_license = True

# Разрешения для галереи, камеры и хранения (Android 13+)
android.permissions = INTERNET,ACCESS_NETWORK_STATE,CAMERA,READ_MEDIA_IMAGES,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,POST_NOTIFICATIONS

android.wakelock = False

# Закрепляем проверенную связку тулчейна.
# p4a-master + NDK r28c ломают нативные рецепты (libffi/libxml2/lxml) на шаге create.
# NDK r25b + стабильный p4a — официально поддерживаемая для kivy 2.3.0 + api 34.
android.ndk = 25b
p4a.branch = v2024.01.21

# Локальные рецепты (переопределяют штатные).
# libffi — берём release-тарбол с готовым configure, чтобы не запускать
# autoreconf (падал на LT_SYS_SYMBOL_USCORE).
p4a.local_recipes = ./p4a-recipes

# Иконка (если есть)
# android.icon.filename = %(source.dir)s/assets/logo.png

[buildozer]
log_level = 2
warn_on_root = 1
