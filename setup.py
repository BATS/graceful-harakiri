try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass
from setuptools import setup

setup(name = 'Graceful Harakiri',
      description = 'Converts SIGTERM signals to SIGINT and prints the stacktrace.',
      version = '0.1',
      author = 'Christian Facchini',
      author_email = 'cfacchini@batstrading.com',
      license = 'BSD',
      py_modules = ['gracefulharakiri'],
      entry_points = {
          'nose.plugins.0.10': [
              'gracefulharakiri = gracefulharakiri:GracefulHarakiri']
          },
      zip_safe = True
)

