#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <fuzzy.h>
#include <unistd.h>
#include <bytesobject.h>

#define PYDEEP_VERSION  "0.5"

static PyObject *pydeepError;

static PyObject * pydeep_hash_file(PyObject *self, PyObject *args) {
    FILE *inputFile;
    PyObject *ssdeepHash = NULL;
    char hashResult[FUZZY_MAX_RESULT];
    char *filename;
    int ret;
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }

    if (access(filename, F_OK) == -1) {
        // File does not exist
        PyErr_SetString(pydeepError, "File does not exist");
        return NULL;
    }

    inputFile = fopen(filename, "rb");
    if (inputFile <= 0) {
        // We could not open the file
        PyErr_SetString(pydeepError, "Error opening file");
        return NULL;
    }

    ret = fuzzy_hash_file(inputFile, (char*)&hashResult);
    if (ret != 0) {
        fclose(inputFile);
        PyErr_SetString(pydeepError, "Error in fuzzy_hash!");
        return NULL;
    }
    ssdeepHash = PyBytes_FromString(hashResult);
    fclose(inputFile);
    return ssdeepHash;
}

static PyObject * pydeep_hash_buf(PyObject *self, PyObject *args) {
    PyObject *ssdeepHash = NULL;
    Py_ssize_t stringSize = 0;
    char *inputBuffer = NULL;
    char hashResult[FUZZY_MAX_RESULT];
    int ret;

    if (!PyArg_ParseTuple(args, "s#", &inputBuffer, &stringSize)) {
        return NULL;
    }

    ret = fuzzy_hash_buf((unsigned char*)inputBuffer, (uint32_t)stringSize, (char*)&hashResult);
    if (ret != 0) {
        PyErr_SetString(pydeepError, "Error in fuzzy_hash!");
        return NULL;
    }
    ssdeepHash = PyBytes_FromString(hashResult);
    return ssdeepHash;
}

static PyObject * pydeep_compare(PyObject *self, PyObject *args) {
    char *ssdeepHash1 = NULL;
    char *ssdeepHash2 = NULL;
    Py_ssize_t ssdeepHash1Size = 0;
    Py_ssize_t ssdeepHash2Size = 0;
    int ret;

    if (!PyArg_ParseTuple(args, "s#s#", &ssdeepHash1, &ssdeepHash1Size, &ssdeepHash2, &ssdeepHash2Size)) {
        return NULL;
    }

    if (strlen(ssdeepHash1) != (size_t)ssdeepHash1Size || strlen(ssdeepHash2) != (size_t)ssdeepHash2Size) {
        PyErr_SetString(PyExc_ValueError, "embedded null byte");
        return NULL;
    }

    ret = fuzzy_compare(ssdeepHash1, ssdeepHash2);
    if (ret < 0) {
        PyErr_SetString(pydeepError, "Error in fuzzy compare");
        return NULL;
    }
    return PyLong_FromLong(ret);
}

// Method definitions
static PyMethodDef pydeepMethods[] = {
    {"hash_file", pydeep_hash_file, METH_VARARGS, "compute the ssdeep fuzzy hash for a file"},
    {"hash_buf", pydeep_hash_buf, METH_VARARGS, "compute the ssdeep fuzzy hash for a buffer"},
    {"hash_bytes", pydeep_hash_buf, METH_VARARGS, "compute the ssdeep fuzzy hash for a buffer"},
    {"compare", pydeep_compare, METH_VARARGS, "compute similarity between two ssdeep hashes"},
    {NULL, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "pydeep",       // m_name
    NULL,           // m_doc
    -1,             // m_size
    pydeepMethods,  // m_methods
    NULL,           // m_slots
    NULL,           // m_traverse
    NULL,           // m_clear
    NULL            // m_free
};

PyObject *PyInit_pydeep(void) {
    PyObject *pydeep;
    pydeep = PyModule_Create(&moduledef);
    if (pydeep == NULL) {
        return NULL;
    }
    pydeepError = PyErr_NewException("pydeep.Error", NULL, NULL);
    Py_INCREF(pydeepError);
    PyModule_AddObject(pydeep, "Error", pydeepError);
    PyModule_AddStringConstant(pydeep, "__version__", PYDEEP_VERSION);
    return pydeep;
}
