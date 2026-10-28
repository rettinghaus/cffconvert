import pytest
from cffconvert.lib.citation import Citation


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
    publisher: "Addison-Wesley"
  - type: article
    authors:
      - family-names: "Turing"
        given-names: "Alan"
    title: "Computing Machinery and Intelligence"
    year: 1950
    journal: "Mind"
"""


@pytest.fixture
def cff_without_references():
    return """cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Repo"
    given-names: "Owner"
title: "Main Software"
"""


@pytest.mark.lib
def test_references_index_zero(cff_with_references):
    citation = Citation(cff_with_references, reference=0)
    bibtex = citation.as_bibtex()
    assert "author = {Knuth, Donald}" in bibtex
    assert "title = {The Art of Computer Programming}" in bibtex
    assert "year = {1968}" in bibtex


@pytest.mark.lib
def test_references_index_one(cff_with_references):
    citation = Citation(cff_with_references, reference=1)
    bibtex = citation.as_bibtex()
    assert "author = {Turing, Alan}" in bibtex
    assert "title = {Computing Machinery and Intelligence}" in bibtex
    assert "year = {1950}" in bibtex


@pytest.mark.lib
def test_references_all_formats(cff_with_references):
    citation = Citation(cff_with_references, reference=0)
    assert citation.as_bibtex() is not None
    assert citation.as_apalike() is not None
    assert citation.as_codemeta() is not None
    assert citation.as_endnote() is not None
    assert citation.as_ris() is not None
    assert citation.as_schemaorg() is not None
    assert citation.as_zenodo() is not None


@pytest.mark.lib
def test_references_missing(cff_without_references):
    with pytest.raises(KeyError, match="references"):
        Citation(cff_without_references, reference=0)


@pytest.mark.lib
def test_references_out_of_bounds(cff_with_references):
    with pytest.raises(IndexError, match="out of bounds"):
        Citation(cff_with_references, reference=5)


@pytest.mark.lib
def test_references_via_suspect_key(cff_with_references):
    citation = Citation(cff_with_references, suspect_key="references/1")
    assert "Turing, Alan" in citation.as_bibtex()
