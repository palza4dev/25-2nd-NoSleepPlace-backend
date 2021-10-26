from django.urls import path

from users.views import KakaoSignUpView

urlpatterns = [
    path('/account/kakao', KakaoSignUpView.as_view()),
]