from django.http import HttpResponse
from django.views.generic import View

from topics.models import Question

import simplejson as json


class QuestionFollowView(View):
    def post(self, request):
        question = Question.objects.get(id=request.POST['question_id'])

        if request.POST['is_follow'] == '0':
            is_follow = self.set_follow(request.user, question)

        if request.POST['is_follow'] == '1':
            is_follow = self.set_unfollow(request.user, question)

        response = {
            'success': 0,
            'data': { 'is_follow': is_follow }
        }

        return HttpResponse(json.dumps(response),
                            content_type='application/json') 

    def set_follow(self, user, question):
        try:
            question.followers.add(user)
            return 1
        except DatabaseError:
            return 0

    def set_unfollow(self, user, question):
        try:
            question.followers.remove(user)
            return 0
        except DatabaseError:
            return 1


class QuestionDownvoteView(View):
    def post(self, request):
        question = Question.objects.get(id=request.POST['question_id'])

        if request.POST['is_downvote'] == '0':
            is_downvote = self.downvote(request.user, question)

        if request.POST['is_downvote'] == '1':
            is_downvote = self.undo_downvote(request.user, question)

        response = {
            'success': 0,
            'data': { 'is_downvote': is_downvote }
        }

        return HttpResponse(json.dumps(response),
                            content_type='application/json') 

    def downvote(self, user, question):
        try:
            question.downvoters.add(user)
            return 1
        except DatabaseError:
            return 0

    def undo_downvote(self, user, question):
        try:
            question.downvoters.remove(user)
            return 0
        except DatabaseError:
            return 1
