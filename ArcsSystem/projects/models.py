from django.db import models

class Project(models.Model):
    '''Required alphabetical'''
    aim = models.CharField(max_length=200, default='Empty')
    description = models.CharField(max_length=5000, default='Empty')
    name = models.CharField(max_length=200, default='Empty')
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    status = models.CharField(max_length=30, default='Empty')
    image_dir = 'http://localhost:8000/media/images/wild-otter-mom-and-pup_d-large.max-165x165.jpg'
    target_audience = models.CharField(max_length=5000, default='Empty')
    contact_name = models.CharField(max_length=200, default='Empty')
    contact_role = models.CharField(max_length=200, default='Empty')
    contact_affiliation = models.CharField(max_length=200, default='Empty')
    contact_email = models.CharField(max_length=200, default='Empty')
    contact_phone = models.CharField(max_length=200, default='Empty')

    # keywords


    def __str__(self):
        return self.name
