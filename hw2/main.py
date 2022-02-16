import os

from generate import generate_latex
from ast_generator.main import main as hw1_main
from table_sample import sample

if __name__ == '__main__':
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    with open('artifacts/output.tex', 'w') as f:
        hw1_main()
        f.write(generate_latex(sample, "fib.png"))
