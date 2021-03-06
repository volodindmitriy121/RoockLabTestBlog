from django.urls import include

from boards import views
from django.contrib import admin
from django.conf.urls import url
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

from boards.views import TopicViewSet, BoardViewSet, PostViewSet, HistoryViewSet

post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

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

history_list = HistoryViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
history_detail = HistoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [

    #  ------------------CRUD board---------------------------
    url(r'^$', views.board_list, name='home'),
    url(r'^boards/create/$', views.board_create, name='board_create'),
    url(r'^boards/(?P<pk>\d+)/update/$', views.board_update, name='board_update'),
    url(r'^boards/(?P<pk>\d+)/delete/$', views.board_delete, name='board_delete'),

    #  ------------------CRUD post---------------------------
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_post, name='reply_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),
    url(r'^posts/(?P<post_pk>\d+)/delete/$',
        views.delete_post, name='post_delete'),

    #  ------------------Sign | Log in---------------------------
    url(r'^signup/staff/$', accounts_views.staff_signup, name='staff-signup'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    #  ------------------Settings---------------------------
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

    #  ------------------Create | Read topic---------------------------
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),

    #  ------------------Get history---------------------------
    url(r'^history/$', views.history, name='history'),

    #  ------------------Admin---------------------------
    url('admin/', admin.site.urls),

    #  ------------------Social auth---------------------------
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    #  ------------------API---------------------------
    url(r'^api/$', board_list, name='board-list'),
    url(r'^api/boards/(?P<pk>\d+)/$', board_detail, name='board-detail'),
    url(r'^api/boards/(?P<pk>\d+)/topics/$', topic_list, name='topic-list'),
    url(r'^api/boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', topic_detail, name='topic-detail'),
    url(r'^api/boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/$', post_list, name='post-list'),
    url(r'^api/boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/$', post_detail, name='post-detail'),
    url(r'^api/history/$', history_list, name='history-list'),
    url(r'^api/history/(?P<pk>\d+)/$', history_detail, name='history-detail'),
]


