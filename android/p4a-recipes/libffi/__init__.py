"""
Самодостаточный локальный рецепт libffi — полностью заменяет штатный.

Почему не наследуемся от pythonforandroid.recipes.libffi:
при загрузке local-recipes p4a регистрирует этот файл под именем
`pythonforandroid.recipes.libffi`, и `from ... import ...` превращается в самоимпорт —
штатный класс не находится, и p4a тихо откатывается к стандартному
рецепту (git-архив → autogen.sh → autoreconf → падение на LT_SYS_SYMBOL_USCORE).

Решение: тянем официальный release-тарбол libffi (в нём `configure` уже
сгенерирован), поэтому autogen.sh/autoreconf не запускаются вообще.
"""
from multiprocessing import cpu_count
from os.path import exists, join

import sh
from pythonforandroid.recipe import Recipe
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory


class LibffiRecipe(Recipe):
    name = "libffi"
    version = "3.4.2"
    # Именно release-asset (.../releases/download/...), а НЕ git-архив:
    # в нём уже лежит готовый ./configure.
    url = "https://github.com/libffi/libffi/releases/download/v{version}/libffi-{version}.tar.gz"

    built_libraries = {"libffi.so": ".libs"}

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            # У release-тарбола configure уже есть — autogen не нужен.
            if not exists("configure"):
                shprint(sh.Command("./autogen.sh"), _env=env)
            shprint(
                sh.Command("./configure"),
                "--host=" + arch.command_prefix,
                "--prefix=" + self.get_build_dir(arch.arch),
                "--disable-builddir",
                "--enable-shared",
                _env=env,
            )
            shprint(sh.make, "-j", str(cpu_count()), "libffi.la", _env=env)

    def get_include_dirs(self, arch):
        # Рецепт python3 вызывает этот метод, чтобы подключить заголовки libffi.
        return [join(self.get_build_dir(arch.arch), "include")]


recipe = LibffiRecipe()
