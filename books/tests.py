import jwt

from django.test           import TestCase, Client

from users.models          import User
from places.models         import Menu, Category, City, Host, Place, Image
from books.models          import Book, BookStatus
from nosleepplace.settings import SECRET_KEY

class BookPlaceTest(TestCase):
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
            id            = 1,
            name          = '빌리',
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
        
        Image.objects.create(
            url      = "https://images.unsplash.com/photo-1536437075651-01d675529a6b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2340&q=80",
            place_id = 1
        )
        
        user = User.objects.create(
            id            = 1,
            kakao_id      = '1960067483',
            nickname      = '성해호',
            profile_image = 'http://k.kakaocdn.net/dn/cnv4DE/btq7DsQ0kM6/mTFyVTEeGMzEbakRv72iKK/img_110x110.jpg',
            email         = 'soh308@nate.com',
            age_range     = '30~39'
        )
        
        self.access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
        
        BookStatus.objects.bulk_create([
            BookStatus(
                id     = 1,
                status = "PENDING"
            ),
            BookStatus(
                id     = 2,
                status = "CONFIRMED"
            )
        ])

        Book.objects.bulk_create([
            Book(
                id             = 1,
                user_id        = 1,
                place_id       = 1,
                date           = "2021-12-11",
                start_time     = "2021-12-11T02:00:00",
                end_time       = "2021-12-11T04:00:00",
                head_count     = 3,
                total_price    = 132000,
                content_type   = "기존 예약 샘플",
                content_info   = "기존 예약 샘플",
                status_code_id = 1
            ),
            Book(
                id             = 2,
                user_id        = 1,
                place_id       = 1,
                date           = "2021-12-10",
                start_time     = "2021-12-10T02:00:00",
                end_time       = "2021-12-10T04:00:00",
                head_count     = 5,
                total_price    = 132000,
                content_type   = "확정 예약 샘플",
                content_info   = "확정 예약 샘플",
                status_code_id = 2
            )
        ])
        
    def tearDown(self):
        Place.objects.all().delete()
        User.objects.all().delete()
        BookStatus.objects.all().delete()
    
    def test_book_place_post_success(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        data     = {
            "place_id"     : 1,
            "start_time"   : "2021-10-30T03:00:00",
            "end_time"     : "2021-10-30T05:00:00",
            "head_count"   : 4,
            "total_price"  : 132000,
            "content_type" : "sample",
            "content_info" : "sample"
        }
        response = client.post('/books', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message':'SUCCESS'})
    
    def test_book_place_post_invalid_place_fail(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        data     = {
            "place_id"     : 99,
            "start_time"   : "2021-10-30T03:00:00",
            "end_time"     : "2021-10-30T05:00:00",
            "head_count"   : 4,
            "total_price"  : 132000,
            "content_type" : "sample",
            "content_info" : "sample"
        }
        response = client.post('/books', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'INVALID_PLACE'})

    def test_book_place_post_invalid_book_time_fail(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        data     = {
            "place_id"     : 1,
            "start_time"   : "2021-12-30T03:00:00",
            "end_time"     : "2021-10-30T05:00:00",
            "head_count"   : 4,
            "total_price"  : 132000,
            "content_type" : "sample",
            "content_info" : "sample"
        }
        response = client.post('/books', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_BOOK_TIME'})

    def test_book_place_post_already_booked_time_fail(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        data     = {
            "place_id"     : 1,
            "start_time"   : "2021-12-11T02:00:00",
            "end_time"     : "2021-12-11T04:00:00",
            "head_count"   : 4,
            "total_price"  : 132000,
            "content_type" : "sample",
            "content_info" : "sample"
        }
        response = client.post('/books', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'ALREADY_BOOKED_TIME'})

    def test_book_place_post_key_error_fail(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        data     = {
            "start_time"   : "2021-10-30T02:00:00",
            "end_time"     : "2021-10-30T04:00:00",
            "head_count"   : 4,
            "total_price"  : 132000,
            "content_type" : "sample",
            "content_info" : "sample"
        }
        response = client.post('/books', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})
    
    def test_book_place_get_success(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        response = client.get('/books?status=PENDING&status=CONFIRMED', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'result': [
                {
                    "book_id"      : 2,
                    "name"         : "마루비 성산 - 80년대 주택을 개조한 빈티지 스튜디오 1F ",
                    "image"        : "https://images.unsplash.com/photo-1536437075651-01d675529a6b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2340&q=80",
                    "content_type" : "확정 예약 샘플",
                    "content_info" : "확정 예약 샘플",
                    "head_count"   : 5,
                    "start_time"   : "2021년 12월 10일 02:00",
                    "end_time"     : "04:00",
                    "usage_time"   : 2,
                    "total_price"  : 132000,
                    "status"       : "CONFIRMED"
                },
                {
                    "book_id"      : 1,
                    "name"         : "마루비 성산 - 80년대 주택을 개조한 빈티지 스튜디오 1F ",
                    "image"        : "https://images.unsplash.com/photo-1536437075651-01d675529a6b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2340&q=80",
                    "content_type" : "기존 예약 샘플",
                    "content_info" : "기존 예약 샘플",
                    "head_count"   : 3,
                    "start_time"   : "2021년 12월 11일 02:00",
                    "end_time"     : "04:00",
                    "usage_time"   : 2,
                    "total_price"  : 132000,
                    "status"       : "PENDING"
                }
            ]
        })

    def test_book_place_get_type_error_fail(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.access_token}
        response = client.get('/books?stasds', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'TYPE_ERROR'})