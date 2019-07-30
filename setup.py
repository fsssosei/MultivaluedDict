'''
multivalued_dict - This is a multi-valued dictionary package.
Copyright (C) 2019  sosei

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from setuptools import setup, find_packages

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='multivalued_dict',
    version='1.4.2',
    description='Multivalued dictionary package in python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fsssosei/MultivaluedDict',
    license='GNU Affero General Public License v3',
    author='sosei',
    author_email='fss.sosei@gmail.com',
    keywords=['multivalued', 'dictionary'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
)
