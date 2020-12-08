from setuptools import setup


setup(
    name="configatron",
    version="1.0.0",
    platforms="any",
    description="Efficient handling of large configuration files.",
    author="Vlad Temian",
    author_email="vladtemian@gmail.com",
    url="https://github.com/vtemian/configatron",
    packages=["configatron", "configatron.nodes"],
    include_package_data=True,
    extras_require={
        "dev": [
            "pytest",
            "black",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
