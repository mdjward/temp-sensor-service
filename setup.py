from setuptools import setup

setup(name='mdjward/adafruit_temp_sensor_service',
    version='0.0.1',
    description='Simple HTTP server providing temperature readings from Adafruit DHT sensors',
    author='Matthew David Ward',
    author_email='dev@mattdw.eu',
    license='GNUv3',
    packages=['adafruit_temp_sensor_service'],
    install_requires=[
        'flask',
        'Adafruit-DHT',
    ],
    test_suite='tests',
    tests_require=[
        'setuptools',
        'pytest',
        'coverage',
        'behave',
        'unittest-data-provider',
    ],
    zip_safe=True)
