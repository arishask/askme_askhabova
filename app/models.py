from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):

    def get_question_by_id(self, question_id):
        return self.get(pk=question_id)

    def new_questions(self):
        return self.order_by('-created_at')

    def best_questions(self):
        return self.annotate(likes_count=models.Count('likes')).order_by('-likes_count')

    def get_questions_by_tag_name(self, tag_name):
        return self.filter(tags__name=tag_name)


class AnswerManager(models.Manager):
    def get_answers_by_question_id(self, question_id):
        return self.filter(question_id=question_id).annotate(likes_count=models.Count('likes')).order_by('-is_accepted',
                                                                                                         '-likes_count')


class ProfileManager(models.Manager):
    def top_users(self, limit=10):
        return self.annotate(
            total_likes=models.Count('user__questions__likes', distinct=True) +
                        models.Count('user__answers__likes', distinct=True)).order_by('-total_likes')[:limit]


class TagManager(models.Manager):
    def popular_tags(self, n=5):
        return self.annotate(questions_count=models.Count('questions')).order_by('-questions_count')[:n]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    objects = TagManager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/questions/{self.id}/"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AnswerManager()

    class Meta:
        ordering = ['-created_at']


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'question')


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'answer')
