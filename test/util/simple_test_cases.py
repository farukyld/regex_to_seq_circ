
from frontend.regex_parser import regex_pattern_to_ast
from frontend.ast_to_formal_circuit import generate_regex_from_ast

health_check = [
    "a?",
    # "b;a+*",
    # "b;a**",
    # "b;a++",
    # "b;a*+",
    "(a;b|b)*;b;a",
    "a|a|a|a|a",
    "a",
    "(a)",
    "a*",
    "a+",
    "a?",
    "a|b;c",
    "a|b|c",
    "a;b|c",
    "a+;b+",
    "a+;b*",
    "a+;b?",
    "a*;b*",
    "a*;b+",
    "a*;b?",
    "a?;b?",
    "a?;b+",
    "a?;b*",
    "a|b",
    "a;b",
    "a;(a|b)*",
    "(a;b|b)*;b+;a?",
    "(a|b|c)*;(d|e|f)*;(g;h;i)*;j",

]

benchmarking = [
    "(a;b|b)*;b;a",
    "a*;a;(a|b)",
    "a*;a;(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|x|y|w|z)",
    "a*;a;(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|x|y|w|z|0|1|2|3|"
    "4|5|6|7|8|9|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|R|S|T|U|V|X|Y|W|Z)",
    "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|x|y|w|z)*;a;(a|b|c|d|"
    "e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|x|y|w|z)*;b;(a|b|c|d|e|f|g|h|i|"
    "j|k|l|m|n|o|p|r|s|t|u|v|x|y|w|z)*;c;(a|b|c|d|e|f|g|h|i|j|k|l|m|n"
    "|o|p|r|s|t|u|v|x|y|w|z)*",
    "(a|b)*;a",
    "(a|b)*;a;(a|b);(a|b);(a|b);(a|b);(a|b)",
    "(a|b)*;a;(a|b);(a|b);(a|b);(a|b);(a|b);(a|b);(a|b);(a|b);(a|b);("
    "a|b);(a|b);(a|b);(a|b)",
    "a;"
    "((a|b|c|d|e|f|g|h|i);b"
    "|(j|k|l|m|n|o|p|r|s);c"
    "|(t|u|v|w|y|x|z|A|B);d"
    "|(C|D|E|F|G|H|I|J|K);e"
    "|(L|M|N|O|P|R|S|T|U);f"
    "|(V|W|Y|X|Z|0|1|2|3);g"
    "|(4|5|6|7|8|9);h);i",
]


# see: https://chatgpt.com/share/683be9e6-eac0-800f-919e-ab41ba76685e
benchmarking_compact_forms: dict[str, str] = {
    "(a;b|b)*;b;a": "(ab|b)*ba",  
    "a*;a;(a|b)": "a*a(a|b)",
    "a*;a;(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|"
    "u|v|x|y|w|z)": "a*a([a-z])",
    "a*;a;(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t"
    "|u|v|x|y|w|z|0|1|2|3|4|5|6|7|8|9|A|B|C|D|E|"
    "F|G|H|I|J|K|L|M|N|O|P|R|S|T|U|V|X|Y|W"
    "|Z)": "a*a([a-z0-9A-Z])",
    "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|"
    "u|v|x|y|w|z)*;a;(a|b|c|d|e|f|g|h|i|j|k|l|"
    "m|n|o|p|r|s|t|u|v|x|y|w|z)*;b;(a|b|c|d|e|f"
    "|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|x|y|w|z)*;c;"
    "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|"
    "x|y|w|z)*": "([a-z])*a([a-z])*b([a-z])*"
    "c([a-z])*",
    "(a|b)*;a": "(a|b)*a",
    "(a|b)*;a;(a|b);(a|b);(a|b);(a|b);(a|b)": "("
    "a|b)*a(a|b){5}",
    "(a|b)*;a;(a|b);(a|b);(a|b);(a|b);(a|b);(a|b"
    ");(a|b);(a|b);(a|b);(a|b);(a|b);(a|b);(a|b)":
    "(a|b)*a(a|b){13}",
    "a;("
    "(a|b|c|d|e|f|g|h|i);b|"
    "(j|k|l|m|n|o|p|r|s);c|"
    "(t|u|v|w|y|x|z|A|B);d|"
    "(C|D|E|F|G|H|I|J|K);e|"
    "(L|M|N|O|P|R|S|T|U);f|"
    "(V|W|Y|X|Z|0|1|2|3);g|"
    "(4|5|6|7|8|9);h);i":
    "a("
    "([a-i]b)b|"
    "([j-s])c|"
    "([t-zAB])d|"
    "([C-K])e|"
    "([L-U])f|"
    "([V-Z0-3])g|"
    "([4-9])h"
    ")i",
}

benchmarking_caconical_forms: dict[str, str] = {
    generate_regex_from_ast(regex_pattern_to_ast(regex)): regex for regex in benchmarking
}

assert (set(benchmarking) == set(benchmarking_compact_forms.keys()))
