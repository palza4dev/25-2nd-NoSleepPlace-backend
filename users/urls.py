from django.urls import path

from users.views import KakaoSignUpView, UserProfileView

urlpatterns = [
    path('/account/kakao', KakaoSignUpView.as_view()),
    path('/profile', UserProfileView.as_view())
]