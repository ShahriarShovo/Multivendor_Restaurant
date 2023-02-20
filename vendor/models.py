from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

# Create your models here.
class Vendor(models.Model):
    vendor_user=models.OneToOneField(User, related_name='vendor_user',
                              on_delete=models.CASCADE)
    vendor_user_profile=models.OneToOneField(UserProfile,related_name='vendor_user_profile',
                                      on_delete=models.CASCADE)
    vendor_name=models.CharField(max_length=50)
    vendor_license=models.ImageField(upload_to='vendor/license')
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name
    


def save(self,*args, **kwargs):

    if self.pk is not None:
        orig=Vendor.objects.get(pk=self.pk)
        if orig.is_approved != self.is_approved:
            mail_template='accounts/email/admin_approval_email.html'
            context={
                    'user' :self.user,
                    'is_approved' : self.is_approved
                }
            if self.is_approved==True:
                #send Notification
                mail_subject="Congrats ! We approved your Restuarant"
                send_notification(mail_subject,mail_template,context)
            else:
                #send Notification
                mail_subject="Sorry ! We cant approved your Restuarant"
                send_notification(mail_subject,mail_template,context)
    return super(Vendor, self).save( *args, **kwargs)

