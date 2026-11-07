#!/usr/bin/env bash
# -------------------------------------------------------------------------
# Локальная проверка сборки APK через Docker.
# Повторяет те же шаги, что и GitHub Actions, но на вашей машине —
# чтобы поймать ошибки (libffi и др.) до push в репозиторий.
#
# Использование:
#   bash docker/build-apk-local.sh            # собрать debug-APK
#   bash docker/build-apk-local.sh shell      # открыть shell в контейнере
#   bash docker/build-apk-local.sh clean      # очистить кэш сборки (android/.buildozer, bin)
#
# Требуется только установленный Docker.
# -------------------------------------------------------------------------
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
APP_DIR="$ROOT/android"
IMAGE="cu-photoreports-builder:latest"

if ! command -v docker >/dev/null 2>&1; then
  echo "[!] Docker не найден. Установите Docker и повторите." >&2
  exit 1
fi

# UID/GID хоста — чтобы результаты сборки не оказались собственностью root.
if [ "$(uname -s)" = "Linux" ]; then
  HOST_UID="$(id -u)"
  HOST_GID="$(id -g)"
else
  # macOS / Docker Desktop — маппинг делается автоматически.
  HOST_UID=1000
  HOST_GID=1000
fi

cmd="${1:-build}"

case "$cmd" in
  clean)
    echo "[*] Удаляю android/.buildozer и android/bin ..."
    rm -rf "$APP_DIR/.buildozer" "$APP_DIR/bin"
    echo "[OK] Кэш сборки очищен."
    exit 0
    ;;
esac

echo "[*] Собираю Docker-образ ($IMAGE) ..."
docker build \
  --build-arg UID="$HOST_UID" \
  --build-arg GID="$HOST_GID" \
  -f "$HERE/Dockerfile.build" \
  -t "$IMAGE" \
  "$HERE"

if [ "$cmd" = "shell" ]; then
  echo "[*] Открываю shell в контейнере (каталог android/ смонтирован в ~/app) ..."
  exec docker run --rm -it \
    -v "$APP_DIR":/home/builder/app \
    "$IMAGE" bash
fi

echo "[*] Запускаю debug-сборку (первый раз долго — скачиваются SDK/NDK) ..."
# Кэш SDK/NDK/p4a ложится в android/.buildozer на хосте и переиспользуется.
docker run --rm -it \
  -v "$APP_DIR":/home/builder/app \
  -e ACLOCAL_PATH=/usr/share/aclocal \
  "$IMAGE" \
  bash -lc "buildozer -v android debug"

echo
if ls "$APP_DIR/bin/"*.apk >/dev/null 2>&1; then
  echo "[OK] APK собран:"
  ls -lh "$APP_DIR/bin/"*.apk
else
  echo "[!] APK не найден — смотрите лог выше, сборка остановилась на ошибке." >&2
  exit 1
fi
