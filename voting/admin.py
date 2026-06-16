from django.contrib import admin
from .models import Voter,Position,Candidate,Vote

# Register your models here.
admin.site.register(Voter)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Vote)
