import unittest

from app import app, code_to_url, url_to_code


class UrlShortenerTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        code_to_url.clear()
        url_to_code.clear()

    def test_homepage_generates_short_url(self):
        long_url = "https://example.com/some/path"
        response = self.client.post(
            "/",
            data={"url": long_url},
        )

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn('value="https://example.com/some/path"', page)
        self.assertIn('class="result-card" id="result-card"', page)
        self.assertIn('class="short-url-field" href="http://localhost/', page)

    def test_short_code_redirects_to_original_url(self):
        code_to_url["demo"] = "https://example.com"

        response = self.client.get("/demo")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "https://example.com")


if __name__ == "__main__":
    unittest.main()
