from django.core import serializers
from django.db.models import Count
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.generic import UpdateView, ListView, DeleteView
from django.utils.decorators import method_decorator

from boards.models import Board, Post, Topic, History
from .forms import NewTopicForm, PostForm, BoardForm
from static.utils import check_recaptcha, get_last_five_history
from rest_framework import permissions
from .serializers import BoardSerializer, TopicSerializer, PostSerializer, HistorySerializer
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse
from RoockLabTestBlog.tasks import send_email


# ---------------------------------------------------------------
# Block of ajax boards views


def history(request):
    data = {}
    if request.method == 'GET':
        action_json = History.objects.order_by('-action_at')[:5]
        data['html_actions'] = render_to_string('actions.html',
                                                {'actions': action_json, 'user': request.user})
        return JsonResponse(data)
    else:
        pass


def save_board_form(request, form, template_name):
    data = {}
    if request.method == "POST":
        if form.is_valid():
            print('im in save board form')
            print(request.user)
            form.save()
            data['form_is_valid'] = True

            action_json = History.objects.order_by('-action_at')[:5]

            data['html_actions'] = render_to_string('actions.html',
                                                    {'actions': action_json, 'user': request.user})

            boards = Board.objects.all()
            data['html_board_list'] = render_to_string('partial_board_list.html',
                                                       {'boards': boards, 'user': request.user})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def board_list(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards, 'user': request.user})


def board_create(request):
    if request.method == 'POST':
        print('im in board_cerate ')
        print(request.user)
        form = BoardForm(request.POST)
        send_email.delay(request.user.email, 'Django Board', 'New board has been created',
                   'volodindmitriy121@gmail.com')
    else:
        form = BoardForm()
    return save_board_form(request, form, 'partial_board_create.html')


def board_update(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
    else:
        form = BoardForm(instance=board)
    return save_board_form(request, form, 'partial_board_update.html')


def board_delete(request, pk):
    board = get_object_or_404(Board, pk=pk)
    data = {}
    if request.method == 'POST':
        board.delete()
        data['form_is_valid'] = True
        boards = Board.objects.all()
        action_json = History.objects.order_by('-action_at')[:5]
        data['html_actions'] = render_to_string('actions.html',
                                                {'actions': action_json, 'user': request.user})
        data['html_board_list'] = render_to_string('partial_board_list.html', {'boards': boards, 'user': request.user})
    else:
        context = {'board': board}
        data['html_form'] = render_to_string('partial_board_delete.html', context, request=request)

    return JsonResponse(data)


def delete_post(request, pk, topic_pk, post_pk):
    data = {}
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'DELETE':

        data['post_id'] = post.pk
        post.delete()
        data['msg'] = 'Post was deleted.'

        return JsonResponse(data)
    else:
        return JsonResponse({'result': 'nothing happened'})


# --------------------------------------------------------------


@login_required
def reply_post(request, pk, topic_pk):
    """
    boards/pk/topics/pk/reply
    """
    data = {}
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)

        post = form.save(commit=False)
        post.topic = topic
        post.created_by = request.user
        post.save()

        topic.last_updated = timezone.now()
        topic.save()

        data['template'] = render_to_string('rep_post.html', {'post': post})
        data['message'] = request.POST.get('the_post')
        data['topic'] = str(post.topic)
        data['created_by'] = post.created_by.username
        data['created_at'] = post.created_at

        return JsonResponse(data)
    else:

        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


# --------------------------------------------------------------


class BoardListView(ListView):
    """
    /
    """
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


class TopicListView(ListView):
    """
    boards/pk/
    """
    model = Topic
    paginate_by = 5
    context_object_name = 'topics'
    template_name = 'topics.html'

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


@login_required
@check_recaptcha
def new_topic(request, pk):
    """
    /boards/pk/new
    """
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)

        if form.is_valid() and request.recaptcha_is_valid:
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


class PostListView(ListView):
    """
    boards/pk/topics/pk
    """
    model = Post
    paginate_by = 1
    context_object_name = 'posts'
    template_name = 'topic_posts.html'

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('-created_at')
        return queryset


@login_required
def reply_topic(request, pk, topic_pk):
    """
    boards/pk/topics/pk/reply
    """
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            return redirect(topic_url)
    else:
        form = PostForm
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    """
    boards/pk/topics/pk/posts/pk/edit
    """
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


class PostDeleteView(DeleteView):

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('-created_at')
        return queryset


# ---------API--------------API-------API--------API--------API---------API-------------


class BoardViewSet(viewsets.ModelViewSet):
    """
    API board
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAdminUser,)


class HistoryViewSet(viewsets.ModelViewSet):
    """
    API board history
    """
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (permissions.IsAdminUser,)


class TopicViewSet(viewsets.ModelViewSet):
    """
    API topics
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(board=self.kwargs.get('pk'))


class PostViewSet(viewsets.ModelViewSet):
    """
    API posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(topic__board=self.kwargs.get('pk'), topic=self.kwargs.get('topic_pk'))
