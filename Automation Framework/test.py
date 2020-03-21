from Excel_keyworks.webkeys import Web

web = Web()
web.openbrowser('google')
web.openurl('https://www.baidu.com')
web.sendkeys('//*[@id="kw"]','大肥猫')
web.click('#su')