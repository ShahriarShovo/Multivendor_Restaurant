from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError(" User must have an Email ")
        """ if not username:
            raise ValueError(" User must have an Username ") """

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
            #username=username,
            #first_name=first_name,
            #last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password=None, **extra_fields):
        user = self.create_user(
           email=self.normalize_email(email),

           #username=username,
           #first_name=first_name,
           #last_name=last_name,
           password=password,
           **extra_fields,
        )

        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):

    VENDOR=1
    CUSTOMER=2

    ROLE_CHOOSE=(
        (VENDOR,'Vendor'),
        (CUSTOMER,'Customer'),
    )


    fist_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=100, unique=True)
    phone_number=models.CharField(max_length=20, blank=True)

    role=models.SmallIntegerField(choices=ROLE_CHOOSE, blank=True, null=True)

    #requires fields
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modify_date=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects=UserManager()

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, object=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role== 1:
            user_role= 'Vendor'
            
        elif self.role== 2:
            user_role= 'Customer'
            
        return user_role


class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    profile_picture=models.ImageField(upload_to='user/profile_picture',blank=True,null=True)
    cover_photo=models.ImageField(upload_to='user/cover_picture',blank=True,null=True)
    address_line_1=models.TextField(blank=True,null=True)
    address_line_2=models.TextField(blank=True,null=True)
    country=models.CharField(max_length=50, blank=True,null=True)
    state=models.CharField(max_length=50, blank=True,null=True)
    city=models.CharField(max_length=50, blank=True,null=True)
    pin_code=models.CharField(max_length=10, blank=True,null=True)
    latitude=models.CharField(max_length=50, blank=True,null=True)
    longitute=models.CharField(max_length=50, blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modify_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username


