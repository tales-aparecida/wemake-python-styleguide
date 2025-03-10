"""Test method contain only allowed empty lines count."""
import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongEmptyLinesCountViolation,
)
from wemake_python_styleguide.visitors.ast.function_empty_lines import (
    WrongEmptyLinesCountVisitor,
)

class_with_wrong_method = """
class WrongClass(object):

    def wrong_method(self):
        foo()

        bar()

        baz()

        lighter()
"""

class_with_valid_method = """
class WrongClass(object):

    def wrong_method(self):
        foo()
        bar()
        baz()
"""

wrong_function = """
def func():
    foo()

    a = 1 + 4

    bar()

    baz()
"""

wrong_function_with_loop = """
def func():
    for x in range(10):

        requests.get(


            'https://github.com/wemake-services/wemake-python-styleguide'
        )
"""

allow_function = """
def func():
    foo()
    if name == 'Moonflower':
        print('Love')

    baz()
"""

allow_function_with_comments = """
def test_func():
   # This function
   #
   # has lots
   #
   # of empty
   #
   # lines
   #
   # in comments
   return 0
"""

function_with_docstring = """
def test_func():
   \"""
   Its docstring

   has many new lines

   but this is

   totally fine

   we don't raise a violation for this
   \"""
   return
"""

function_with_docstring_and_comments = """
def test_func():
   \"""
   Its docstring

   has many new lines

   but this is

   totally fine

   we don't raise a violation for this
   \"""
   # This function
   #
   # has lots
   #
   # of empty
   #
   # lines
   #
   # in comments
   return 0
"""


@pytest.mark.parametrize('input_', [
    class_with_wrong_method,
    wrong_function,
    wrong_function_with_loop,
])
def test_wrong(
    input_,
    default_options,
    assert_errors,
    parse_tokens,
    mode,
):
    """Testing wrong cases."""
    file_tokens = parse_tokens(mode(input_))

    visitor = WrongEmptyLinesCountVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [WrongEmptyLinesCountViolation])


@pytest.mark.parametrize('input_', [
    class_with_valid_method,
    allow_function,
    allow_function_with_comments,
    function_with_docstring,
    function_with_docstring_and_comments,
])
def test_success(
    input_,
    parse_tokens,
    default_options,
    assert_errors,
    mode,
):
    """Testing available cases."""
    file_tokens = parse_tokens(mode(input_))

    visitor = WrongEmptyLinesCountVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])


def test_zero_option(
    parse_tokens,
    default_options,
    assert_errors,
    options,
    mode,
):
    """Test zero configuration."""
    file_tokens = parse_tokens(mode(allow_function))
    visitor = WrongEmptyLinesCountVisitor(
        options(exps_for_one_empty_line=0), file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [WrongEmptyLinesCountViolation])


def test_zero_option_with_valid_method(
    parse_tokens,
    default_options,
    assert_errors,
    options,
    mode,
):
    """Test zero configuration with valid method."""
    file_tokens = parse_tokens(mode(class_with_valid_method))
    visitor = WrongEmptyLinesCountVisitor(
        options(exps_for_one_empty_line=0), file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [])
