from setuptools import setup

setup(name='mdjward/temp-sensor-service',
    version='0.0.1',
    description='Simple HTTP server providing temperature readings from Adafruit DHT sensors',
    author='Matthew David Ward',
    author_email='dev@mattdw.eu',
    license='GNUv3',
    packages=['eu.mattdw.temp_sensor_service'],
    install_requires=[
        'flask',
        'Adafruit_DHT',
    ],
    test_suite='tests',
    tests_require=[
        'pytest',
        'coverage',
        'behave',
    ],
    zip_safe=True)
