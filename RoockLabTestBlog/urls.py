from django.urls import include

from boards import views
from django.contrib import admin
from django.conf.urls import url
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

from boards.views import TopicViewSet, BoardViewSet

topic_list = TopicViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
topic_detail = TopicViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

board_list = BoardViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
board_detail = BoardViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    # url(r'^$', views.BoardListView.as_view(), name='home'),
    url(r'^$', views.board_list, name='home'),
    url(r'^boards/create/$', views.board_create, name='board_create'),
    url(r'^boards/(?P<pk>\d+)/update/$', views.board_update, name='board_update'),
    url(r'^boards/(?P<pk>\d+)/delete/$', views.board_delete, name='board_delete'),

    url(r'^oauth/', include('social_django.urls', namespace='social')),


    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),

    # url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_post, name='reply_topic'),

    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),

    url(r'^reset/$', auth_views.PasswordResetView.as_view(template_name='password_reset.html',
                                                          email_template_name='password_reset_email.html',
                                                          subject_template_name='password_reset_subject.txt'),
        name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    url(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),


    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/delete/$',
        views.delete_post, name='post_delete'),

    url('admin/', admin.site.urls),


    #  ------------------API---------------------------
    url(r'^api/$', board_list, name='board-list'),
    url(r'^api/boards/(?P<pk>\d+)/$', board_detail, name='board-detail'),
    url(r'^api/boards/(?P<pk>\d+)/topics/$', topic_list, name='topic-list'),
    url(r'^api/boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', topic_detail, name='topic-detail'),
]


