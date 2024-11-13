from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class StoreUser(User):
    contact_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\+92[0-9]{10}$')], null=False, blank=False, unique=True)

    def __str__(self):
        return self.username
    
    def __repr__(self):
        return self.username


