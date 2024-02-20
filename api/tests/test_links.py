import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.models import Link
from api.tests.factories.link_factory import LinkFactory


class TestLink(TestCase):
    def test_get_link(self):
        """GET /api/v1/links/1"""
        link: Link = LinkFactory.create()

        response = self.client.get(reverse("link", kwargs={"link_id": link.id}))
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(link.id, content["id"])

    def test_get_all_links(self):
        """GET /api/v1/links"""
        LinkFactory.create()
        LinkFactory.create()

        response = self.client.get(reverse("links"))
        content: list = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(content))

    def test_get_random_link(self):
        """GET /api/v1/links?random"""
        link1 = LinkFactory.create()
        link2 = LinkFactory.create()

        response = self.client.get(
            reverse("links", kwargs={"link_id": 1}), json.dumps({"id": 1})
        )
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(content["id"] in [link1.id, link2.id])

    def test_404_when_getting_link_that_doesnt_exist(self):
        """GET /api/v1/links?random"""
        response = self.client.get(
            reverse("links", kwargs={"link_id": 1}), json.dumps({"id": 1})
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create_new_link(self):
        """PUT /api/v1/links"""
        response = self.client.put(
            reverse("links"),
            json.dumps(
                {
                    "flag": False,
                    "keywords": [],
                    "notes": "",
                    "title": "title",
                    "url": "youtube.com",
                    "start_time": 0,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_400_WhenMissingRequiredFields(self):
        """PUT /api/v1/links"""
        response = self.client.put(
            reverse("links"),
            json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_WhenCreatingNewLink_WithSameUrlAndStartTime_ReturnExistingLink(self):
        """PUT /api/v1/links"""
        link = LinkFactory.create(url="youtu.be/CPLdltN7wgE", start_time=0)

        response = self.client.put(
            reverse("links"),
            json.dumps(
                {
                    "url": "https://www.youtube.com/watch?v=CPLdltN7wgE",
                }
            ),
            content_type="application/json",
        )
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_226_IM_USED, response.status_code)
        self.assertEqual(link.views + 1, content["views"])

    def test_updating_link_views_will_always_increment_by_one(self):
        """PUT /api/v1/links/1"""
        link = LinkFactory.create()

        response = self.client.put(
            reverse("links", kwargs={"link_id": 1}),
            json.dumps(
                {
                    "id": link.id,
                    "notes": link.notes,
                    "title": "New title",
                    "url": link.url,
                    "keywords": link.keywords,
                    "flag": link.flags,
                    "start_time": link.start_time,
                    "views": 10000,
                }
            ),
            content_type="application/json",
        )
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("New title", content["title"])
        self.assertEqual(link.views + 1, content["title"])

    def test_update_existing_link_where_ids_dont_match(self):
        """PUT /api/v1/links/1"""
        link = LinkFactory.create()

        response = self.client.put(
            reverse("links", kwargs={"link_id": link.id}),
            json.dumps(
                {
                    "id": link.id + 1,
                    "notes": link.notes,
                    "title": "New title",
                    "url": link.url,
                    "keywords": link.keywords,
                    "flag": link.flags,
                    "start_time": link.start_time,
                    "views": link.views,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete_existing_link(self):
        link = LinkFactory.create()
        link_id = link.id

        """DELETE /api/v1/links/1"""
        response = self.client.delete(reverse("links", kwargs={"link_id": link_id}))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertFalse(Link.objects.filter(id=link_id))

    def test_404_when_deleting_link_with_id_that_doesnt_exist(self):
        """DELETE /api/v1/links/1"""
        response = self.client.delete(reverse("links", kwargs={"link_id": 1}))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_405_when_deleting_without_providing_link_id(self):
        """DELETE /api/v1/links"""
        response = self.client.delete(reverse("links"))
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
