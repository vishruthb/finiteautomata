from setuptools import setup, find_packages

setup(
    name='fiauto',
    version='0.1.0',
    description='A Python library for creating finite automata diagrams with intuitive syntax.',
    author='Vishruth Bharath',
    author_email='',
    packages=find_packages(),
    install_requires=[
        'graphviz',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

