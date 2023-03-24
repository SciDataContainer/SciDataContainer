@echo off
cd python
call build.bat
cd ..
set /p version=<python\VERSION
git add .
git commit -am "Version %version%"
git push -u origin main
