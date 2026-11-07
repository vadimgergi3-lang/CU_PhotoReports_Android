# Локальная проверка сборки APK через Docker

Эти два файла позволяют собрать тот же APK, что и в GitHub Actions, но локально —
чтобы ловить ошибки до push:

- `Dockerfile.build` — образ с Python 3.11 + JDK 17 + весь toolchain Buildozer.
  Включает то же исправление libffi: `automake`, `libtool-bin` и
  `ACLOCAL_PATH=/usr/share/aclocal`.
- `build-apk-local.sh` — скрипт запуска.

## Требования

Установленный Docker (Linux / macOS / Windows+WSL2). Больше ничего.

## Запуск

Из корня проекта:

```bash
bash docker/build-apk-local.sh
```

Первый запуск долгий (скачиваются Android SDK/NDK). Готовый файл появится в
`android/bin/*.apk`.

### Дополнительные режимы

```bash
bash docker/build-apk-local.sh shell   # shell внутри контейнера (ручная отладка)
bash docker/build-apk-local.sh clean   # удалить кэш android/.buildozer и android/bin
```

## Как это работает

- Каталог `android/` монтируется в контейнер, внутри выполняется
  `buildozer -v android debug`.
- Кэш SDK/NDK/p4a сохраняется на хосте в `android/.buildozer`, поэтому
  повторные сборки быстрые.
- Образ создаёт пользователя с вашим UID/GID (на Linux), чтобы файлы
  сборки не оказались собственностью root.

> Это близкое, но не 100% тождественное окружение с GitHub Actions
> (там Ubuntu, здесь Debian bookworm). Но версия Python, JDK, Buildozer,
> Cython и набор системных пакетов совпадают — этап libffi и похожие
> ошибки toolchain воспроизводятся одинаково.
