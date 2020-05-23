from django import forms
from .models import Event, Comment, Attend
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import bootstrap_datepicker_plus as datetimepicker

class CustomChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return u'%s' % obj.name


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'type', 'date_time', 'place', 'created_by')
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': '記入例：多摩川練習'}
            ),
            'type': forms.RadioSelect,
            'date_time': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY/MM/MM',
                }
            ),
            'time': datetimepicker.TimePickerInput(
                format='%H:%M',
                options={
                    'locale': 'ja',
                }
            ),
            'place': forms.TextInput(
                attrs={'placeholder': '記入例: 多摩川テニスコート'}
            )
        }


class CommentForm(forms.ModelForm):
    event = CustomChoiceField(queryset=Event.objects.all())

    class Meta:
        model = Comment
        fields = ('content', 'event', 'commented_by')
        widgets = {
            'content': forms.TextInput(),
        }


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
        )


class UserLoginForm(AuthenticationForm):
    pass


class AttendForm(forms.ModelForm):

    event = CustomChoiceField(queryset=Event.objects.all())

    class Meta:
        model = Attend
        fields = (
            'attend_state',
#            'event',
#            'user',
        )
