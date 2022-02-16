import setuptools

install_requires = ["graphviz==0.19.1",
                    "matplotlib==3.5.1",
                    "networkx==2.6.3",
                    "pydot==1.4.2"]

setuptools.setup(
    name="ast-generator-hw",
    version="1.7.3",
    author="Ruslan Salkaev",
    install_requires=install_requires,
    url="https://github.com/salkaevruslan/advanced-python",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
