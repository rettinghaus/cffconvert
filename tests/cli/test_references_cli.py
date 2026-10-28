import tempfile
from pathlib import Path
import pytest
from click.testing import CliRunner
from cffconvert.cli.cli import cli as cffconvert


@pytest.fixture
def cff_with_references():
    return """cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Repo"
    given-names: "Owner"
title: "Main Software"
references:
  - type: book
    authors:
      - family-names: "Knuth"
        given-names: "Donald"
    title: "The Art of Computer Programming"
    year: 1968
  - type: article
    authors:
      - family-names: "Turing"
        given-names: "Alan"
    title: "Computing Machinery and Intelligence"
    year: 1950
"""


@pytest.mark.cli
def test_references_cli_short_flag(cff_with_references):
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        cff_file = Path(tmpdir) / "CITATION.cff"
        cff_file.write_text(cff_with_references, encoding="utf-8")
        result = runner.invoke(cffconvert, ["-i", str(cff_file), "-f", "bibtex", "-r", "1"])
    assert result.exit_code == 0
    assert "author = {Turing, Alan}" in result.output
    assert "title = {Computing Machinery and Intelligence}" in result.output


@pytest.mark.cli
def test_references_cli_long_flag(cff_with_references):
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        cff_file = Path(tmpdir) / "CITATION.cff"
        cff_file.write_text(cff_with_references, encoding="utf-8")
        result = runner.invoke(cffconvert, ["-i", str(cff_file), "-f", "bibtex", "--reference", "0"])
    assert result.exit_code == 0
    assert "author = {Knuth, Donald}" in result.output
    assert "title = {The Art of Computer Programming}" in result.output
