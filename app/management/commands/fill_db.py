from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from faker import Faker
from django.db import IntegrityError
import random


class Command(BaseCommand):
    help = "Fill the database with test data"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio of data population')

    def handle(self, *args, **options):
        fake = Faker()
        ratio = options['ratio']
        users = []
        for i in range(ratio):
            while True:
                username = fake.user_name()
                try:
                    user = User.objects.create_user(username=username)
                    users.append(user)
                    Profile.objects.create(user=user, avatar=None)
                    break
                except IntegrityError:
                    continue

        tags = []
        for _ in range(ratio):
            tag_name = fake.unique.word()
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        questions = []
        for i in range(ratio * 10):
            question = Question.objects.create(
                title=fake.sentence(),
                text=fake.text(),
                author=random.choice(users)
            )
            question.tags.add(*random.sample(tags, random.randint(1, 5)))
            questions.append(question)

        answers = []
        for i in range(ratio * 100):
            answer = Answer.objects.create(
                question=random.choice(questions),
                author=random.choice(users),
                text=fake.text(),
                is_accepted=random.choice([True, False])
            )
            answers.append(answer)

        question_likes = []
        for i in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(questions)
            if not QuestionLike.objects.filter(user=user, question=question).exists():
                question_like = QuestionLike.objects.create(user=user, question=question)
                question_likes.append(question_like)

        answer_likes = []
        for i in range(ratio * 200):
            user = random.choice(users)
            answer = random.choice(answers)
            if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                answer_like = AnswerLike.objects.create(user=user, answer=answer)
                answer_likes.append(answer_like)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with a ratio of {ratio}'))
