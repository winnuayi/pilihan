from __future__ import unicode_literals

from django.core.validators import validate_email
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(_('username'), max_length=30, unique=True)
    fullname = models.CharField(_('full name'), max_length=100,
                                 null=True, blank=True)
    email = models.EmailField(_('email address'), max_length=254,
                              unique=True, validators=[validate_email])
    image = models.ImageField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['password']

    objects = UserManager()

    def get_short_name(self):
        return self.fullname


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    creator = models.ForeignKey(CustomUser)
    followers = models.ManyToManyField(CustomUser, related_name='question_followers')
    downvoters = models.ManyToManyField(CustomUser, related_name='question_downvoters')
    category = models.ForeignKey(Category, null=True, blank=True)
    slug = models.SlugField(max_length=120)
    question = models.CharField(max_length=100)
    view = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(_('created_at'),
                                      default=timezone.now)

    def __unicode__(self):
        return self.question


class QuestionComment(models.Model):
    pass


class Answer(models.Model):
    question = models.ForeignKey(Question)
    creator = models.ForeignKey(CustomUser)
    downvoters = models.ManyToManyField(CustomUser, related_name='answer_downvoters')
    upvoters = models.ManyToManyField(CustomUser, related_name='answer_upvoters')
    answer = models.TextField(null=True, blank=True)
    view = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(_('created_at'),
                                      default=timezone.now)

    def __unicode__(self):
        return self.choice.name + ' - ' + self.title


class AnswerComment(models.Model):
    pass


# class Tag(models.Model):
#     question = models.ManyToManyField(Question)
#     name = models.CharField(max_length=30)


class Choice(models.Model):
    question = models.ForeignKey(Question)
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    like = models.IntegerField(null=True, blank=True, default=0)
    dislike = models.IntegerField(null=True, blank=True, default=0)

    def __unicode__(self):
        return self.name


# class Procon(models.Model):
#     choice = models.ForeignKey(Choice)
#     title = models.CharField(max_length=100)
#     type = models.BooleanField()
#     answer = models.TextField(null=True, blank=True)
#     like = models.IntegerField(null=True, blank=True, default=0)
#     dislike = models.IntegerField(null=True, blank=True, default=0)
#
#     def __unicode__(self):
#         return self.choice.name + ' - ' + self.title
