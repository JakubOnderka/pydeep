import io
import os
import sys
import glob

if os.path.exists("../build"):
    sys.path.insert(0, glob.glob('../build/lib.*-' + str(sys.version_info[0]) + '.*')[0])
import pydeep

testL = [
    ('calc.exe', 114688, b'1536:JEl14rQcWAkN7GAlqbkfAGQGV8aMbrNyrf1w+noPvLV6eBsCXKc:JYmZWXyaiedMbrN6pnoXL1BsC'),
    ('notepad.exe', 69120, b'1536:0awOnbNQKLjWDyy1o5RefYMJUEbooPRrKKRl1P3:0YNQKPWDyDRefVJltZrpRl1P3'),
    ('bc', 77168, b'1536:MsjYdR3Bul8hcURWhEcg4/btZzDcQflbCUPEBEh8wkcGDioxMYeo7:TYf8l8htRWA4ztZsGlWUPEBEh8wmxMYe')
]


def test_pydeep():
    for test in testL:
        filename, filelen, filehash = test
        data = io.open(filename, 'rb').read()
        hash_buf = pydeep.hash_buf(data)
        hash_file = pydeep.hash_file(filename)
        assert len(data) == filelen, "File length error"
        assert hash_buf == filehash, "Error hashing %s using hash_buf" % filename
        assert hash_file == filehash, "Error hashing %s using hash_file" % filename


def test_pydeep_compare():
    hash1 = testL[0][-1]
    hash2 = testL[1][-1]
    assert pydeep.compare(hash1, hash2) == 0, "Error fuzzy compare value"
    # Same hash
    assert pydeep.compare(b"96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16", b"96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16") == 100
    assert pydeep.compare("96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16", "96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16") == 100
    assert pydeep.compare("96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16", b"96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16") == 100
    # Similar hash
    assert pydeep.compare(b"96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16", b"96:aN0jOc0WlWW+LWQnjv7ufGcE5ESr5YaZ6uicEDEO9VCN116Sb5EutkB:aSeoF+L/zqfGtfr5YiWcsVCv16W5htk") == 40
    assert pydeep.compare("96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16", "96:aN0jOc0WlWW+LWQnjv7ufGcE5ESr5YaZ6uicEDEO9VCN116Sb5EutkB:aSeoF+L/zqfGtfr5YiWcsVCv16W5htk") == 40
    assert pydeep.compare("96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16", b"96:aN0jOc0WlWW+LWQnjv7ufGcE5ESr5YaZ6uicEDEO9VCN116Sb5EutkB:aSeoF+L/zqfGtfr5YiWcsVCv16W5htk") == 40

    try:
        pydeep.compare(b"96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16\x00", b"96:CFzROqsgconvv7uUo6jTcEGEvpVCN116S:CNVnqj8cMVCv16\x00")
        assert False
    except Exception as e:
        assert isinstance(e, ValueError)


if __name__ == "__main__":
    print('Using %s, version %s' % (pydeep.__file__, pydeep.__version__))
    test_pydeep()
    test_pydeep_compare()
    print('Tests Successful')
