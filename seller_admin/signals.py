from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Verification_code
from users.models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def save_seller_account_verification_code(sender, instance, created, **kwargs):
#     if created:
#         verification_code_model = Verification_code(user=instance, user_verification_code=, user_active_status=, )
