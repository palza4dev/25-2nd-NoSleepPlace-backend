# 🌅 NoSleepPlace Project

- 촬영 장소 예약 플랫폼 HourPlace를 모티브로 한 팀 프로젝트


## 👩‍👩‍👧‍👦 팀 소개

- 팀명 : NoSleepPlace 
- 개발 기간 : 2021.10.18 ~ 2021.10.29
- 개발 인원
  - [FrontEnd](https://github.com/wecode-bootcamp-korea/25-2nd-NoSleepPlace-frontend) 3명 : [전태양](https://github.com/xodid157), [강성구](), [성해호]()
  - [BackEnd](https://github.com/wecode-bootcamp-korea/25-2nd-NoSleepPlace-backend) 2명 : [문승준](https://github.com/palza4dev), [김주현]()

## 🎬 프로젝트 구현 영상(사진 클릭시 유튜브 링크로 연결)

[![](https://user-images.githubusercontent.com/80348575/139586650-9d5195e7-0c74-45a2-bcff-aa2797f9894f.gif)](https://www.youtube.com/watch?v=gMjL4kwj8cE)


## ⚙️ 적용기술

- FrontEnd : React, HTML5, CSS3 , Styled Components
- BackEnd : Python, Django, MySQL, EC2, RDS
- Communication : Git, GitHub, Trello, Slack, PostMan

## 💾 DB 모델링 
![스크린샷 2021-12-07 오후 6 40 16](https://user-images.githubusercontent.com/72376931/145012694-8fe0d35a-0977-44df-bdd6-f4b1577dd438.png)




## 📒 구현기능

공통

- DB 모델링
- API 문서 작성 및 업데이트



문승준

- 카카오 API을 활용해 소셜 회원가입 및 로그인 기능
- JWT를 사용한 인증&인가와 회원 프로필 조회 기능
- 장소별 캘린더 조회시 예약정보 전송 기능 
- 장소별 예약 및 현황별 예약 조회 기능
- EC2와 RDS를 연동한 백엔드 서버 배포


김주현

- 메뉴, 카테고리별 장소 조회
- 장소 리스트 전체 조회
- 가격순, 등록순 장소 리스트 조회
- 키워드 검색으로 장소 조회

## ⌨️ API EndPoint

- [API 문서 링크](https://documenter.getpostman.com/view/17676214/UV5f7tWj)

- 회원관리
  - `POST` /users/account/kakao
  - `GET` /users/profile
  
- 상품조회
  - `GET` /places?menu=<menu_id>
  - `GET` /places?category=<category_id>
  - `GET` /places
  - `GET` /places?order=price
  - `GET` /places?order=-created_at
  - `GET` /places?keyword=<검색단어>
  - `GET` /places/<place_id>
  - `GET` /places/<place_id>/calendar?time=<연월시정보(datatime)>&days=<날짜기간(integer)>

- 예약관리
  - `POST` /books
  - `GET` /books?status=<status_code>



## ❗️ Reference

- 이 프로젝트는 [HourPlace](https://hourplace.co.kr/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
