"""
This module contains the definition of the SOP-FBR function
"""
import numpy as np
from numpy.polynomial import chebyshev as cheby
import tensorly as tl

# Define system parameters

CHEBDIM = 7
GDIM = np.array([5, 5, 5, 5, 5, 5])
NCHEB = np.sum(GDIM) * CHEBDIM

CARRAY = np.loadtxt('./params_init')
CORA = CARRAY[NCHEB::].reshape(GDIM)
STUB_CHEB = np.array(np.split(CARRAY[:NCHEB],
                              CARRAY[:NCHEB].shape[0] / CHEBDIM))
CHEBS = np.array(np.split(STUB_CHEB, np.cumsum(GDIM))[0:-1])

# Define the SOP-FBR function


def sop_fun(r2, r3, r1, t2, t1, ph):
    """
    Computes the value of the SOP-FBR potential by first
    conforming the vij(k) matrices, then reshaping
    the core tensor, and performing the tensor n-mode product.
    Parameters
    ==========
    q_array : array
             Array of the values of the DVR in each DOFs
    Returns
    =======
    prod : float or array
         The values of the SOP-FBR in a point or in a grid
    """
    q_array = r2, r3, r1, t2, t1, ph
    # Generates the matrices (or vectors) of the SPPs

    v_matrices = []
    for kdof, m_kp in enumerate(GDIM):
        v_kp = np.zeros(m_kp)
        for j_kp in np.arange(m_kp):
            v_kp[j_kp] = cheby.chebval(
                q_array[kdof], CHEBS[kdof][j_kp])
        v_matrices.append(v_kp)
    v_matrices = np.array(v_matrices)

    # Tensor n-mode product of the Tucker tensor

    prod = tl.tucker_tensor.tucker_to_tensor((CORA, v_matrices))

    return float(prod[0])


if __name__ == "__main__":
    print(sop_fun(2, 2.2, 2.4, 0.7, 0.9, 1.4))
