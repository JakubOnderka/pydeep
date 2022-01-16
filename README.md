# pydeep

Python/C bindings for the [ssdeep](https://ssdeep-project.github.io/ssdeep/index.html) library.

### Forked from [kbandla/pydeep](https://github.com/kbandla/pydeep)

* Fixed `DeprecationWarning: PY_SSIZE_T_CLEAN will be required for '#' formats`
* Published wheels at PyPI for x86_64 and aarch64

### Installation 

Requires Python 3.6 or later. For older Python version, you can use [original pydeep](https://github.com/kbandla/pydeep).

From PyPI:

    pip install pydeep2

From source (ssdeep library must be already installed):

    python setup.py build
    python setup.py test
    sudo python setup.py install

### Usage

Methods:

* `pydeep.hash_buf` / `pydeep.hash_bytes` - returns the ssdeep hash for a given buffer
* `pydeep.hash_file` - returns the ssdeep hash for filepath
* `pydeep.compare` - returns the % match between 2 hashes

Example:

```python
import pydeep
hash1 = pydeep.hash_buf('somedata')
hash2 = pydeep.hash_file('/path/to/file')
pydeep.compare(hash1, hash2)
```

## Copyright

* 2011-2012 Kiran Bandla <kbandla@in2void.com>
* 2021 Jakub Onderka
