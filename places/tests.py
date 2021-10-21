import jwt

from django.test           import TestCase, Client

from nosleepplace.settings import SECRET_KEY
from places.models         import Menu, Category, Place, City, Host, Image
from users.models          import User
from books.models          import Book, BookStatus

class PlaceListTest(TestCase):
    def setUp(self):     
        Menu.objects.create(
            id   = 1,
            name = '가정집',
        )
        
        Menu.objects.create(
            id   = 2,
            name = '스튜디오',
        )
        Category.objects.create(
            id      = 1,
            name    = '주택',
            menu_id = 1,
        )
        
        Category.objects.create(
            id      = 3,
            name    = '빈티지',
            menu_id = 2 
        )
        City.objects.create(
            id   = 1,
            name = '서울'
        )
        Host.objects.create(
            id = 1,
            name = '빌리',
            profile_image = 'https://cdn.pixabay.com/photo/2017/07/10/11/28/bulldog-2489829_1280.jpg'
        ) 
        
        Place.objects.create(
            id           = 1,
            name         = '마루비 성산 - 80년대 주택을 개조한 빈티지 스튜디오 1F ',
            category_id  = 1,
            host_id      = 1,
            city_id      = 1,
            price        = 66000,
            minimum_time = 2,
            description  = '<p>마루비 동교에 이어 두번째 스튜디오를 만들었습니다. 이곳은 80년대 지어진 2층 단독 건물로 천장이 예쁘고 나무 루바로 된 벽이나 아치형 도어 등 요즘 주택에서 찾아보기 힘든 멋진 디테일이 있습니다. 바닥 및 가구는 고재 소나무 폐교마루를 시공해 제작하였으며 자연스럽지만 잘 정돈된 생활공간(1F)을 만들고자 하였습니다. <br><br> 촬영가능시간 7-22시</p>',
            capacity     = '기본 7명',
            size         = '35평 / 116m²',
            floor        = '지상 1층',
            parking      = '주차 3대 가능',
            location_info= '<p>주차는 단층 임대시 2대, 1-2층 통으로 임대 시 최대 6대까지 가능합니다. 조용한 성산동에 있으며 마포중앙도서관 걸어서 5분거리, 마포구청 걸어서 10분거리입니다. 식사는 중앙도서관 내 식당 이용하시는걸 추천드립니다.</p>'
        )
        
        Image.objects.create(
            id      = 1,
            url     = 'https://images.unsplash.com/photo-1536437075651-01d675529a6b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2340&q=80',
            place_id= 1
        )
        
        Image.objects.create(
            id      = 2,
            url     = 'https://images.unsplash.com/photo-1536437155202-feece465c323?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=3387&q=80',
            place_id= 1
        )
        
        Image.objects.create(
            id      = 3,
            url     = 'https://images.unsplash.com/photo-1471476730017-8169d050fa19?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1010&q=80',
            place_id= 1
        )      

    def tearDown(self):
        Place.objects.all().delete()   
        
    def test_authorview_post_success(self):
        client   = Client()
        response = client.get('/places?menu=1')
        self.assertEqual(response.json(),
                {
                "result": [
                        {
                        "id"        : 1,
                        "place_name": "마루비 성산 - 80년대 주택을 개조한 빈티지 스튜디오 1F ",
                        "price"     : 66000,
                        "capacity"  : "기본 7명",
                        "city"      : "서울",
                        "parking"   : "주차 3대 가능",
                        "url"       : [
                            "https://images.unsplash.com/photo-1536437075651-01d675529a6b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2340&q=80",
                            "https://images.unsplash.com/photo-1536437155202-feece465c323?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=3387&q=80",
                            "https://images.unsplash.com/photo-1471476730017-8169d050fa19?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1010&q=80"
                            ]
                        }
                    ]
                }       
            )
        self.assertEqual(response.status_code, 200)       

class PlaceDetailView(TestCase):
    def setUp(self):  
        Menu.objects.create(
            id   = 1,
            name = '가정집',
        )
        
        Menu.objects.create(
            id   = 2,
            name = '스튜디오',
        )
        Category.objects.create(
            id      = 1,
            name    = '주택',
            menu_id = 1,
        )
        
        Category.objects.create(
            id      = 3,
            name    = '빈티지',
            menu_id = 2
        )
        City.objects.create(
            id   = 1,
            name = '서울'
        )
        Host.objects.create(
            id   = 1,
            name = '빌리',
            profile_image = 'https://cdn.pixabay.com/photo/2017/07/10/11/28/bulldog-2489829_1280.jpg'
        ) 

        Place.objects.create(
            id            = 1,
            name          = '마루비 성산 - 80년대 주택을 개조한 빈티지 스튜디오 1F',
            category_id   = 1,
            host_id       = 1,
            city_id       = 1,
            price         = 66000,
            minimum_time  = 2,
            description   = '<p>마루비 동교에 이어 두번째 스튜디오를 만들었습니다. 이곳은 80년대 지어진 2층 단독 건물로 천장이 예쁘고 나무 루바로 된 벽이나 아치형 도어 등 요즘 주택에서 찾아보기 힘든 멋진 디테일이 있습니다. 바닥 및 가구는 고재 소나무 폐교마루를 시공해 제작하였으며 자연스럽지만 잘 정돈된 생활공간(1F)을 만들고자 하였습니다. <br><br> 촬영가능시간 7-22시</p>',
            capacity      = '기본 7명',
            size          = '35평 / 116m²',
            floor         = '지상 1층',
            parking       = '주차 3대 가능',
            location_info = '<p>주차는 단층 임대시 2대, 1-2층 통으로 임대 시 최대 6대까지 가능합니다. 조용한 성산동에 있으며 마포중앙도서관 걸어서 5분거리, 마포구청 걸어서 10분거리입니다. 식사는 중앙도서관 내 식당 이용하시는걸 추천드립니다.</p>'
        )
        
        Image.objects.create(
            id = 1,
            url = 'https://images.unsplash.com/photo-1536437075651-01d675529a6b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2340&q=80',
            place_id = 1
        )
        
        Image.objects.create(
            id = 2,
            url = 'https://images.unsplash.com/photo-1536437155202-feece465c323?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=3387&q=80',
            place_id = 1
        )
        
        Image.objects.create(
            id = 3,
            url = 'https://images.unsplash.com/photo-1471476730017-8169d050fa19?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1010&q=80',
            place_id = 1
        )       
        
    def tearDown(self):
        Place.objects.all().delete(),
        
    def test_authorview_post_success(self):
        client   = Client()
        response = client.get('/places/1')
        self.assertEqual(response.json(),
            {
                "result": 
                    {
                        "id"           : 1,
                        "place_name"   : "마루비 성산 - 80년대 주택을 개조한 빈티지 스튜디오 1F",
                        "category"     : "주택",
                        "city"         : "서울",
                        "minimum_time" : 2,
                        "description"  : "<p>마루비 동교에 이어 두번째 스튜디오를 만들었습니다. 이곳은 80년대 지어진 2층 단독 건물로 천장이 예쁘고 나무 루바로 된 벽이나 아치형 도어 등 요즘 주택에서 찾아보기 힘든 멋진 디테일이 있습니다. 바닥 및 가구는 고재 소나무 폐교마루를 시공해 제작하였으며 자연스럽지만 잘 정돈된 생활공간(1F)을 만들고자 하였습니다. <br><br> 촬영가능시간 7-22시</p>",
                        "capacity"     : "기본 7명",
                        "price"        : 66000,
                        "parking"      : "주차 3대 가능",
                        "size"         : "35평 / 116m²",
                        "floor"        : "지상 1층",
                        "url"          : [
                            "https://images.unsplash.com/photo-1536437075651-01d675529a6b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2340&q=80",
                            "https://images.unsplash.com/photo-1536437155202-feece465c323?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=3387&q=80",
                            "https://images.unsplash.com/photo-1471476730017-8169d050fa19?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1010&q=80"
                        ],
                        "location_info": "<p>주차는 단층 임대시 2대, 1-2층 통으로 임대 시 최대 6대까지 가능합니다. 조용한 성산동에 있으며 마포중앙도서관 걸어서 5분거리, 마포구청 걸어서 10분거리입니다. 식사는 중앙도서관 내 식당 이용하시는걸 추천드립니다.</p>"
                        
                    }
                
            }     
            )
        self.assertEqual(response.status_code, 200)

class PlaceCalendarTest(TestCase):
    def setUp(self):
        Menu.objects.create(
            id   = 1,
            name = '가정집',
        )
        
        Category.objects.create(
            id      = 1,
            name    = '주택',
            menu_id = 1,
        )
        
        City.objects.create(
            id   = 1,
            name = '서울'
        )
        
        Host.objects.create(
            id   = 1,
            name = '빌리',
            profile_image = 'https://cdn.pixabay.com/photo/2017/07/10/11/28/bulldog-2489829_1280.jpg'
        )
        
        Place.objects.create(
            id            = 1,
            name          = '마루비 성산 - 80년대 주택을 개조한 빈티지 스튜디오 1F ',
            category_id   = 1,
            host_id       = 1,
            city_id       = 1,
            price         = 66000,
            minimum_time  = 2,
            description   = '<p>마루비 동교에 이어 두번째 스튜디오를 만들었습니다. 이곳은 80년대 지어진 2층 단독 건물로 천장이 예쁘고 나무 루바로 된 벽이나 아치형 도어 등 요즘 주택에서 찾아보기 힘든 멋진 디테일이 있습니다. 바닥 및 가구는 고재 소나무 폐교마루를 시공해 제작하였으며 자연스럽지만 잘 정돈된 생활공간(1F)을 만들고자 하였습니다. <br><br>* 촬영가능시간 7-22시</p>',
            capacity      = '기본 7명',
            size          = '35평 / 116m²',
            floor         = '지상 1층',
            parking       = '주차 3대 가능',
            location_info = '<p>\n주차는 단층 임대시 2대, 1-2층 통으로 임대 시 최대 6대까지 가능합니다. 조용한 성산동에 있으며 마포중앙도서관 걸어서 5분거리, 마포구청 걸어서 10분거리입니다. 식사는 중앙도서관 내 식당 이용하시는걸 추천드립니다.\n</p>'
        )
        
        user = User.objects.create(
            id            = 1,
            kakao_id      = '1960067483',
            nickname      = '성해호',
            profile_image = 'http://k.kakaocdn.net/dn/cnv4DE/btq7DsQ0kM6/mTFyVTEeGMzEbakRv72iKK/img_110x110.jpg',
            email         = 'soh308@nate.com',
            age_range     = '30~39'
        )
        
        BookStatus.objects.create(
            id     = 1,
            status = "대기" 
        )
        
        Book.objects.create(
            id             = 1,
            user_id        = 1,
            place_id       = 1,
            date           = "2021-10-28",
            start_time     = "2021-10-28T02:00:00",
            end_time       = "2021-10-28T04:00:00",
            head_count     = 3,
            total_price    = 224000,
            content_type   = "촬영 소개",
            content_info   = "촬영 내용",
            status_code_id = 1
        )
        
        self.access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
        
    def tearDown(self):
        Place.objects.all().delete()
        User.objects.all().delete()
        Book.objects.all().delete()
    
    def test_place_calendar_get_success(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        response = client.get('/places/1/calendar?days=30&time=2021-10-21T12:00:00', **headers)
        self.assertEqual(response.json(),
            {
                "result" : [
                    {
                        "start_time" : "2021-10-28T02:00:00",
                        "end_time"   : "2021-10-28T04:00:00",
                        "usage_time" : "2"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_place_calendar_get_invalid_place_id_fail(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        response = client.get('/places/99/calendar?time=2021-10-21T12:00:00', **headers)
        
        self.assertEqual(response.json(),{"message":"INVALID_PLACE_ID"})
        self.assertEqual(response.status_code, 404)
        
    def test_place_calendar_get_value_error_fail(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        response = client.get('/places/1/calendar?time=2021-10-21T12', **headers)
        
        self.assertEqual(response.json(),{"message":"VALUE_ERROR"})
        self.assertEqual(response.status_code, 400)
    
    def test_place_calendar_get_type_error_fail(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        response = client.get('/places/1/calendar', **headers)
        
        self.assertEqual(response.json(),{"message":"TYPE_ERROR"})
        self.assertEqual(response.status_code, 400)
