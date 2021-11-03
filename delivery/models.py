from django.db import models
from django.utils.translation import gettext_lazy as _



class DeliveryContainer(models.Model):
    TIME_CHOICES = (('9:00-12:00', '9-12'),
                    ('13:00-16:00', '13-16'))
    start = models.DateTimeField()
    end = models.DateTimeField()
    admin_check = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    # TODO: Farsi date should be automatic
    fa_date = models.CharField(max_length=250, blank=True, null=True)
    fa_time = models.CharField(max_length=200, choices=TIME_CHOICES, default='morning')
    # TODO: add the quantity of order accepted in this container
    order_in_container = models.PositiveIntegerField(default=0)
    # TODO: make a logic to control the number of order in a container



    def __str__(self):
        # return "{}{}: Hour {} to {}".format(str(self.start.day), self.start.strftime("%B"), str(self.start.hour), str(self.end.hour) )
        return "{} {} {}".format(self.fa_date, _('Hour'), self.fa_time)
