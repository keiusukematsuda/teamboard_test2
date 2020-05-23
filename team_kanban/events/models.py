from django.db import models
from django.conf import settings


class Event(models.Model):
    TYPE_CHOICES = (
        (1, "練習"),
        (2, "試合"),
        (3, "飲み会"),
        (4, "その他イベント"),
    )

    name = models.CharField(
        verbose_name='イベント名',
        max_length=30
    )

    type = models.IntegerField(
        verbose_name='種類',
        choices=TYPE_CHOICES,
        default=1,
    )

    date_time = models.DateField(
        verbose_name='日時',
        blank=False,
        null=False,
    )

    time = models.TimeField(
        verbose_name='時刻',
        blank=True,
        null=True,
    )

    place = models.CharField(
        verbose_name='場所',
        max_length=100,
    )

    created_at = models.DateTimeField(
        verbose_name='登録日',
        auto_now_add=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='作成ユーザ',
        on_delete=models.SET_NULL,
        null=True,
    )

    num_join = models.IntegerField(
        verbose_name='人数(参加)',
        default=0
    )

    num_pend_join = models.IntegerField(
        verbose_name='人数(参加より保留)',
        default=0
    )

    num_pend_def = models.IntegerField(
        verbose_name='人数(不参加より保留)',
        default=0
    )

    num_cancel = models.IntegerField(
        verbose_name='人数(キャンセル)',
        default=0
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name='イベント',
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        verbose_name='内容',
        max_length=150,
    )
    commented_at = models.DateTimeField(
        verbose_name='投稿日',
        auto_now_add=True,
    )

    commented_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='投稿者',
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.content


class Attend(models.Model):
    STATE_CHOICE = (
        (1, "参加"),
        (2, "保留(参加より)"),
        (3, "保留(不参加より)"),
        (4, "キャンセル"),
    )

    attend_state = models.IntegerField(
        verbose_name='参加状況',
        choices=STATE_CHOICE,
        default=1,
    )

    event = models.ForeignKey(
        Event,
        verbose_name='イベント',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='参加ユーザ',
        on_delete=models.SET("削除されたユーザ"),
    )

    created_at = models.DateTimeField(
        verbose_name='更新日',
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return str(self.attend_state)