from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (IndexView, PostDetailView, CategoryListView, TageListView, 
                    CategoryPostView, TagPostView, SearchPostView, CommentFormView,
                    comment_approve, comment_remove, ReplyFormView, reply_approve,
                    reply_remove
)


app_name = 'blog'

# path()には、ルーティング、ビュー、（追加のキーワード）、名前を引数として渡します。
# 先ほど少し触れましたが、URL パターンには名前をつけることができます。逆引き（ビューから URL に変換すること）を行う際に名前があると便利です。
urlpatterns = [
    # path('admin/', admin.site.urls), # add a code
    path('', IndexView.as_view(), name='index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('tags/', TageListView.as_view(), name='tag_list'),
    path('category/<str:category_slug>/', CategoryPostView.as_view(), name='category_post'),
    path('tag/<str:tag_slug>/', TagPostView.as_view(), name='tag_post'),
    path('search/', SearchPostView.as_view(), name='search_post'),
    path('comment/<int:pk>/', CommentFormView.as_view(), name='comment_form'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'), # 関数ビューにはas_view()は不要
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),# 関数ビューにはas_view()は不要
    path('reply/<int:pk>/', ReplyFormView.as_view(), name='reply_form'),
    path('reply/<int:pk>/approve/', reply_approve, name='reply_approve'), # 関数ビューにはas_view()は不要
    path('reply/<int:pk>/remove/', reply_remove, name='reply_remove'), # 関数ビューにはas_view()は不要
    # path('post_list/', views.PostListView.as_view(), name='post_list'), # add code
    # path('post_create/', views.PostCreateView.as_view(), name='post_create'), # add code'''
    #path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), # 追加　(例) /blog/detail/1　※特定のレコードに対して処理を行うので pk で識別
    #path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'), # 追加　(例) /blog/update/1　※同上
    #path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'), # 追加　(例) /blog/delete/1　※同上
]