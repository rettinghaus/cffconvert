import os
from pykwalify.core import Core
from ruamel.yaml import SafeConstructor
from ruamel.yaml import YAML
from cffconvert.lib.cff_1_1_x.apalike import ApalikeObject
from cffconvert.lib.cff_1_1_x.bibtex import BibtexObject
from cffconvert.lib.cff_1_1_x.codemeta import CodemetaObject
from cffconvert.lib.cff_1_1_x.endnote import EndnoteObject
from cffconvert.lib.cff_1_1_x.ris import RisObject
from cffconvert.lib.cff_1_1_x.schemaorg import SchemaorgObject
from cffconvert.lib.cff_1_1_x.zenodo import ZenodoObject
from cffconvert.lib.constants import YAML_TIMESTAMP_TYPE
from cffconvert.lib.contracts.citation import Contract
from cffconvert.root import get_package_root


class Citation_1_1_x(Contract):  # noqa

    supported_cff_versions = [
        "1.1.0"
    ]

    def __init__(self, cffstr, cffversion, preferred_citation=False, reference=None):
        self.cffstr = cffstr
        self.cffversion = cffversion
        self.preferred_citation = preferred_citation
        self.reference = reference
        self.raw_cffobj = self._parse()
        self.schema = self._get_schema()
        self.cffobj = self._select_cffobj()

    def _get_schema(self):
        schema_path = os.path.join(get_package_root(), "schemas", self.cffversion, "schema.yaml")
        with open(schema_path, "rt", encoding="utf-8") as fid:
            return YAML(typ="safe").load(fid.read())

    def _parse(self):
        # instantiate the YAML module:
        yaml = YAML(typ="safe")

        # store the current value of the timestamp parser
        tmp = yaml.constructor.yaml_constructors.get(YAML_TIMESTAMP_TYPE)

        # Configure YAML to load timestamps as timestamps:
        yaml.constructor.yaml_constructors[YAML_TIMESTAMP_TYPE] = SafeConstructor.construct_yaml_timestamp

        try:
            cffobj = yaml.load(self.cffstr)
        finally:
            # restore the old value
            yaml.constructor.yaml_constructors[YAML_TIMESTAMP_TYPE] = tmp

        if not isinstance(cffobj, dict):
            raise ValueError("Provided CITATION.cff does not seem valid YAML.")

        return cffobj

    def _get_preferred_citation(self):
        if "preferred-citation" not in self.raw_cffobj:
            raise KeyError("No 'preferred-citation' key found in CITATION.cff.")
        pref = self.raw_cffobj["preferred-citation"]
        if not isinstance(pref, dict):
            raise ValueError("Expected 'preferred-citation' to be a dictionary.")
        cffobj = pref.copy()
        cffobj["cff-version"] = self.cffversion
        return cffobj

    def _get_reference(self):
        if "references" not in self.raw_cffobj:
            raise KeyError("No 'references' key found in CITATION.cff.")
        refs = self.raw_cffobj["references"]
        if not isinstance(refs, list):
            raise ValueError("Expected 'references' to be a list.")
        try:
            idx = int(self.reference)
        except (ValueError, TypeError):
            raise ValueError(f"Reference index must be an integer, got '{self.reference}'.")
        if idx < 0 or idx >= len(refs):
            raise IndexError(f"Reference index {idx} out of bounds (0..{len(refs)-1}).")
        ref = refs[idx]
        if not isinstance(ref, dict):
            raise ValueError(f"Expected reference item at index {idx} to be a dictionary.")
        cffobj = ref.copy()
        cffobj["cff-version"] = self.cffversion
        return cffobj

    def _select_cffobj(self):
        if self.preferred_citation and self.reference is not None:
            raise ValueError("Specify either preferred_citation or reference, not both.")
        if self.preferred_citation:
            return self._get_preferred_citation()
        if self.reference is not None:
            return self._get_reference()
        return self.raw_cffobj

    def as_apalike(self):
        return ApalikeObject(self.cffobj).as_string()

    def as_bibtex(self):
        return BibtexObject(self.cffobj).as_string()

    def as_cff(self):
        return self.cffstr

    def as_codemeta(self):
        return CodemetaObject(self.cffobj).as_string()

    def as_endnote(self):
        return EndnoteObject(self.cffobj).as_string()

    def as_ris(self):
        return RisObject(self.cffobj).as_string()

    def as_schemaorg(self):
        return SchemaorgObject(self.cffobj).as_string()

    def as_zenodo(self):
        return ZenodoObject(self.cffobj).as_string()

    def validate(self, verbose=True):
        # validation using YAML based schema
        if verbose:
            print("--verbose behavior not implemented for cff-version 1.1.x, continuing...")
        Core(source_data=self.raw_cffobj, schema_data=self.schema).validate(raise_exception=True)
