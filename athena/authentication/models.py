import uuid
from enum import Enum

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Model

from athena.core.models import UUIDModel
from athena.edu.models import StudentGroup, Subject


class RolesEnum(Enum):
    student = "student"
    tutor = "tutor"
    teacher = "teacher"
    admin = "admin"


class Role(Model):
    name = models.CharField(
        primary_key=True,
        max_length=32,
        choices=[(role, role.value) for role in RolesEnum],
    )

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username: str, password: str, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, password: str = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self._create_user(username, password, **extra_fields)
        return user

    def create_superuser(self, username: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        user = self._create_user(username, password, **extra_fields)
        admin, _ = Role.objects.get_or_create(name="admin")
        user.roles.add(admin)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={"unique": "A user with that username already exists."},
    )
    first_name = models.CharField(max_length=30, blank=True)
    second_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    roles = models.ManyToManyField(Role, related_name="users")

    objects = UserManager()

    USERNAME_FIELD = "username"

    def _contains_role(self, role: RolesEnum):
        try:
            self.roles.get(name=role)
        except Role.DoesNotExist:
            return False
        else:
            return True

    @property
    def is_student(self) -> bool:
        return self._contains_role(RolesEnum.student)

    @property
    def is_tutor(self) -> bool:
        return self._contains_role(RolesEnum.tutor)

    @property
    def is_teacher(self) -> bool:
        return self._contains_role(RolesEnum.teacher)

    @property
    def is_admin(self) -> bool:
        return self._contains_role(RolesEnum.admin)


class Student(Model):
    cipher = models.CharField(max_length=15, unique=True, null=True)
    id = models.OneToOneField(
        User, primary_key=True, related_name="student", on_delete=models.CASCADE
    )
    student_group = models.ForeignKey(
        StudentGroup, related_name="students", null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return "{} {} {}".format(
            self.id.second_name, self.id.first_name, self.id.last_name
        )


class Tutor(Model):
    id = models.OneToOneField(
        User, primary_key=True, related_name="tutor", on_delete=models.CASCADE
    )

    def __str__(self):
        return "{} {} {}".format(
            self.id.second_name, self.id.first_name, self.id.last_name
        )


class Teacher(Model):
    id = models.OneToOneField(
        User, primary_key=True, related_name="teacher", on_delete=models.CASCADE
    )
    subjects = models.ManyToManyField(Subject, related_name="teachers")

    def __str__(self):
        return "{} {} {}".format(
            self.id.second_name, self.id.first_name, self.id.last_name
        )
