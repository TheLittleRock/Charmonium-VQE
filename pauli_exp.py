from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator, SparsePauliOp
from qiskit.primitives import StatevectorSampler, PrimitiveJob
from qiskit.circuit.library import TwoLocal
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_aer import AerSimulator
from qiskit_nature.second_q.circuit.library import UCC, UCCSD
from qiskit.quantum_info import Pauli
from qiskit.circuit import Parameter
import numpy as np
import matplotlib.pyplot as plt
from sys import modules

def pauli_exp_circ(pauli_str, index = 0, pm = 1):

    theta = Parameter("theta{}".format(index))

    qc = QuantumCircuit(pauli_str.num_qubits, name="exp(ip{})".format(str(pauli_str)))
    num_q = pauli_str.num_qubits
    p = str(pauli_str)
    pr = str(pauli_str)[::-1]
    
    for i in range(num_q):

        if pr[i] == "X": 
            qc.h(i)
        elif pr[i] == "Y":
            qc.sdg(i)
            qc.h(i)
        else:
            pass

    for i in range(num_q-1,0,-1):

        if pr[i] == "I":
            pass
        else:
            j = i-1
            while j >= 0:
                if pr[j] == "I": 
                    j -= 1
                else:
                    qc.cx(i,j)
                    break
    i = 0
    while i < num_q:
        if pr[i] != "I":
            if pm == 1:
                qc.rz(theta, i)
            else:
                qc.rz(-theta, i)
            break
        else:
            i+=1


    for i in range(num_q-1):

        if pr[i] == "I":
            pass
        else:
            j = i+1
            while j < num_q:
                if pr[j] == "I": 
                    j += 1
                else:
                    qc.cx(j,i)
                    break
    
    for i in range(num_q):

        if pr[i] == "X": 
            qc.h(i)
        elif pr[i] == "Y":
            qc.h(i)
            qc.s(i)
        else:
            pass
        
    
    return qc