import json, jwt
from unittest.mock         import MagicMock, patch

from django.test           import TestCase, Client

from users.models          import User
from nosleepplace.settings import SECRET_KEY

class KakaoSignUpTest(TestCase):
    @patch("users.kakao.requests")
    def test_kakao_signup_new_user_success(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            def __init__(self, status_code):
                self.status_code = status_code
    
            def json(self):
                return {
                    "id" : "1204",
                    "kakao_account" : {
                        "profile" : {
                            "nickname" : "승준",
                            "thumbnail_image_url" : "http://k.kakaocdn.net/img_110x110.jpg"
                        },
                        "email_needs_agreement" : False,
                        "email" : "dddsfa@sample.com",
                        "age_range_needs_agreement" : False,
                        "age_range" : "20-30"
                    }
                }

        mocked_requests.post = MagicMock(return_value = MockedResponse(200))
        headers              = {"Authorization" : "fake_kakao_token"}
        response             = client.post("/users/account/kakao", **headers)
        self.assertEqual(response.status_code, 200)

        access_token = response.json()['access_token']
        payload      = jwt.decode(access_token, SECRET_KEY, algorithms="HS256")
        kakao_id     = User.objects.get(id=payload['id']).kakao_id
        
        self.assertEqual(kakao_id, "1204")

    @patch("users.kakao.requests")
    def test_kakao_signup_fail(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            def __init__(self,status_code):
                self.status_code = status_code
            
            def json(self):
                return {
                    "status_code" : -401,
                    "message" : "INVALID_KAKAO_TOKEN"
                }
                
        mocked_requests.post = MagicMock(return_value = MockedResponse(200))
        headers              = {"Authorization" : "fake_kakao_token"}
        response             = client.post("/users/account/kakao", **headers)
        
        self.assertEqual(response.status_code, 400)