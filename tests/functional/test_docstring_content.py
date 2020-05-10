import os

import pytest

from interrogate import config
from interrogate import coverage


HERE = os.path.abspath(os.path.join(os.path.abspath(__file__), os.path.pardir))
SAMPLE_DIR = os.path.join(HERE, "sample")
DOCSTRING_CONTENT = os.path.join(SAMPLE_DIR, "docstring_content")
FIXTURES = os.path.join(HERE, "fixtures")


@pytest.mark.parametrize(
    "paths,conf,exp_results",
    (
        (
            [os.path.join(DOCSTRING_CONTENT, "foo_method.py")],
            {},
            (6, 6, 0, "100.0", "80.0"),
        ),
    ),
)
def test_coverage_simple(paths, conf, exp_results, mocker):
    """Happy path - get expected results given a file or directory"""
    conf = config.InterrogateConfig(**conf)
    interrogate_coverage = coverage.InterrogateCoverage(paths=paths, conf=conf)

    results = interrogate_coverage.get_coverage()

    assert results.total == exp_results[0]
    assert results.covered == exp_results[1]
    assert results.missing == exp_results[2]
    assert "{:.1f}".format(results.perc_covered) == exp_results[3]
    assert (
        "{:.1f}".format(results.perc_function_quality_score) == exp_results[4]
    )
