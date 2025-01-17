from setuptools import setup, find_packages

setup(
    name='litchi',
    version='0.1.2',
    description='a lilypond / csound parser',
    author="jacopo greco d'alceo",
    author_email='jacopo.grecodalceo@gmail.com',
    url='https://github.com/jacopogrecodalceo/litchi.git',
    packages=find_packages(),
    install_requires=[
        'abjad==3.19',
        'ctcsound==6.17.1',
        'numpy==2.2.1',
        'quickly==0.7.0',
        'setuptools==74.1.2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
