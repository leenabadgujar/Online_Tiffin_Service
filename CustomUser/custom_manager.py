from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, number, password=None):
        if not email:
            raise ValueError("Enter Your Email.")
        if not name:
            raise ValueError("Enter Your Name.")
        if not number:
            raise ValueError("Enter Your Number.")
        print(password)
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            number = number,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, name, email, number, password):
        user = self.create_user(
            email = self.normalize_email(email),
            name = name,
            password = password,
            number = number,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self._db)
        return user