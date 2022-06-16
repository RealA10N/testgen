from setuptools import setup

with open("README.md", mode="r", encoding="utf8") as f:
    README = f.read()

with open("example.py", mode="r", encoding="utf8") as f:
    EXAMPLE = f'```python\n{f.read()}```'

with open("requirements.txt", mode="r", encoding="utf8") as f:
    DEPENDENCIES = f.read().splitlines()

setup(
    name='testgen',
    version='0.2',
    description='Generate random reproducible competitvie programming tests',
    author='Alon Krymgand',
    long_description=README + '\n' + EXAMPLE,
    long_description_content_type='text/markdown',
    url='https://github.com/RealA10N/testgen',
    py_modules=['testgen'],
    install_requires=DEPENDENCIES,
)
