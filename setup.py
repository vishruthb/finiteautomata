from setuptools import setup, find_packages

setup(
    name='fin-auto',
    version='0.1.2',
    description='A more intuitive way to create finite automata diagrams.',
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

