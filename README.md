# MultivaluedDict

![PyPI](https://img.shields.io/pypi/v/multivalued-dict?color=red)
![PyPI - Status](https://img.shields.io/pypi/status/multivalued-dict)
![GitHub Release Date](https://img.shields.io/github/release-date/fsssosei/MultivaluedDict)
[![Build Status](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/badges/build.png?b=master)](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/build-status/master)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/fsssosei/MultivaluedDict.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/fsssosei/MultivaluedDict/context:python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a486aacc36da4dea8016136bd0f52d5f)](https://www.codacy.com/app/fsssosei/MultivaluedDict?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fsssosei/MultivaluedDict&amp;utm_campaign=Badge_Grade)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/?branch=master)
![PyPI - Downloads](https://img.shields.io/pypi/dw/multivalued-dict?label=PyPI%20-%20Downloads)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/multivalued-dict)
![PyPI - License](https://img.shields.io/pypi/l/multivalued-dict)

*Multivalued dictionary package in python.* 

*This package features a high degree of consistency with the dict native type use case, including the type of exception that occurs. On this basis, some special multi-value dictionary methods are added.*

## Installation

Installation can be done through pip. You must have python version >= 3.7

	pip install multivalued_dict

## Usage

The statement to import the package:

	from multivalued_dict_package import *
	
Example:

	>>> mv_d = multivalued_dict()

	>>> mv_d

	multivalued_dict({})


	>>> mv_d = multivalued_dict({'a': ['test-1', 'test-2', 'test-3'], 'b': 'test-4'})

	>>> mv_d

	multivalued_dict({'a': ['test-1', 'test-2', 'test-3'], 'b': ['test-4']})


	>>> mv_d = multivalued_dict([['a', 'test-1'], ['b', 'test-2'], ['a', 'test-3']])

	>>> mv_d

	multivalued_dict({'a': ['test-1', 'test-3'], 'b': ['test-2']})


Statements for automated testing of modules:

	import multivalued_dict_package.doctestmod_module as mvdt
	mvdt.doctestmod()
