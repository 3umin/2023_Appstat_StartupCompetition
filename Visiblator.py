import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import easyocr

reader = easyocr.Reader(['ko'])
result = reader.readtext('D:/Kak.jpg')

read_text = ''

for i in range(len(result)):
    read_text += result[i][1]

print('OCR로 인식된 문장 : ', read_text)

# 맞춤법 맞추기
from hanspell import spell_checker
read_text = spell_checker.check(read_text).as_dict()['checked']
print('맞춤법 검사된 문장 : ',read_text)

from konlpy.tag import Okt

okt = Okt()
po = okt.pos(read_text, norm=True, stem=True, join=True)

import fnmatch

list_rm = ["*/Josa", "*/Punctuation"]

for pos in po:
    for i in list_rm:
        if fnmatch.fnmatch(pos, i):
            po.remove(pos)

import re

for i in range(len(po)):
    po[i] = re.sub('[/A-z]', '', po[i])

for i in range(len(po)):
    po[i] = po[i] + '.mp4'

po[2] = '것.mp4'

print(po)

import cv2
# po = ['본인.mp4', '먹다.mp4', '거.mp4', '본인.mp4', '알다.mp4', '치우다.mp4', '회장.mp4']
# po는 위에서 형태소분석기 거쳐서 저장됨

for i in po:
    Vid = cv2.VideoCapture('D:/' + i)

    if Vid.isOpened():
        fps = Vid.get(cv2.CAP_PROP_FPS)
        f_count = Vid.get(cv2.CAP_PROP_FRAME_COUNT)
        f_width = Vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        f_height = Vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        print('Word : ', i[:-4])

    while Vid.isOpened():
        ret, frame = Vid.read()
        if ret:
            re_frame = cv2.resize(frame, (round(f_width / 1.5), round(f_height / 1.5)))
            cv2.imshow('hand_Video', re_frame)
            key = cv2.waitKey(10)

            if key == ord('q'):
                break
        else:
            break

Vid.release()
cv2.destroyAllWindows()