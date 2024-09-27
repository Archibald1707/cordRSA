from setuptools import setup, find_packages

setup(
    name="rsa-chat",
    version="0.0.1",
    description="A simple client-server chat application with RSA encryption",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Arsen Martirosjan",
    author_email="martirosjan.acmc@gmail.com",
    url="https://github.com/Archibald1707/cordRSA",  # Замените на актуальный URL репозитория
    packages=find_packages(),
    install_requires=[
        "colorama",
        "sympy"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",  # Указана только лицензия MIT
    ],
    python_requires='>=3.6',  # Минимальная версия Python (если используете функции Python 3.6 и выше)
)
