from django.urls import path
from accounts.views import (
                        get_csrftoken, 
                        signup, 
                        login, 
                        logout, 
                        change_password,
                        edit_profile,
                    )

urlpatterns = [
    path('get_csrftoken/', get_csrftoken),
    path('signup/', signup),
    path('<how>/login/', login), # 의도: <how>에 token 넣으면 token 방식으로 로그인됨
    path('<how>/logout/', logout), # 의도: <how>에 session 넣으면 session 방식으로 로그아웃됨
    path('change_password/', change_password),
    path('edit_profile/', edit_profile),
]