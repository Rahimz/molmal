from django.db import models


class DeliveryContainer(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    admin_check = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    # TODO: add the quantity of order accepted in this container
    order_in_container = models.PositiveIntegerField(default=0)
    # TODO: make a logic to control the number of order in a container



    def __str__(self):
        return "Day {} Hour {} to {}".format(str(self.start.day), str(self.start.hour), str(self.end.hour) )
