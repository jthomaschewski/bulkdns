from setuptools import setup, find_packages

setup(
    name='cfbulk',
    version='0.0.1',
    author='Janek Thomaschewski',
    author_email='janek@thomaschewski.dev',
    description=('DNS bulk updater for Cloudflare DNS'),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click>=7',
        'cloudflare>=2',
        'pyaml>=20',
        'schema>=0.7',
    ],
    entry_points='''
      [console_scripts]
      cfbulk=cfbulk.scripts:cli
    '''
)
