# Evaluation Review Gates

Phase 2 Package 1 adds configuration review gates, not runtime evaluation gates.

Current review gates verify that:

- the evaluation directory structure exists
- golden sets validate against `schemas/golden-set.schema.json`
- the eval suite registry validates against `schemas/eval-suite.schema.json`
- each Phase 1 core skill has exactly one eval suite entry
- every suite points to an existing golden set
- suite metadata does not reference missing Promptfoo configs or missing DeepEval tests
- documentation does not claim production observability, Promptfoo execution, DeepEval execution, dependency graph behavior, marketplace behavior, or self-improvement automation as implemented

Later Phase 2 packages may add Promptfoo execution, DeepEval execution, or CI smoke evaluation commands after those behaviors are explicitly implemented and tested.
