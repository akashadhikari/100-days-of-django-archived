from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    profile_pic = models.ImageField(default='user-icon.png')

    def get_full_name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        full_name = self.user.first_name + " " + self.user.last_name
        return full_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class FollowUser(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    is_following = models.BooleanField(default=False)
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('following', 'followed_by',)

    def __str__(self):
        if self.is_following:
            return self.following.get_full_name() + " is followed by " + self.followed_by.get_full_name()
