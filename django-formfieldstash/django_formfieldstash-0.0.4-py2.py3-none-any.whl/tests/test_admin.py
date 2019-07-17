# -*- coding: utf-8 -*-
from django.conf import settings
from selenium.webdriver.support.expected_conditions import visibility_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options

from formfieldstash.tests.utils.django_utils import create_superuser
from formfieldstash.tests.utils.selenium_utils import SeleniumTestCase, CustomWebDriver, \
    invisibility_of
from formfieldstash.tests.test_app.models import TestModelSingle, TestModelAdvanced

# compat
import django
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


class FormFieldStashAdminTests(SeleniumTestCase):

    def setUp(self):
        self.single_empty = TestModelSingle()
        self.single_empty.save()
        self.single = TestModelSingle(**{'selection': 'octopus', })
        self.single.save()
        self.advanced_empty = TestModelAdvanced()
        self.advanced_empty.save()
        self.advanced = TestModelAdvanced(**{'set': 'set1', })
        self.advanced.save()
        self.superuser = create_superuser()
        # Instantiating the WebDriver will load your browser
        options = Options()
        if settings.HEADLESS_TESTING:
            options.add_argument("--headless")
        self.webdriver = CustomWebDriver(firefox_options=options, )

    def tearDown(self):
        self.webdriver.quit()

    def test_app_index_get(self):
        self.login()
        self.open(reverse('admin:index'))
        self.webdriver.find_css(".app-test_app")

    def test_single_stash_empty(self):
        self.login()
        self.open(reverse('admin:test_app_testmodelsingle_change', args=[self.single_empty.id]))
        horse = self.webdriver.find_css("div.field-horse")
        # why wait? widget init delays initialization for 20ms, for other widgets to initialize.
        wait = WebDriverWait(self.webdriver, 1)
        wait.until(invisibility_of(horse))
        # self.assertFalse(horse.is_displayed())
        bear = self.webdriver.find_css("div.field-bear")
        wait.until(invisibility_of(bear))
        # self.assertFalse(bear.is_displayed())
        octo = self.webdriver.find_css("div.field-octopus")
        wait.until(invisibility_of(octo))
        # self.assertFalse(octo.is_displayed())

    def test_single_stash(self):
        self.login()
        self.open(reverse('admin:test_app_testmodelsingle_change', args=[self.single.id]))
        horse = self.webdriver.find_css("div.field-horse")
        wait = WebDriverWait(self.webdriver, 1)
        wait.until(invisibility_of(horse))
        # self.assertFalse(horse.is_displayed())
        bear = self.webdriver.find_css("div.field-bear")
        wait.until(invisibility_of(bear))
        # self.assertFalse(bear.is_displayed())
        octo = self.webdriver.find_css("div.field-octopus")
        wait.until(visibility_of(octo))
        # self.assertTrue(octo.is_displayed())
        # change select value
        self.webdriver.find_css("div.field-selection select > option[value=horse]").click()
        horse = self.webdriver.find_css("div.field-horse")
        self.assertTrue(horse.is_displayed())
        octo = self.webdriver.find_css("div.field-octopus")
        self.assertFalse(octo.is_displayed())

    def test_multi_stash_empty(self):
        self.login()
        self.open(reverse('admin:test_app_testmodeladvanced_change', args=[self.advanced_empty.id]))
        inline = self.webdriver.find_css("#testinlinemodel_set-group")
        wait = WebDriverWait(self.webdriver, 1)
        wait.until(invisibility_of(inline))
        # self.assertFalse(inline.is_displayed())
        f11 = self.webdriver.find_css("div.field-set1_1")
        wait.until(invisibility_of(f11))
        # self.assertFalse(f11.is_displayed())
        f31 = self.webdriver.find_css("div.field-set3_1")
        wait.until(invisibility_of(f31))
        # self.assertFalse(f31.is_displayed())

    def test_multi_stash(self):
        self.login()
        self.open(reverse('admin:test_app_testmodeladvanced_change', args=[self.advanced.id]))
        inline = self.webdriver.find_css("#testinlinemodel_set-group")
        wait = WebDriverWait(self.webdriver, 1)
        wait.until(visibility_of(inline))
        # self.assertTrue(inline.is_displayed())
        f11 = self.webdriver.find_css("div.field-set1_1")
        wait.until(visibility_of(f11))
        # self.assertTrue(f11.is_displayed())
        f31 = self.webdriver.find_css("div.field-set3_1")
        wait.until(invisibility_of(f31))
        # self.assertFalse(f31.is_displayed())
