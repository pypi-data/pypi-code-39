import inspect
import discord
from discord.ext import commands


class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger(object):

    @staticmethod
    def logTest(text):
        print(bcolors.HEADER + bcolors.BOLD + '\n' + text + bcolors.ENDC)

    @staticmethod
    def logStep(text):
        print(bcolors.OKBLUE + '--> ' + text + '  ' + bcolors.ENDC)

    @staticmethod
    def logSuccess(text):
        print(bcolors.OKGREEN + '--> ' + text + bcolors.ENDC)

    @staticmethod
    def logWarning(text):
        print(bcolors.WARNING + '--> ' + text + bcolors.ENDC)

    @staticmethod
    def logFail(text):
        print(bcolors.FAIL + bcolors.BOLD + text + bcolors.ENDC)


class Test(object):

    def __init__(self, test_case, x=50):
        self.method = test_case
        self.x = x

    async def __call__(self, *args, **kwargs):
        Logger.logTest(f'Running test {self.method.__name__}')
        try:
            if inspect.iscoroutinefunction(self.method):
                await self.method(*args, **kwargs)
            else:
                self.method(*args, **kwargs)
        except TestFailedException as e:
            Logger.logFail(f'Test {self.method.__name__} failed with exception {type(e).__name__}')
            if hasattr(e, 'message'):
                Logger.logFail(f'\n{e}\n')
            return -1
        except Exception as e:
            Logger.logWarning(f'Uncaught Exception:\n\n{e}\n')
        return 0


class Teddi(commands.Cog):
    def __init__(self, token):
        self.test_suites = {}
        self.channel = None
        self.token = token
        self.client = commands.Bot(command_prefix=':')
        self.client.add_cog(self)

    def connect(self):
        self.client.run(self.token)

    async def test_all(self, test_definitions):
        test_suite = test_definitions(self)
        for function_name in dir(test_suite):
            function = getattr(test_suite, function_name)
            if isinstance(function, Test):
                await function(test_suite)

    async def test(self, test_definitions, test_name):
        test_suite = test_definitions(self)
        for function_name in dir(test_suite):
            function = getattr(test_suite, function_name)
            if isinstance(function, Test) and function.method.__name__ == test_name:
                return await function(test_suite) == 0

    def add_suite(self, test_definitions):
        self.test_suites[test_definitions.__name__] = test_definitions

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.channel is None:
            self.channel = message.channel

    @commands.command()
    async def setchannel(self, context):
        self.channel = context.channel

    @commands.command()
    async def setbot(self, context, member: discord.Member):
        if member.bot:
            self.bot = member
        else:
            await context.send('You must specify a bot user.')

    @commands.command()
    async def showtests(self, context):
        msg = '```\n'
        for test_suite in self.test_suites:
            msg += test_suite + '\n'
            for function_name in dir(self.test_suites[test_suite]):
                function = getattr(self.test_suites[test_suite], function_name)
                if isinstance(function, Test):
                    print(function.method.__name__)
                    msg += f'- {function.method.__name__}\n'
        msg += '```'
        await context.send(msg)

    @commands.command()
    async def runtests(self, context, test_suite):
        test_suite = test_suite
        if test_suite in self.test_suites:
            await self.test_all(self.test_suites[test_suite])
        else:
            await context.send('That test suite doesn\'t seem to be correct.')

    async def get_last_message(self, user=None):
        if user is None:
            user = self.bot
        async for message in self.channel.history(limit=200):
            if message.author.id == user.id:
                return message.content

    async def send_message(self, text):
        if self.channel is not None:
            await self.channel.send(text)
        else:
            pass  # TODO create exception


class TestSuite(object):
    def __init__(self, teddi):
        self.teddi = teddi


class TestFailedException(Exception):
    pass


class AssertTrueException(TestFailedException):
    pass


class AssertFalseException(TestFailedException):
    pass


class AssertEqualException(TestFailedException):
    pass


class AssertNotEqualException(TestFailedException):
    pass


def assertTrue(condition=True, fail=None, success=None):
    if condition:
        if success is not None:
            Logger.logSuccess(success)
    else:
        raise AssertTrueException(fail)


def assertFalse(condition=True, fail=None, success=None):
    if not condition:
        if success is not None:
            Logger.logSuccess(success)
    else:
        raise AssertFalseException(fail)


def assertEqual(a, b, fail=None, success=None):
    if a == b:
        if success is not None:
            Logger.logSuccess(success)
    else:
        raise AssertEqualException(fail)


def assertNotEqual(a, b, fail=None, success=None):
    if not a == b:
        if success is not None:
            Logger.logSuccess(success)
    else:
        raise AssertNotEqualException(fail)
