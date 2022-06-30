from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ratings(models.Model):
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rating)


class Reviews(models.Model):
    review = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.review)


class ItemQuerySet(models.QuerySet):
    def search(self, query):
        lookup = Q(name__icontains=query) | Q(category__icontains=query)

        qs = self.filter(lookup)
        return qs


class ItemManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return ItemQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_query_set().search(query)

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ratings = models.ForeignKey(Ratings, on_delete=models.CASCADE, blank=True, null=True)
    reviews = models.ForeignKey(Reviews, on_delete=models.CASCADE, blank=True, null=True)
    variants = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    objects = ItemManager()

    @property
    def avg_rating(self):
        ratings = self.ratings.all()
        return ratings.aggregate(models.Avg('rating')).get('rating__avg')

    @property
    def all_reviews(self):
        return self.reviews.all()

    def __str__(self):
        return self.name


class Order(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
