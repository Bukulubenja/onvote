from django.contrib.auth.models import User
from django.db import models

import random
import string

password = ''.join(
    random.choices(
        string.ascii_letters + string.digits,
        k=8
    )
)


# create user 

# user = User.objects.create_user(
#     username=student_id,
#     password=password
# )

class Class_name(models.Model):
    name = models.CharField(max_length=20)

#create voters
class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    student_id = models.CharField(max_length=20, unique=True)

    class_name = models.ForeignKey(Class_name, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_id
    
# positions

class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class Candidate(models.Model):

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    class_name = models.ForeignKey(Class_name, on_delete=models.CASCADE)

    # photo = models.ImageField(
    #     upload_to='candidates/'
    # )

    slogan = models.TextField(blank=True)

    class Meta:
        unique_together = ('position', 'name')

    def __str__(self):
        return self.name
    

class Vote(models.Model):

    voter = models.ForeignKey(
        Voter,
        on_delete=models.CASCADE
    )

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    voted_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        unique_together = ('voter', 'position')


