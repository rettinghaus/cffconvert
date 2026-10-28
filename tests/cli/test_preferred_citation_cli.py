import tempfile
from pathlib import Path
import pytest
from click.testing import CliRunner
from cffconvert.cli.cli import cli as cffconvert


@pytest.fixture
def cff_with_preferred():
    return """cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Repo"
    given-names: "Owner"
title: "Software Repository"
preferred-citation:
  type: article
  authors:
    - family-names: "Einstein"
      given-names: "Albert"
  title: "On the Electrodynamics of Moving Bodies"
  journal: "Annalen der Physik"
  year: 1905
  doi: "10.1002/andp.19053221004"
"""


@pytest.mark.cli
def test_preferred_citation_cli_short_flag(cff_with_preferred):
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        cff_file = Path(tmpdir) / "CITATION.cff"
        cff_file.write_text(cff_with_preferred, encoding="utf-8")
        result = runner.invoke(cffconvert, ["-i", str(cff_file), "-f", "bibtex", "-p"])
    assert result.exit_code == 0
    assert "author = {Einstein, Albert}" in result.output
    assert "title = {On the Electrodynamics of Moving Bodies}" in result.output


@pytest.mark.cli
def test_preferred_citation_cli_long_flag(cff_with_preferred):
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        cff_file = Path(tmpdir) / "CITATION.cff"
        cff_file.write_text(cff_with_preferred, encoding="utf-8")
        result = runner.invoke(cffconvert, ["-i", str(cff_file), "-f", "bibtex", "--preferred-citation"])
    assert result.exit_code == 0
    assert "author = {Einstein, Albert}" in result.output
    assert "title = {On the Electrodynamics of Moving Bodies}" in result.output
