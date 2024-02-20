import factory
from faker import Faker

from api.models import Link
from api.tests.factories.auth_user_factory import UserFactory

faker = Faker()


class LinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Link

    title = factory.LazyAttributeSequence(lambda o, n: f"{faker.company()}_{n}")
    keywords = []
    url = faker.url()
    notes = ""
    views = 2
    user = factory.SubFactory(UserFactory)
    flag = False
    start_time = 0
