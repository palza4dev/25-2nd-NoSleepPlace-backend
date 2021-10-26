import requests

from django.http import JsonResponse

class KakaoAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.user_url     = 'https://kapi.kakao.com/v2/user/me'

    def get_kakao_user(self):
        headers  = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(self.user_url, headers=headers, timeout=3)

        if not response.status_code == 200:
            return JsonResponse({'message':"INVALID_KAKAO_TOKEN"}, status=401)

        return response.json()