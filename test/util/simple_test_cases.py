
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
