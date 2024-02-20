import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class TestLink(TestCase):
    def test_get_link(self):
        """GET /api/v1/links/1"""
        self.client.get(reverse("link", kwargs={"link_id": 1}), json.dumps({"id": 1}))

    def test_get_all_links(self):
        """GET /api/v1/links"""
        # create two links
        self.client.get(reverse("links"))
        # expect 2 links

    def test_get_random_link(self):
        """GET /api/v1/links?random"""
        self.client.get(reverse("links", kwargs={"link_id": 1}), json.dumps({"id": 1}))

    def test_404_when_getting_link_that_doesnt_exist(self):
        """GET /api/v1/links?random"""
        self.client.get(reverse("links", kwargs={"link_id": 1}), json.dumps({"id": 1}))
        # expect status.404

    def test_create_new_link(self):
        """PUT /api/v1/links/1"""
        self.client.put(
            reverse("links"),
            json.dumps({"id": 1}),
            content_type="application/json",
        )

    def test_update_existing_link(self):
        """PUT /api/v1/links/1"""
        self.client.put(
            reverse("links", kwargs={"link_id": 1}),
            json.dumps({"id": 1}),
            content_type="application/json",
        )

        self.client.put(
            reverse("links", kwargs={"link_id": 1}),
            json.dumps({"id": 1}),
            content_type="application/json",
        )

    def test_update_existing_link_where_ids_dont_match(self):
        """PUT /api/v1/links/1"""
        self.client.put(
            reverse("links", kwargs={"link_id": 1}),
            json.dumps({"id": 2}),
            content_type="application/json",
        )
        # it should return a 400 error, bad input data

    def test_delete_existing_link(self):
        """DELETE /api/v1/links/1"""
        self.client.put(
            reverse("links", kwargs={"link_id": 1}),
            json.dumps({"id": 2}),
            content_type="application/json",
        )
        # it should return a 400 error, bad input data

    def test_404_when_deleting_link_with_id_that_doesnt_exist(self):
        """DELETE /api/v1/links/1"""
        self.client.put(
            reverse("links", kwargs={"link_id": 1}),
            json.dumps({"id": 2}),
            content_type="application/json",
        )
        # it should return a 404 error, link with id doesn't exist
