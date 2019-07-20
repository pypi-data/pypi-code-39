import setuptools

install_requires=[
   'vk_api',
]

setuptools.setup(
    name="mayevsky-chatbot",
    version="1.1.0",
    author="RedSnail, SomeAnonimCoder",
    author_email="oleg.demianchenko@gmail.com, glubshev2001@mail.ru",
    description="The bot for TheBigMayevsky(https://github.com/someanonimcoder/thebigmayevsky)",
    url="https://github.com/RedSnail/mayevsky-chatbot",
    packages=setuptools.find_packages(),
    install_requires=install_requires
)
