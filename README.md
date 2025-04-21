see: https://arxiv.org/pdf/1801.08979

see: https://github.com/llvm/circt

see: https://github.com/Dragon-Git/pycde_example

```shell
pip install -e .
python src/test.py
# or
python -m src.test.py
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
pip uninstall cocotb==1.9.2
pip uninstall cocotb-test==0.2.5
pip uninstall exceptiongroup==1.2.2
pip uninstall find_libpython==0.4.0
pip uninstall iniconfig==2.0.0
pip uninstall Jinja2==3.1.4
pip uninstall MarkupSafe==3.0.2
pip uninstall numpy==2.1.2
pip uninstall packaging==24.1
pip uninstall pluggy==1.5.0
pip uninstall pybind11==2.13.6
pip uninstall pycde==0.6.1
pip uninstall pyparsing==3.1.4
pip uninstall pytest==8.3.3
pip uninstall PyYAML==6.0.2
pip uninstall -e git+https://github.com/farukyld/regex_to_seq_circ@45bc184b5884cddd568a5640c5c53cf1bb5d2f8f#egg=regex_machine
pip uninstall tomli==2.0.2