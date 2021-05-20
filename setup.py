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
    version='0.3.0',
    author='Daniil Minukhin',
    author_email='ddddsa@gmail.com',
    packages=['foliant.preprocessors.dbmldoc'],
    package_data={'foliant.preprocessors.dbmldoc': ['template/*.j2']},
    license='MIT',
    platforms='any',
    install_requires=[
        'foliant>=1.0.5',
        'jinja2',
        'pydbml>=0.4.0',
        'foliantcontrib.utils.combined_options>=1.0.7',
        'foliantcontrib.utils.preprocessor_ext',
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
