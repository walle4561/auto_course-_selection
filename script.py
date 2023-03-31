from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
import pytesseract
import cv2

import msvcrt, sys, os
import time

studentNumInput = input("請輸入學號：")
print("請輸入密碼：",end="",flush=True)

li = []
while 1:
    ch = msvcrt.getch()
    #回车
    if ch == b'\r':
        msvcrt.putch(b'\n')
        break
    #退格
    elif ch == b'\x08':
        if li:
            li.pop()
            msvcrt.putch(b'\b')
            msvcrt.putch(b' ')
            msvcrt.putch(b'\b')
    #Esc
    elif ch == b'\x1b':
        break
    else:
        li.append(ch)
        msvcrt.putch(b'*')

studentPwdInput = '%s' % b''.join(li).decode()
PATH = "C:/Users/walle4561/Desktop/auto_course _selection/edgedriver_win64msedgedriver.exe"
driver = webdriver.Edge(PATH)
driver.get("https://ntcbadm1.ntub.edu.tw/login.aspx")
driver.maximize_window()
driver.save_screenshot("full.png")
studentNum = driver.find_element(By.ID, 'UserID')
studentPwd = driver.find_element(By.NAME,"PWD")
studentNum.send_keys(studentNumInput)
studentPwd.send_keys(studentPwdInput)
# ==================================valid code=============================
validImg = driver.find_element(By.ID,"Validation_Image")
validImgLocation = validImg.location
validImgsize = validImg.size
rangle = (int(validImgLocation['x']),int(validImgLocation['y']),int(validImgLocation['x']+validImgsize['width']),int(validImgLocation['y']+validImgsize['height']))
fullWebPageImg = Image.open("full.png")
fincrop = fullWebPageImg.crop(rangle)
fincrop.save('validImg.png')

img = cv2.imread('validImg.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, validImgFin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY) 

# test image
# cv2.imshow('test',output1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

text = pytesseract.image_to_string(validImgFin, lang='eng')
print(text)
checkCode = driver.find_element(By.ID,"CheckCode")
checkCode.send_keys(text)
# ===============================跳轉畫面===================================

WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ThemePanelMainItem"))
)

themePanelMainItem = driver.find_element(By.CLASS_NAME,"ThemePanelMainItem")
themePanelMainItem.click()

driver.quit()