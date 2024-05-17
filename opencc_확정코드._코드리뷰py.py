from flask import Flask, render_template, request, jsonify
import json
import os
from konlpy.tag import Okt  # pip install konlpy
# from soynlp.tokenizer import RegexTokenizer
import pandas as pd 
from waitress import serve  # pip install waitress
import logging
import pymysql


# !pip install flask
# !pip install waitress

app = Flask(__name__, template_folder='templates', static_folder='static')
    #app = Flask(__name__,) 
        #<<<Flask라는 웹을 만든다 
    #template_folder = 'templates'
        #<<<HTML파일이 들어있는 폴더라 templates라는 것을 알려준다 
    #static_folder='static'
        #<<<CSS, 이미지 같은 정적 파일이 들어 있는 폴더가 'static'이라는것이다


logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.DEBUG) 로깅시스템을 설정하는 코드
        #로깅이란? 프로그램이 실행되는 동안 발생하는 다양한사건(정보,경고,오류)를기록하는것 로그를 남기면 프로그램의 동작을 추척하고오류를 찾아냄
        #로깅레벨을 'DEBUG'로 설정 - 
            #DEBUG: 상세한 디버깅 정보. 보통 개발 중에만 사용합니다.
            #INFO: 일반적인 정보 메시지. 프로그램이 정상적으로 동작하는 동안의 정보를 기록합니다.
            #WARNING: 경고 메시지. 프로그램이 작동은 하지만 문제가 발생할 수 있는 상황을 기록합니다.
            #ERROR: 오류 메시지. 프로그램이 특정 기능을 수행하지 못했음을 기록합니다.
            #CRITICAL: 심각한 오류 메시지. 프로그램이 계속 실행될 수 없음을 나타냅니다
    #level = logging.DEBUG로 설정하면 위에 나열된 모든 수준의 로그메세지가 기록된다.프로그램 실행중에 발생하는 모든 사건을 로그로 남기겠다

        #>>> 로깅사용하는이유 1)디버깅 2)상태추척 3)성능모니터링 4)오류 및 경고 로깅 5)감사 및보안
        #>>> 로깅은 프로그램을 이해하고 유지보수하며, 문제를 진단하고 해결하는 도구 
@app.route('/')
#웹사이트의 루트 페이지에 해당되는 내용을 처리 Flask애플리케이션에서 '/'경로에 대한 보낸다
def home():
    #home이라는 함수정의
    app.logger.info('Serving the "home" route')
    #"Serving the'home' route" 라는  메세지를 기록한다.
        #>>>홈페이지 경로를 서빙하고있다는 정보를 로그에 그린다
    return render_template('ex.html')
    #ex.html이라는 파일을 반환한다.
        #>>>이 함수를 통해 사용자에게 홈페이지의 내용을 보여준다
    # return os.getcwd()

@app.route('/send', methods=['POST'])
#웹 애플리케이션에 '/send'라는 URL 주소를 설정
    #>>>이 URL에 대해 POST방식 요청이 들어오면,'send'라는 함수실행
def send():
    app.logger.info('Serving the "send" route')
    #로그에 메세지를 남기며,'/send'경로에 서비스 중이라는 정도를남긴다'
    print(1)
    #숫자 1을 출력
        #>>>'/send'에 POST요청이 오면, 이 함수가 실행되고 로그를 기록하여 숫자 1을 출력한다

    data = request.get_json() 
    #클라이언트가 주는 정보가 request에 담아서 date로 줘서 받았다
    user_message = data.get('message', 'No message received')
    print(1)

    if user_message != 'No message received':
        app.logger.info('message: {}'.format(user_message))

        nouns_tagger = Okt()

        # nouns: 명사 추출, morphs: 형태소 추출, normalize: 메시지 그대로
        nouns = nouns_tagger.nouns(user_message)
        # morphs = nouns_tagger.morphs(user_message)
        normalize = nouns_tagger.normalize(user_message)
        pos = nouns_tagger.pos(user_message)
        # phrases = nouns_tagger.phrases(user_message)

        #user_message = {'message':[user_message], 'nouns':nouns, 'morphs':morphs, 'normalize':normalize, 'pos':pos, 'phrases':phrases}
        # answer_message_1 = f"'message':[{user_message}], 'nouns':{nouns}, 'morphs':{morphs}, 'normalize':{normalize}, 'pos':{pos}, 'phrases':{phrases}\n"
        answer_message_1 = f"\n'normalize':{normalize}, \n'pos':{pos}\n"

        conn = pymysql.connect(host='127.0.0.1', user='user', password='user1234', db='opencc', charset='utf8')
        cur = conn.cursor()

        # 경기도 화성시 30평대 제일 저렴한 매물 알려줘
        
        sql = "SELECT 시군구, 도로명, 단지명, 층, 건축년도, 계약년월, 계약일, 전용면적, 거래금액 FROM y21_경기도 WHERE 시군구 LIKE '%화성시%' AND 전용면적 BETWEEN 99.173554 AND 132.231405 ORDER BY 거래금액 ASC LIMIT 5"
        
        #>>>sql 다른버전
        sql = """
        SELECT 시군구,도로명,단지명,층,건축년도,계약년월,계약일,전용면적,거래금액
        FROM y_21경기도
        WHERE 시군구 LIKE'%화성시%'
        AND 전용면적 BETWEEN 99.173554 AND 132.231405
        ORDER BY 거래금액 ASC
        LTMIT 5;
        """
       
        #FROM y_21경기도 라는 테이블안에서의 칼럼인 시군구, 도로명, 단지명, 층, 건축년도, 계약년월,계약일, 전용면적, 거래금액 지정한다.
            # >>> 검토y21_경기도 테이블이름이 정확한지 확인하고 데이터베이스에 존재하는지 확인해야함.
        
        #시군구 LIKE '%화성시%'
            #>>>시군구열의 "화성시"가 들어간 열(아래 쭈우우욱)을 포함한다
            
        #AND 전용면적 BETWEEN 99.173554 AND 132.231405
            #>>>전용면적이 저정된 범위 (99.173554에서 132.231405제곱미터)내에 있는 행(오른쪽쭈우욱)내에 있는 행을 필터링한다.
            
        #ORDER BY 거래금액 ASC
            #>>> 거래금액을 오름차순으로 정리한다 
            #>>> 거래금액을 오름차순으로 정리하면 가장 저렴한 거래가 먼저 나온다. 오름차순 - 1,2,3,4,5  내림차순 - 5,4,3,2,1,
            
            
        #LIMIT절
            #>>>반환되는 행의 수를 5개로 제한합니다.
            #>>> 데이터의 샘플을 가져오거나 상위 결과만 필요할 때 유용하다. 데이터베이스의 부하를 줄이고 퀴리응답 속돌르 높이는데 도움이 된다. 
        
        
        cur.execute(sql)
        #execute - 실행하다.
            #python에서 데이터베이스 커서를 사용하여 SQL쿼리를 실행한다 
            #>>>'cur'가 데이터베이스 연결에서 유효한커서 객체인지 확인. 쿼리 실행중 오류가 발생할 경우를 대비해 적절한 예외처리를 추가하는 것이 좋다 .
        results = cur.fetchall()
        

        answer_message_2 = ''
        #print(results)
        for i in results:
            exclusive_area = f'{i[-2]}㎡'
            
            pyeong = f'{i[-2] * 0.3025:3.2f}평, '
            
            apartment = f'{i[2]} {str(i[3]):>2}층, '
            
            contact_y_m = str(i[5])
            
            contact_y_m_d = f'{contact_y_m[:4]}.{contact_y_m[4:]}.{i[6]:02}'
            
            #contact_y_m_d = f'{i[5]//100}.{i[5]%100:02}.{i[6]:02}'
            print(f'{i[0]+", ":<20}{i[1]+", ":<15}{apartment:<15}\t건축년도 {i[4]}년, \t{exclusive_area:10} {pyeong}\t{int(i[-1])//10000:4}억 {int(i[-1])%10000:4}만 원 \t계약일 {contact_y_m_d}')
            answer_message_2 += answer_message_2 + f'{i[0]+", ":<20}{i[1]+", ":<15}{apartment:<15}\t건축년도 {i[4]}년, \t{exclusive_area:10} {pyeong}\t{int(i[-1])//10000:4}억 {int(i[-1])%10000:4}만 원 \t계약일 {contact_y_m_d}\n'
        print()
        answer_message_2 += answer_message_2 + '\n'

        answer_message = answer_message_1 + answer_message_2

        response_data = {
            "reply": f"Received your message:{answer_message}"
        }

        app.logger.info('reply: {}'.format(answer_message))
    else:
        app.logger.info('No message received')

    print(data)

    print(1)


    # 객체를 bytes로 변경???
    print(jsonify(response_data))

    print(1)
    return jsonify(response_data)


# def tokenize_morpheme(question):
#     tokenizor = RegexTokenizer()
#
#     tokens = tokenizor.tokenize(question)
#
#     return tokens


if __name__ == '__main__':
    app.debug = True
    serve(app, host='localhost', port=5000)