@echo OFF
if not defined VIRTUAL_ENV (
  call .venv\Scripts\activate
)
pyinstaller --onefile --icon appicon.ico .\\src\\index.py