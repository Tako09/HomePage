from django.db import models
from django.db.models.query import FlatValuesListIterable
from django.utils import timezone # manage date and time
from django.core.validators import FileExtensionValidator 
from django_summernote.fields import SummernoteTextField


# Create your models here.
CATEGORY = (('Python', 'Python'), ('News', 'ニュース'), ('Daily', '日常'))
'''class Post(models.Model): # add db
    # This db allow superuser to post a new article
    title = models.CharField('Title', max_length=200)
    text = models.TextField('Contents')
    date = models.DateTimeField('Date', default=timezone.now)
    category = models.CharField('Category', max_length=50, choices=CATEGORY)

    def __str__(self): 
        # define the return value if Post self is called
        return self.title'''

###############################################################################

class Category(models.Model):
    # Create Category
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    # create Tag
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    tiumestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    # Make a post
    category = models.ForeignKey(Category, on_delete=models.PROTECT) # one post has one category
    tags = models.ManyToManyField(Tag, blank=True) # one post has multiple tags
    title = models.CharField(max_length=255) # title
    content = models.TextField() # content
    image = models.ImageField(upload_to='post_images/', null=True, blank=True, verbose_name='添付画像')
    description = models.TextField(blank=True) # description 
    created_at = models.DateTimeField(auto_now_add=True) # date of creation
    updated_at = models.DateTimeField(auto_now_add=True) # date of update
    published_at = models.DateTimeField(blank=True, null=True) # date of publication
    is_public = models.BooleanField(default=False) # not to publish a draft

    class Meta:
        ordering = ['-created_at'] # make a list that has the newest post at the top
        verbose_name = 'ブログ'
        verbose_name_plural = 'ブログ'
    
    def save(self, *args, **kwargs):
        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

#########################################test###############################################
""" from django.db import models


class Blog(models.Model):
    title = models.CharField('タイトル', max_length=50)
    text = models.TextField('テキスト')
    created_at = models.DateField('作成日', auto_now_add=True)
    updated_at = models.DateField('更新日', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ブログ'
        verbose_name_plural = 'ブログ' """
#########################################test###############################################

class ContentImage(models.Model):
    # ブログ記事に画像を挿入する
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='post_content_images/')
    # admin.pyを開いて、このモデルを編集できるようにしましょう
    # ただし今回は設定方法が少し異なります。admin の「インライン」という機能を使って、親モデルのページから編集できるようにします。

class Comment(models.Model):
    # コメント機能の実装
    #　入力で保存されるデータを作成
    # Postと結びつく
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
    
    def approve(self):
        self.approve = True
        self.save()

    def __str__(self):
        return self.text

class Reply(models.Model):
        # allow to reply a message
        # Commetnと結びつく
        comment = models.ForeignKey(
            Comment, on_delete=models.CASCADE, related_name='replies'
        )
        author = models.CharField(max_length=50)
        text = models.TextField()
        timestamp = models.DateTimeField(auto_now_add=True)
        approved = models.BooleanField(default=False)

        def approve(self):
            self.approve = True
            self.save()
        
        def __str__(self):
            return self.text
'''
related_nameは、リレーションの逆参照に使用する名前を指定します。リレーションを張られたモデルが、この名前を使ってリレーションを張ったモデルを参照（いわゆる逆参照）できるようになります。テンプレートで実際に使ってみるとよくわかるので、今はピンと来ていなくても大丈夫です。
投稿されたコメントや返信は、サイト管理者が承認してから公開するようにしたいので、approved属性とapprove()メソッドを定義しておきます。
コメントは新しいものを上に表示したいので、タイムスタンプの降順に並べ替えます。
'''

