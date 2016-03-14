:: Simple build script
:: Pyinstaller must be installed: python -m pip install pyinstaller
:: The Python Scripts folder must be in your %PATH%
pyinstaller --clean --version-file=VERSION --onefile dir_diff.py