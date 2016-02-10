from django.core.urlresolvers import reverse

from django_webtest import WebTest


class ExcursionsAppTestCase(WebTest):

    def setUp(self):
        pass
        # self.user = User.objects.create(username='Tester')
        # self.top_review = BlogPost.objects.create(
            # title='First_car_review',
            # user_id=self.user.pk,
            # top_review=True,
            # featured_review=False,
        # )
        # self.featured_review = BlogPost.objects.create(
            # title='First_car_review',
            # user_id=self.user.pk,
            # top_review=False,
            # featured_review=True
        # )
        # self.fixtures = pkg_resources.resource_filename(
            # 'autodiiliweb.reviews.tests',
            # 'fixtures'
        # )

    def test_explore_page_status(self):
        # response = self.app.get(reverse(
            # 'explore', kwargs={
                # 'slug': self.top_review.slug
            # }))
        response = self.app.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)
