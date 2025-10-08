from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured"]
                                                                        # Nanti 2 fitur terakhir hapus (?)

class RegisterForm(UserCreationForm):
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
            raise ValidationError("Password must contain at least one symbol.")
        return password
