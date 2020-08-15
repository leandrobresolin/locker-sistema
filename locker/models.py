from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    uid = models.IntegerField()
    enabled = models.BooleanField(default=False)
    autorized = models.BooleanField(default=False)
    date_time = models.DateTimeField()

    def __str__(self):
        return 'UID: {0} | Name: {1} | Autorizado: {2} | Habilitado: {3}'.format(self.uid, self.name, self.autorized, self.enabled)

    class Meta:
        ordering = ['-date_time']
        

class Device(models.Model):
    device_id = models.CharField(max_length=40)
    door_status = models.BooleanField(default=False)
    uid = models.IntegerField()
    date_time = models.DateTimeField()

    def __str__(self):
        return '{0} | Device ID: {1} | Porta: {2}'.format(self.date_time, self.device_id, self.door_status)

    
    class Meta:
        ordering = ['-date_time']


    # class Meta:
    #     get_latest_by = 'created'
    #     ordering = ['-created']