# 这个 hook 会告诉 PyInstaller 自动收集 FastApi 目录下的所有子模块。
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('FastApi')
