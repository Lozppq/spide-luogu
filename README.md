# spide-luogu
先通过login.py手动登录获取Cookies，
在运行gethtml.py获取题解，
题解在gethtml.py同级目录下
chromedrver在目录里，可自行寻找，这个目前匹配的是我的最新版，该安装路径，要配置系统变量，或者把该exe文件，放到gethtml.py同级目录，如
```python
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options,executable_path='./chromeWebDriver')
```
最新版selenium需要python3.9以上的版本，其他的各种库文件需要自行安装
