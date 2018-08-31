from setuptools import setup

setup(
    name='note_builder',
    version='0.1.0',
    author='Justin Pinkney',
    author_email='justinpinkney@gmail.com',
    py_modules=['note_builder'],
    license='LICENSE',
    install_requires=[
        'Click', 'pygal', 'jinja2', 'tinydb'
    ],
    entry_points='''
        [console_scripts]
        note_builder=note_builder.scripts.run:build
    ''',
)
