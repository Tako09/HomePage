from django.db.models import Count, Q, query
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


# from .forms import PostCreateForm
# from .models import Post
from .models import Post, Category, Tag, Comment, Reply
from .forms import CommentForm, ReplyForm
# Create your views here.
'''
ビューとは、リクエストを受け取りレスポンスを返す、呼び出し可能なオブジェクトです。
このレスポンスは、Web ページの HTML コンテンツ、リダイレクトや 404 エラー、または XML ドキュメントやイメージ、その他何にでもなり得ます。
要は、要求されたページの情報をテンプレートに渡したり、例外を発生させたりすることができるよーということです。
'''

class PostDetailView(DetailView):
    # show a post
    model = Post # model = Postは、queryset = Post.objects.all()を簡略化したもの

    def get_object(self, queryset=None): 
        # 記事を取得するメソッド
        #　公開andログインしてない場合はアクセスできない
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj

class IndexView(ListView):
    # 記事一覧を見せる
    model = Post
    # 使うhtmlファイルを明示
    template_name = 'blog/index.html'
    paginate_by = 2

class CategoryListView(ListView):
    # show a category
    # categoryに紐ずくpostを集計(公開のみ)
    paginate_by = 2
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True))
    )

class TageListView(ListView):
    # show a tag
    # tagに紐づくpostを集計(公開のみ)
    paginate_by = 2
    queryset = Tag.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True))
    )

# 基本的には投稿一覧のビューと同じですが、
# QuerySet をフィルタリングして取得します。category_slug、tag_slugは、URLconf から渡されるキーワード引数です。
class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category_post.html'
    paginate_by = 2

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class TagPostView(ListView):
    model = Post
    template_name = 'blog/tag_post.html'
    paginate_by = 2

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchPostView(ListView):
    # 検索結果を表示するビューの作成
    model = Post
    template_name = 'blog/search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct() # distinct - 検索結果の重複を避けるため。
            return qs
        qs = super().get_queryset
        return qs
        # Qオブジェクトの使い方は以前にやった通りですが、&や|演算子で結合することもできます。これで「タイトルに値が含まれる場合、
        # もしくは本文中に値が含まれる場合、もしくは…」といった複雑な検索が可能になります。

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

# コメントを管理するためのビューを作成
class CommentFormView(CreateView):
    # コメントの投稿、セーブを行うビューを作成
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()
        return redirect('blog:post_detail', pk=post_pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)
        return context

# 管理者がコメントを管理できるようにする
@login_required
def comment_approve(request, pk):
    # コメントを承認する
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    # コメントを削除する
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)

# 返信を管理するためのビューを作成
class ReplyFormView(CreateView):
    # 返信の投稿、セーブを行うビューを作成
    model = Reply
    form_class = ReplyForm # カスタマイズしたフォームを使用

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        reply.comment = get_object_or_404(Comment, pk=comment_pk)
        reply.save()
        return redirect('blog:post_detail', pk=reply.comment.post.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context

# 管理者がコメントを管理できるようにする
@login_required
def reply_approve(request, pk):
    # 返信を承認する
    reply = get_object_or_404(Reply, pk=pk)
    reply.approve()
    return redirect('blog:post_detail', pk=reply.comment.post.pk)

@login_required
def reply_remove(request, pk):
    # 返信を削除する
    reply = get_object_or_404(Reply, pk=pk)
    reply.delete()
    return redirect('blog:post_detail', pk=reply.comment.post.pk)



