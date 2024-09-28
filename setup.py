from setuptools import setup, find_packages

setup(
    name="rsa-chat",
    version="0.0.2",
    description="A simple client-server chat application with RSA encryption and Tkinter GUI",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Arsen Martirosjan",
    author_email="martirosjan.acmc@gmail.com",
    url="https://github.com/Archibald1707/cordRSA",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "sympy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
