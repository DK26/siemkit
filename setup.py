from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='siemkit',
    # version='0.0.15a1.dev1',
    version='0.0.17',
    packages=['siemkit', 'hfilesize'] + find_packages(),
    include_package_data=True,
    url='https://github.com/cybersiem',
    license='Apache 2.0',
    author='CyberSIEM Community',
    author_email='dave@cybersiem.com',
    description='Open-Source Community Tools for SIEM',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[  # https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Libraries",
        "Development Status :: 1 - Planning"
    ],
    keywords=[
        'SIEM',
        'CEF',
        'LEEF',
        'SOC',
        'CYBERSIEM',
        'KIT'
    ],
    install_requires=[
        'pytimeparse',
        'dateparser',
    ],
    python_requires='>=3.8'
)
