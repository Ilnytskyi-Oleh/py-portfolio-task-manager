from django.test import Client, TestCase
from django.urls import reverse


class LanguageSwitchTests(TestCase):
    def setUp(self) -> None:
        self.client = Client(HTTP_HOST="localhost")

    def test_set_language_uk_updates_ui_and_cache_headers(self) -> None:
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("no-cache", response.get("Cache-Control", ""))
        self.assertIn("Cookie", response.get("Vary", ""))

        set_lang = self.client.post(
            reverse("set_language"),
            data={"language": "uk", "next": login_url},
            follow=False,
        )
        self.assertEqual(set_lang.status_code, 302)
        self.assertEqual(self.client.cookies.get("django_language").value, "uk")

        translated = self.client.get(login_url)
        self.assertEqual(translated.status_code, 200)
        body = translated.content.decode()
        self.assertIn("Мова", body)
        self.assertIn('value="uk"', body)
        self.assertIn("is-active", body)
        self.assertIn("no-cache", translated.get("Cache-Control", ""))
        self.assertIn("Cookie", translated.get("Vary", ""))
