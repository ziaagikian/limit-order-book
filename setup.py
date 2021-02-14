from setuptools import setup, find_packages

setup(name="limit-order-book",
      description="Python LimitOrderBook",
      url="https://github.com/ziaagikian/limit-order-book",
      version="0.0.1",
      author="Zia Ur Rahman",
      author_email="ziaagikian@gmail.com",
      license="MIT",
      packages=find_packages(exclude=["tests"]),
      platforms="any",
      scripts=["bin/script_runner.py", "bin/benchmark.py", "bin/threaded_script.py"],
      classifiers=[
        "python3", "trade", "exchange",
        "order-book", "limit-order-book"
        "multi-threading", "batches", "mongodb", "transactions"],
      python_requires=">=3.0")

