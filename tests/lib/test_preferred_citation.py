import pytest
from cffconvert.lib.citation import Citation


@pytest.fixture
def cff_with_preferred():
    return """cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Repo"
    given-names: "Owner"
title: "Software Repository"
date-released: "2020-01-01"
preferred-citation:
  type: article
  authors:
    - family-names: "Einstein"
      given-names: "Albert"
  title: "On the Electrodynamics of Moving Bodies"
  journal: "Annalen der Physik"
  year: 1905
  month: 6
  volume: 17,
  issue: 10,
  pages: "891-921"
  doi: "10.1002/andp.19053221004"
"""


@pytest.fixture
def cff_without_preferred():
    return """cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Repo"
    given-names: "Owner"
title: "Software Repository"
"""


@pytest.mark.lib
def test_preferred_citation_bibtex(cff_with_preferred):
    citation = Citation(cff_with_preferred, preferred_citation=True)
    bibtex = citation.as_bibtex()
    assert "author = {Einstein, Albert}" in bibtex
    assert "title = {On the Electrodynamics of Moving Bodies}" in bibtex
    assert "doi = {10.1002/andp.19053221004}" in bibtex
    assert "year = {1905}" in bibtex


@pytest.mark.lib
def test_preferred_citation_apalike(cff_with_preferred):
    citation = Citation(cff_with_preferred, preferred_citation=True)
    apalike = citation.as_apalike()
    assert "Einstein A." in apalike
    assert "On the Electrodynamics of Moving Bodies" in apalike
    assert "(1905)." in apalike


@pytest.mark.lib
def test_preferred_citation_all_formats(cff_with_preferred):
    citation = Citation(cff_with_preferred, preferred_citation=True)
    assert citation.as_bibtex() is not None
    assert citation.as_apalike() is not None
    assert citation.as_codemeta() is not None
    assert citation.as_endnote() is not None
    assert citation.as_ris() is not None
    assert citation.as_schemaorg() is not None
    assert citation.as_zenodo() is not None


@pytest.mark.lib
def test_preferred_citation_missing(cff_without_preferred):
    with pytest.raises(KeyError, match="preferred-citation"):
        Citation(cff_without_preferred, preferred_citation=True)


@pytest.mark.lib
def test_preferred_citation_and_reference_conflict(cff_with_preferred):
    with pytest.raises(ValueError, match="Specify either preferred_citation or reference"):
        Citation(cff_with_preferred, preferred_citation=True, reference=0)


@pytest.mark.lib
def test_preferred_citation_via_suspect_key(cff_with_preferred):
    citation = Citation(cff_with_preferred, suspect_key="preferred-citation")
    assert "Einstein, Albert" in citation.as_bibtex()
