from setuptools import setup


SHORT_DESCRIPTION = 'Documentation generator for DBML sepcification format'

try:
    with open('README.md', encoding='utf8') as readme:
        LONG_DESCRIPTION = readme.read()

except FileNotFoundError:
    LONG_DESCRIPTION = SHORT_DESCRIPTION


setup(
    name='foliantcontrib.dbmldoc',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    version='0.3.1',
    author='Daniil Minukhin',
    author_email='ddddsa@gmail.com',
    packages=['foliant.preprocessors.dbmldoc'],
    package_data={'foliant.preprocessors.dbmldoc': ['template/*.j2']},
    license='MIT',
    platforms='any',
    install_requires=[
        'foliant>=1.0.5',
        'jinja2',
        'pydbml>=0.4.1',
        'foliantcontrib.utils>=1.0.2',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Utilities",
    ]
)
