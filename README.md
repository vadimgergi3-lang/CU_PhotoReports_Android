# CONTROL UNION — фото-отчёты (Android, offline)

Полноценное Android-приложение, которое делает то же, что и Telegram-бот CONTROL UNION,
но **без Telegram** и **без сети**. Весь сбор фото и генерация Word-отчёта
работают прямо на телефоне.

> Важно: документ формируется **тем же самым кодом** (`config.py` + `docgen.py` +
> `continue_report.py`), что и в боте — логотип, шрифты, размеры, объединённые
> подписи — отчёты получаются идентичными. Поэтому приложение сделано на
> Python/Kivy (Buildozer), а не переписано на Kotlin: это гарантирует полное
> совпадение результата с ботом.

## Что умеет приложение

- **Новый отчёт** — выбор шаблона (те же 6 шаблонов из `config.py`).
- **Метаданные** — № отчёта, место, груз, объём услуг, дата, подпись.
- **Контейнеры** — два способа ввода: серийные номера через разделитель
  или количество N (нумерация 1…N).
- **Пошаговый сбор фото** — галерея или камера, прогресс, список слотов.
- **Генерация `.docx`** и кнопка **«Отправить / Поделиться»**.
- **Продолжить из .docx** — разбор ранее созданного отчёта.
- **Восстановление** незавершённого отчёта после закрытия приложения.

Целевой Android: **13 и выше** (minSdk 33, target 34), архитектура `arm64-v8a`.

## Структура проекта

```
CU_PhotoReports_Android/
├─ .github/workflows/build-apk.yml   ← сборка APK на GitHub Actions
├─ .gitignore
├─ README.md
└─ android/
   ├─ main.py              ← UI (Kivy): экраны и логика
   ├─ config.py            ← шаблоны отчётов
   ├─ docgen.py            ← генерация Word-документа
   ├─ continue_report.py   ← «продолжить из .docx»
   ├─ buildozer.spec       ← настройки сборки
   ├─ prepare.sh
   ├─ BUILD_APK.md
   └─ assets/logo.png
```

Папка `android/` самодостаточна — все модули генератора лежат рядом с `main.py`.

---

## Сборка APK на GitHub (рекомендуемый способ)

1. Создайте новый репозиторий на GitHub (например `cu-photoreports-android`).
2. Залейте туда всё содержимое этого архива (вместе с папкой `.github/`):

   ```bash
   git init
   git add .
   git commit -m "CONTROL UNION offline Android app"
   git branch -M main
   git remote add origin https://github.com/<ваш-логин>/cu-photoreports-android.git
   git push -u origin main
   ```

3. Сборка запустится автоматически при push в `main`. Либо вручную:
   **Actions → Build Android APK → Run workflow**.
4. Когда сборка завершится (≈ 20–40 мин первый раз), откройте страницу запуска
   и скачайте артефакт **`fotoreportcu-apk`** (внутри — файл `.apk`).

Рабочий процесс (`.github/workflows/build-apk.yml`) сам:
- ставит Python 3.11, JDK 17, системные зависимости, Buildozer и Cython 0.29.36;
- проверяет наличие всех файлов в `android/`;
- собирает debug-APK и публикует его как артефакт.

## Сборка локально (Linux / WSL2)

```bash
sudo apt update && sudo apt install -y \
  git zip unzip openjdk-17-jdk autoconf libtool pkg-config \
  zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev build-essential ccache

pip install --user buildozer Cython==0.29.36

cd android
buildozer -v android debug
# готовый файл: android/bin/fotoreportcu-2.0.0-arm64-v8a-debug.apk
```

Первая сборка долгая — Buildozer скачивает Android SDK/NDK.

## Локальная проверка сборки через Docker

Если не хотите ставить toolchain на систему — проверьте сборку в контейнере
(то же окружение, что и в Actions, с исправлением libffi):

```bash
bash docker/build-apk-local.sh
```

Подробности — в `docker/README_DOCKER.md`. Требуется только установленный Docker.

## Установка на телефон

1. Перекиньте `.apk` на телефон.
2. Разрешите «Установка из неизвестных источников».
3. Установите. При первом запуске разрешите доступ к фото / камере.

## Замечания

- `.apk` из Actions — **debug** (подписан отладочным ключом), для личного
  использования этого достаточно. Для Google Play нужен release-APK/AAB
  с собственным keystore.
- По умолчанию собирается только `arm64-v8a`. Чтобы добавить 32-битные
  устройства, в `buildozer.spec` укажите `android.archs = arm64-v8a,armeabi-v7a`.
- Интерфейс — только русский, как в боте.
