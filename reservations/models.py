from django.db import models
from django.utils import timezone
from core import models as core_models


class Reservation(core_models.TimeSatampedModel):
    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()

    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room}-{self.check_in}"

    def in_progress(self):
        now = timezone.localdate()
        print(now)
        # 왜 현재를 8/13일이 아니라 8월 12일을 가르키고 있는지 의문
        # timezone.now().date()로 읽게 되면 UTC 기준으로 값을 읽음
        # 단순히 UTC+9시간 기준으로 읽는 것이기 때문에 날짜 상으로는 하루전이 출력됨
        # 이를 위해서 localdate()를 통해 값을 얻어서 현재 날짜를 얻어옴

        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.localdate()
        return now > self.check_out

    is_finished.boolean = True

