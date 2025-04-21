see: https://arxiv.org/pdf/1801.08979

see: https://github.com/llvm/circt

see: https://github.com/Dragon-Git/pycde_example

```shell
pip install -e .
python src/test.py
# or
python -m src.test
# or to run individual tests
python -m src.frontend.ast_to_formal_circuit
python -m src.frontend.generate_grep_style
python -m src.frontend.operation_types
python -m src.frontend.regex_ast_node
python -m src.frontend.regex_normalizer
python -m src.frontend.regex_parser

python -m src.backend.builder
python -m src.backend.circuit_deser
```
