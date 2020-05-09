
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
        ([os.path.join(DOCSTRING_CONTENT, "foo.py"),], {}, (4, 4, 0, "100.0")),
    ),
)

def test_coverage_simple(paths, conf, exp_results, mocker):
    """Happy path - get expected results given a file or directory"""
    conf = config.InterrogateConfig(**conf)
    interrogate_coverage = coverage.InterrogateCoverage(paths=paths, conf=conf)

    results = interrogate_coverage.get_coverage()

    assert exp_results[0] == results.total
    assert exp_results[1] == results.covered
    assert exp_results[2] == results.missing
    assert exp_results[3] == "{:.1f}".format(results.perc_covered)
