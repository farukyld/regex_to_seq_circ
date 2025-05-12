see: https://arxiv.org/pdf/1801.08979

see: https://github.com/llvm/circt

see: https://github.com/Dragon-Git/pycde_example

```shell
pip install -e .

export PYTHONPATH=$(pwd)/test

python test/modules/test_ciruit_deser.py
python test/modules/test_ast_to_formal_circuit.py  
python test/modules/test_regex_normalizer.py
python test/modules/test_builder.py                
python test/modules/test_regex_parser.py
python test/modules/test_flow.py

pip install -e .[dev]
python test/verification/run_testbench.py
```
