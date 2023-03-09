#-*- coding: utf-8 -*-
import sys
import json
from utagger_py import my_in, UTagger

print("프로그램 시작")
rt = UTagger.Load_global('../bin/UTaggerR64.dll', '../Hlxcfg.txt') #window dll
#rt = UTagger.Load_global('c:\\utagger solutions\\utagger share5\\bin\\UTaggerR64.dll', '..\\Hlxcfg.txt') #window dll 절대 경로

#rt = UTagger.Load_global('../bin/UTagger.so', '../Hlxcfg.txt') #linux UTagger.so

if rt!='':
    print(rt)
    sys.exit(1)

ut = UTagger(0) # 0은 객체 고유번호. 0~99 지정 가능. 같은 번호로 여러번 생성하면 안됨. 한 스레드당 하나씩 지정 필요.
rt = ut.new_ucma() #객체 생성. 객체가 있어야 유태거 이용 가능.
if rt!='':
    print(rt)
    sys.exit(1)

if __name__ == "__main__":

    menu = 1

    while(menu!=0):
        #my_in은 파이썬2에서도 utf8로 잘 작동하라고 만든 키보드 입력 함수다. 파이썬3은 그냥 input와 동일.
        menu = int( my_in(u'0.종료;  1.간단분석;  2. json으로 분석;  3.의존(통계);  4. 개체명;  5. 띄붙보정; 6.사용자말뭉치재학습 ' ) )
                        
        if menu==1:
            s = my_in('input line = ')
            rt = ut.tag_line(s, 3) #분석! 문장을 분석하여 단순한 bsp의 나열로 출력. json 형태 아님. 2번째 인자 '3'은 hlxcfg의 영향을 덜 받게 해주는 옵션.
            print(rt)
            
        if menu==2:
            s = my_in('input line = ')
            rt = ut.analyze1(s, 3, 1) #분석! 형태소로 분석하여 json 형태로 보여준다. 후보(동형이의어 수준)와 대역어 등 다양한 정보를 포함한다.
            #1 : 문장(들)
            #2 : 후보 개수 제한.
            #3 : 대역어 언어 코드. 0.없음. 1 영어. 2 일어. 3프랑스(불어) 4스페인 5아랍 6몽골 7베트남 8태국 9인도네시아 10러시아 11중국
            

            #print(rt)
            j = json.loads(rt)
            print(json.dumps(j, indent=4, sort_keys=True, ensure_ascii=False))
        
        if menu==3:
            #의존관계 분석기 통계
            s=my_in('depen: sentence = ')
            rt = ut.depen2(s)
            print(rt)
            j = json.loads(rt)
            print(json.dumps(j, indent=4, sort_keys=True, ensure_ascii=False))

        if menu==4: #개체명
            s=my_in('ner: sentence = ')
            rt = ut.ner(s)
            print(rt)
            j = json.loads(rt)
            print(json.dumps(j, indent=4, sort_keys=True, ensure_ascii=False))

        if menu==5: #띄붙보정
            s=my_in('erc: sentence = ')
            rt = ut.erc(s)
            print(rt)

        if menu==6: #사용자말뭉치 재학습
            rt = ut.reload_custom()
            print(rt)


    ut.release_ucma() #객체 해제
    UTagger.Release_global() #사전 해제
    print("종료")
