from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "user"

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"


class Product(BaseModel):
    class Meta:
        db_table = "product"

    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


class Order(BaseModel):
    class Meta:
        db_table = "order"

    user = models.ForeignKey(
        CustomUser,
        related_name="orders",
        on_delete=models.CASCADE,
    )
    order_date = models.DateTimeField(null=True, blank=True)


class OrderDetail(BaseModel):
    class Meta:
        db_table = "order_detail"

    order = models.ForeignKey(
        Order,
        related_name="order_details",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name="order_details",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    quantity = models.IntegerField()


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
