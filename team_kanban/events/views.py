from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from .forms import EventForm
from .models import Event, Comment, Attend

class EventListView(View):
    def get(self, request, *args, **kwargs):
        all_events = Event.objects.order_by('-created_at')
        paginate_by = 10
        paginator = Paginator(all_events, paginate_by)
        p = request.GET.get('p')
        events = paginator.get_page(p)
        return render(request, 'events/event_list.html', {'events': events})


class EventDetailView(View):
    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['event_id'])
        all_comments = Comment.objects.all().filter(event=event)
        paginate_by = 10
        paginator = Paginator(all_comments, paginate_by)
        p = request.GET.get('p')
        comments = paginator.get_page(p)
        # eventに紐づくattendを取得する(ユーザ一覧表示用)
        try:
            attends = Attend.objects.all().filter(event=event)
        except Attend.DoesNotExist:
            attends = None

        # eventとユーザに紐づくattendを取得する
        try:
            attend = Attend.objects.get(event=event, user=self.request.user)
        # まだ該当するAttendインスタンスが作成されていない場合は、attendにNoneを入れて返す
        except Attend.DoesNotExist:
            attend = None
        return render(request, 'events/event_detail.html', {'event': event, 'attends': attends, 'attend': attend, 'comments': comments})


class EventRegisterView(View):
    def get(self, request, *args, **kwargs):
        print(request.user)
        return render(request, 'events/event_register.html', {'form': EventForm(initial={'created_by': self.request.user})})

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        post = form.save(commit=False)
        post.save()

        return redirect('proto1:event_list')