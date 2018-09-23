from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Poll, Choice
from .serializers import *

# Create your views here.
def polls_list(request):
    MAX_OBJECTS = 20
    polls = Poll.objects.all()[:20]
    data = {'results': list(polls.values('question', 'created_by__username', 'pub_date'))}
    return JsonResponse(data)

def polls_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    data = {'results': {
        'question': poll.question,
        'created_by': poll.created_by.username,
        'pub_date': poll.pub_date
    }}
    return JsonResponse(data)

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll")
        return super().destory(request, *args, **kwargs)
