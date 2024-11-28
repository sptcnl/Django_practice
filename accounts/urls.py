from django.urls import path
from accounts.views import get_csrftoken, signup, login

urlpatterns = [
    path('get_csrftoken/', get_csrftoken),
    path('signup/', signup),
    path('<how>/login/', login), # 의도: <how>에 token 넣으면 token 방식으로 로그인됨

]