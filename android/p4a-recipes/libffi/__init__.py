"""
Локальный p4a-рецепт libffi — обход ошибки сборки:

    configure.ac:215: error: possibly undefined macro: LT_SYS_SYMBOL_USCORE
    autoreconf: error: /usr/bin/autoconf failed with exit status: 1

Причина: штатный рецепт берёт git-архив libffi без готового `configure`,
поэтому запускает autogen.sh/autoreconf. На Ubuntu 24.04 (libtool 2.4.7)
autoreconf не находит макрос LT_SYS_SYMBOL_USCORE, и сборка падает.

Решение: тянем официальный release-тарбол libffi, в котором `configure` уже
сгенерирован. Тогда рецепт пропускает autogen.sh и autoreconf вообще не
вызывается — макрос больше не нужен.
"""
from pythonforandroid.recipes.libffi import LibffiRecipe as _LibffiRecipe


class LibffiReleaseRecipe(_LibffiRecipe):
    # Версия с готовым release-архивом (содержит ./configure).
    version = "3.4.2"
    # Важно: именно release-asset (.../releases/download/...), а не git-архив.
    url = "https://github.com/libffi/libffi/releases/download/v{version}/libffi-{version}.tar.gz"
    # Патчи штатного рецепта рассчитаны на git-раскладку; для release-
    # тарбола они не нужны ␸ configure уже собран.
    patches = []


recipe = LibffiReleaseRecipe()
