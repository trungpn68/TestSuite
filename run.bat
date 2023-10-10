@echo off
setlocal

rem Run the provided Python script (replace with your script's path)
./venv/Scripts/python testcase.py --url "http://192.168.101.101:1234/convert" --repeat 1 --request-json requestInfo.json "Đường dẫn thư mục ảnh"
endlocal
