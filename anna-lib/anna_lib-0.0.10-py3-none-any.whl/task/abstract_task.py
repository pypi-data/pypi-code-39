import abc

from selenium.webdriver.remote.webdriver import WebDriver

from anna_lib.selenium import assertions


class AbstractTask(object):
	driver: WebDriver

	def __init__(self, driver):
		self.driver = driver
		self.result = []
		self.passed = False
		self.required = True

	def execute(self) -> None:
		self.before_execute()
		self.__execute__()
		self.after_execute()
		if self.required:
			self.passed = not any(not r for r in self.result)
		else:
			self.passed = True

	@abc.abstractmethod
	def before_execute(self) -> None:
		pass

	@abc.abstractmethod
	def __execute__(self) -> None:
		pass

	@abc.abstractmethod
	def after_execute(self) -> None:
		pass

	def assert_element_exists(self, target: str) -> None:
		try:
			self.result.append({'assertion': 'element_exists', 'passed': assertions.element_exists(driver=self.driver, target=target)})
		except TypeError as e:
			self.result.append(
				{
					'assertion': 'element_exists',
					'passed': False,
					'log': str(e)
				})

	def assert_url_equals(self, expected: str) -> None:
		try:
			self.result.append({'assertion': 'url_equals',
			                    'passed': assertions.url_equals(driver=self.driver, expected=expected)})
		except ValueError as e:
			self.result.append(
				{
					'assertion': 'url_equals',
					'passed': False,
					'log': str(e)
				})

	def assert_in_url(self, part: str) -> None:
		try:
			self.result.append({'assertion': 'in_url',
			                    'passed': assertions.in_url(driver=self.driver, part=part)})
		except ValueError as e:
			self.result.append(
				{
					'assertion': 'in_url',
					'passed': False,
					'log': str(e)
				})
