import json, requests, jwt

from django.http           import JsonResponse
from django.views          import View

from nosleepplace.settings import SECRET_KEY
from users.models          import User
from users.kakao           import KakaoAPI

class KakaoSignUpView(View):
    def post(self, request):
        try:
            kakao_token   = request.headers.get('Authorization')
            kakao_user    = KakaoAPI(kakao_token).get_kakao_user()
            kakao_account = kakao_user['kakao_account']

            nickname      = kakao_account['profile']['nickname'],
            profile_image = kakao_account['profile']['thumbnail_image_url']

            user, created = User.objects.get_or_create(
                kakao_id = kakao_user['id'],
                defaults = {
                    'nickname'     : nickname,
                    'profile_image': profile_image,
                    'email'        : kakao_account.get('email', ''),
                    'age_range'    : kakao_account.get('age_range', '')
                }
            )

            access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'access_token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':"KEY_ERROR"}, status=400)
        except ValueError:
             return JsonResponse({'message':"VALUE_ERROR"}, status=400)