FROM python:3.8-slim
COPY main.py main.py
COPY generate.py generate.py
COPY table_sample.py table_sample.py
RUN mkdir -p /artifacts
RUN apt-get update; apt-get install -y texlive graphviz
RUN python3 -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ast-generator-hw==1.7.3
RUN python3 main.py

WORKDIR artifacts
RUN pdflatex output.tex
RUN rm output.aux output.log