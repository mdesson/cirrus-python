try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup
    
config = {
    'description': 'Cirrus: Texting the Weather to Your Phone',
    'author': 'Michael Desson',
    'url': 'https://github.com/mdesson/cirrus.',
    'download_url': 'https://github.com/mdesson/cirrus',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['nose', 'selenium'],
    'packages': ['cirrus'],
    'scripts': [],
    'name': 'cirrus'
}

setup(**config)