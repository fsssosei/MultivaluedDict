# MultivaluedDict

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/fsssosei/MultivaluedDict.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/fsssosei/MultivaluedDict/context:python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a486aacc36da4dea8016136bd0f52d5f)](https://www.codacy.com/app/fsssosei/MultivaluedDict?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fsssosei/MultivaluedDict&amp;utm_campaign=Badge_Grade)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/?branch=master)
[![Build Status](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/badges/build.png?b=master)](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/build-status/master)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/fsssosei/MultivaluedDict/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence)

*本包特点是跟dict原生类型用例高度一致，包括发生异常的类型。在此基础上增添了一些专门的多值字典方法。*

*欢迎补全文档。*

*Multivalued dictionary package in python.* 

*Welcome to complete the documentation.*

## Installation

Installation can be done through pip. You must have python version >= 3.6.

	pip install multivalued_dict

## Usage

The statement to import the package:

	from multivalued_dict_package import multivalued_dict


or

	from multivalued_dict_package import *
	
Example:

	>>> mv_d = multivalued_dict()

	>>> mv_d

	multivalued_dict({})


	>>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})

	>>> mv_d

	multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})


	>>> mv_d = multivalued_dict([['a', 'test-1'], ['b', 'test-2'], ['a', 'test-3']])

	>>> mv_d

	multivalued_dict({'a': ['test-1', 'test-3'], 'b': ['test-2']})


Statements for automated testing of modules:

	import multivalued_dict_package.doctestmod_module as mvd
	mvd.doctestmod()
