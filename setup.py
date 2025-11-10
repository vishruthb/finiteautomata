from setuptools import setup, find_packages

setup(
    name='finiteautomata',
    version='1.2.0',
    description='A more intuitive way to create finite automata diagrams.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/vishruthb/finiteautomata",
    author='Vishruth Bharath',
    author_email='',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'cairo': ['cairosvg>=2.7'],
        'dev': ['pytest>=7.0', 'pytest-cov>=4.0', 'cairosvg>=2.7'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

