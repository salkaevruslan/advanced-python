import functools
from typing import List


def generate_header() -> str:
    return (
        "\\documentclass[12pt]{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{graphicx}\n"
        "\\begin{document}\n"
    )


def generate_table(table_data: List[List[str]]) -> str:
    return generate_table_header(table_data) + generate_table_body(table_data) + generate_table_footer()


def generate_table_header(table_data: List[List[str]]) -> str:
    return "\\begin{tabular}{||" + \
           functools.reduce(lambda l, _: l + "c|", table_data[0], "") + \
           "|}\n\\hline\n"


def generate_table_body(table_data: List[List[str]]) -> str:
    return functools.reduce(lambda l, r: l + "\n\\hline\n" + r,
                            map(lambda line: functools.reduce(lambda l, r: l + " & " + r, line) + " \\\\", table_data))


def generate_table_footer() -> str:
    return "\n\\hline\n\\end{tabular}\\\\\n"


def generate_image(img_path, scale) -> str:
    return f"\\includegraphics[scale={scale}]{{{img_path}}}\n"


def generate_footer() -> str:
    return "\\end{document}"


def generate_latex(table, img_path):
    return generate_header() + generate_table(table) + generate_image(img_path, 0.16) + generate_footer()
