import django.contrib.auth.models as auth_models
import factory
from faker import Faker

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = auth_models.User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@domain.com")
    password = "some_password"
