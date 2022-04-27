from django.urls import path

from core.views import *

urlpatterns = [
    path('home/', home_view),
    path('register/', register_view),
    path('login/', login_view),
    path('dashboard/', dashboard_view),
    path('logout/', logout_view),
    path('update/', update_user_view),
    path('delete/', delete_user_view),
    path('new/', new_view),
    path('notes/', notes_view),
    path('note/update/<int:note_id>', note_update_view),
    path('note/delete/<int:note_id>', note_delete_view),
]
