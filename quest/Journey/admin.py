from django.contrib import admin
from .models import Challenge, Goal, UserProfile, Reward,Badge,Leaderboard

admin.site.register(Challenge)
admin.site.register(Goal)
admin.site.register(UserProfile)
admin.site.register(Reward)
admin.site.register(Badge)
admin.site.register(Leaderboard)

# Register your models here.
