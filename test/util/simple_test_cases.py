
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
    "a|a",
    "a|a|a|a|a|a|a|a|a|a",
    "a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a",
    "(a|a);b",
    "(a|a|a|a|a|a|a|a|a|a);b",
    "(a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a);b",
    "(a|a);(b|c)*",
    "(a|a|a|a|a|a|a|a|a|a);(b|c)*",
    "(a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a);(b|c)*",
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
]


# see: https://chatgpt.com/share/683be9e6-eac0-800f-919e-ab41ba76685e
benchmarking_compact_forms: dict[str, str] = {
    "(a;b|b)*;b;a": "(a;b|b)*;b;a",  # Example: same as original (if
    # no better compact form)
    "a|a": "a|a#2",  # Compact form: "a|a" is the same as "a"
    "a|a|a|a|a|a|a|a|a|a": "a|a#10",
    "a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a": "a|a#20",
    "(a|a);b": "a|a#2;b",
    "(a|a|a|a|a|a|a|a|a|a);b": "a|a#10;b",
    "(a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a);b": "a|a#20;b",
    "(a|a);(b|c)*": "a|a#2;(b|c)*",
    "(a|a|a|a|a|a|a|a|a|a);(b|c)*": "a|a#10;(b|c)*",
    "(a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a|a);(b|"
    "c)*": "a|a#20;(b|c)*",
    "a*;a;(a|b)": "a*;a;(a|b)",
    "a*;a;(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|"
    "u|v|x|y|w|z)": "a*;a;([a-z])",
    "a*;a;(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t"
    "|u|v|x|y|w|z|0|1|2|3|4|5|6|7|8|9|A|B|C|D|E|"
    "F|G|H|I|J|K|L|M|N|O|P|R|S|T|U|V|X|Y|W"
    "|Z)": "a*;a;([a-z0-9A-Z])",
    "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|"
    "u|v|x|y|w|z)*;a;(a|b|c|d|e|f|g|h|i|j|k|l|"
    "m|n|o|p|r|s|t|u|v|x|y|w|z)*;b;(a|b|c|d|e|f"
    "|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|x|y|w|z)*;c;"
    "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|"
    "x|y|w|z)*": "([a-z])*;a;([a-z])*;b;([a-z])*"
    ";c;([a-z])*",
    "(a|b)*;a": "(a|b)*;a",
    "(a|b)*;a;(a|b);(a|b);(a|b);(a|b);(a|b)": "("
    "a|b)*;a;(a|b){5}",
    "(a|b)*;a;(a|b);(a|b);(a|b);(a|b);(a|b);(a|b"
    ");(a|b);(a|b);(a|b);(a|b);(a|b);(a|b);(a|b)":
    "(a|b)*;a;(a|b){13}",
}
assert (set(benchmarking).__eq__(set(benchmarking_compact_forms.keys())))


assert (set(benchmarking) == set(benchmarking_compact_forms.keys()))
