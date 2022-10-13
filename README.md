# install package
```
pip install pyside6
pip install pikepdf
pip install fpdf2
pip install pyinstaller
```
# git
## initialize
```
git init
git remote add pdf https://github.com/gemini910610/pdf.git
```
## pull
```
git pull pdf master
```
## push
```
git add .
git commit -m "your commit message"
git push pdf master
```
# .gitignore
* 不要被上傳的檔案
# pyinstaller
```
@pyinstaller main.py -w -F -p ./.venv/Lib/site-packages --copy-metadata pikepdf
@rmdir build /s /q
@del main.spec
@copy MicrosoftYaHeiMono-CP950.ttf dist\MicrosoftYaHeiMono-CP950.ttf
```
> **`-w`** hide console when run exe<br>
> **`-F`** only output one file<br>
> **`-p`** python site-packages path
