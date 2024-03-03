from setuptools import find_packages, setup

setup(
    name='NAMeCSaverCam',
    packages=find_packages(include=['mypythonlib']),
    version='0.1.0',
    description='Librairie pour utiliser la caméra pour NAMeC-Saver.',
    author='Noémie L "Mimolette"',
    #install_requires=["opencv-python","picamera2","numpy"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)