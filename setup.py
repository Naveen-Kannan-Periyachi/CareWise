from setuptools import setup, find_packages

setup(
    name="carewise",
    version="1.0.0",
    description="Biomedical Research Assistant with LLM-powered query intelligence",
    author="Your Name",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "carewise=carewise.__main__:main",
        ],
    },
)
