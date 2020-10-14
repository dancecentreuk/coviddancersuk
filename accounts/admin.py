from django.contrib import admin
from .models import User, Candidate, Employer, CandidateImage

admin.site.register(User)
admin.site.register(Candidate)
admin.site.register(Employer)
admin.site.register(CandidateImage)


