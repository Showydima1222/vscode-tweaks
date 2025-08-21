# VSCode Tweaks
this program generates for you a .css file and applying it to your vscode if you have installed [Cutsom UI Plguin](https://marketplace.visualstudio.com/items?itemName=subframe7536.custom-ui-style)

# How to install [WINDOWS WAY]
You can install executable file builded with pyautoinstaller from releases. This way is easy, but your antivirus can mark this .exe file as virus (not my issue, so you can manually insatll it)

# How to install
1. Install python 3.11+
2. clone source code
3. run `pip install pyqt6`
4. go to directrory with sources
5. in this directory run `python main.py` (or write absolute path to main.py file)

# How to use
1. Install [Cutsom UI Plguin](https://marketplace.visualstudio.com/items?itemName=subframe7536.custom-ui-style) plugin in VSCode.
2. Run the program, go to project and create new.
3. Name it how you like, i recommend do not use spaces to avoid any path problems
4. Select tweaks
5. Save (in project tab) project if you want to save progress
6. Go to project, save to .css and apply manually file in settings.json or Apply from program (If windows, if your pc running another os see below how to apply it manually)
7. Go to vscode, press `CTRL` + `SHIFT` + `P`, type "ui:reload" (Custom UI Style:Reload) and press enter
8. Press restart app in apperaed notification

# How to apply .css file manually?
Go to vscode, open `Settings -> Extentions -> Custom UI Style -> External: Imports`. Press `Edit in settings.json`. Enter `file://[PATH TO YOUR FILE]`. Save and continue original how to use steps.
