from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='command-tool-sdk',
    version='1.0.0',
    description='A fun admin command-line tool SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='KhoaDang2011',
    author_email='your-email@example.com',
    url='https://github.com/KhoaDang2011/command-tool-sdk',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    install_requires=[
        'click>=8.0.0',
        'colorama>=0.4.4',
        'psutil>=5.9.0',
    ],
    entry_points={
        'console_scripts': [
            'command-tool=main:cli',
        ],
    },
)
