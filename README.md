# cobertura_parser

get info from cobertura.xml easily

## usage

```python
from cobertura_parser import CoberturaParser
import pprint

c = CoberturaParser.from_file("tests/data/cobertura.xml")
s = c.get_structure(with_line=True)

pprint.pprint(s)
```

## installation

```bash
pip install cobertura_parser
```
