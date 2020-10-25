#####################################
# File Name: setup.py
# Author: Jamkung【好音宫】
# Mail: admin@jamkung.com
# Created Time:  2020-10-23 15:02:34
#####################################


from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="yg_token",
    version="1.0",
    keywords=("pip", "token", "json_web_token", "JWT"),
    description="能生成JWT的python3工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",

    url="https://github.com/BeyondLam",
    author="好音宫",
    author_email="admin@jamkung.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    python_requires=">=3",
    install_requires=[]

)
