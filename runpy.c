#define PY_SSIZE_T_CLEAN
#ifndef DOF
#define DOF 6
#endif
#include <Python.h>

void pythonner(double *q_array, double *pot)
{
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    int i;

    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append(\".\")");
    pName = PyUnicode_DecodeFSDefault("sop_fbr");
    /* Error checking of pName left out */

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, "sop_fun");
        /* pFunc is a new reference */

        if (pFunc && PyCallable_Check(pFunc)) {
            pArgs = PyTuple_New(DOF);

            for (i = 0; i < DOF; ++i) {
                pValue = PyFloat_FromDouble(q_array[i]);
                if (!pValue) {
                    Py_DECREF(pArgs);
                    Py_DECREF(pModule);
                    fprintf(stderr, "Cannot convert argument\n");
                }
                /* pValue reference stolen here: */
                PyTuple_SetItem(pArgs, i, pValue);
            }

            pValue = PyObject_CallObject(pFunc, pArgs);
            *pot =  PyFloat_AsDouble(pValue);

            } 

        else {
            Py_DECREF(pFunc);
            Py_DECREF(pModule);
            PyErr_Print();
            fprintf(stderr,"Call failed\n");\
        } 
    }
    
}

int main(int argc, char const *argv[])
{
    double geotest[DOF] = {2, 2.2, 2.4, 0.7, 0.9, 1.4};
    double vsop = 0;
    pythonner(geotest, &vsop);
    printf("%f\n", vsop);
    return 0;
}