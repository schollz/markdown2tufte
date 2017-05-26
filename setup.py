from setuptools import setup

setup(
    name='markdown2tufte',
    packages=['markdown2tufte'],
    version='0.0.1',
    description='Generate a nice HTML Tufte-like book from markdown files',
    author='schollz',
    url='https://github.com/schollz/book',
    author_email='hypercube.platforms@gmail.com',
    download_url='https://github.com/schollz/book/archive/v0.0.1.tar.gz',
    keywords=['html', 'markdown', 'tufte'],
    classifiers=[],
    install_requires=[
        "toml",
    ],
    include_package_data=True,
    package_data={
        '': ['*.html5', 'assets/*.css', 'assets/et-book/et-book-bold-line-figures/*', 'assets/et-book/et-book-display-italic-old-style-figures/*', 'assets/et-book/et-book-roman-line-figures/*', 'assets/et-book/et-book-roman-old-style-figures/*', 'assets/et-book/et-book-semi-bold-old-style-figures/*'],
    },
    setup_requires=[],
    tests_require=[],
    entry_points={'console_scripts': [
        'markdown2tufte = markdown2tufte.__main__:main',
    ], },
)
