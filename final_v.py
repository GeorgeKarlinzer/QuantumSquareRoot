import math
from qrisp import *

def zcx() -> Operation:
    """
    Builds the inverted controlled X gate
    Returns:
        Operation: the inverted controlled X gate
    """
    qc = QuantumCircuit(2)
    qc.append(XGate().control(ctrl_state=0), [0, 1])
    return qc.to_gate(name="ICX")

def peres_gate() -> Operation:
    qc = QuantumCircuit(3)
    qc.ccx(0, 1, 2)
    qc.cx(0, 1)
    return qc.to_gate(name="PERES")


def add_circuit(n: int) -> Operation:
    qc = QuantumCircuit(2 * n)
    A = [i for i in range(0, n, 1)]
    B = [i for i in range(n, 2 * n, 1)]

    # Step 1
    for i in range(1, n):
        qc.cx(B[i], A[i])
    # Step 2
    for i in range(n-2, 0, -1):
        qc.cx(B[i], B[i+1])
    # Step 3
    for i in range(0, n-1):
        qc.ccx(B[i], A[i], B[i+1])
    # Step 4
    for i in range(n-1, -1, -1):
        if i == n - 1:
            qc.cx(B[i], A[i])
        else:
            qc.append(
                peres_gate(), 
                [B[i], A[i], B[i+1]])
    # Step 5
    for i in range(1, n-1):
        qc.cx(B[i], B[i+1])
    # Step 6
    for i in range(1, n):
        qc.cx(B[i], A[i])
    return qc.to_gate(name="ADD")

def ctrl_add_sub_circuit(n: int) -> Operation:
    qc = QuantumCircuit(2 * n + 1)
    z = 0
    A = [i for i in range(1, n + 1, 1)]
    B = [i for i in range(n + 1, 2 * n + 1, 1)]

    for i in A:
        qc.cx(z, i)
    qc.append(add_circuit(n), A + B)
    for i in A:
        qc.cx(z, i)
    return qc.to_gate(name="CTRL ADD/SUB")

def ctrl_add_circuit(n: int) -> Operation:
    qc = QuantumCircuit(2 * n + 1)
    z = 0
    A = [i for i in range(1, n + 1, 1)]
    B = [i for i in range(n + 1, 2 * n + 1, 1)]

    # Step 1
    for i in range(1, n):
        qc.cx(B[i], A[i])

    # Step 2
    for i in range(n - 2, 0, -1):
        qc.cx(B[i], B[i+1])

    # Step 3
    for i in range(0, n - 1):
        qc.ccx(A[i], B[i], B[i+1])

    # Step 4
    qc.ccx(z, B[n-1], A[n-1])

    # Step 5
    for i in range(n-2, -1, -1):
        qc.ccx(A[i], B[i], B[i+1])
        qc.ccx(z, B[i], A[i])

    # Step 6
    for i in range(1, n-1):
        qc.cx(B[i], B[i+1])

    # Step 7
    for i in range(1, n):
        qc.cx(B[i], A[i])
    return qc.to_gate(name="CTRL ADD")

def part1_circuit(n: int) -> Operation:
    qc = QuantumCircuit(2 * n + 1)
    R = [i for i in range(n)]
    F = [i for i in range(n, 2 * n)]
    z = 2 * n

    # Step 1
    qc.x(R[n-2])
    # Step 2
    qc.cx(R[n-2], R[n-1])
    # Step 3
    qc.cx(R[n-1], F[1])
    # Step 4
    qc.append(zcx(), [R[n-1], z])
    # Step 5
    qc.append(zcx(), [R[n-1], F[2]])
    # Step 6
    qc.append(
        ctrl_add_sub_circuit(4),
        [z, R[n-4], R[n-3], 
        R[n-2], R[n-1], F[0], 
        F[1], F[2], F[3]])
    return qc.to_gate(name="PART 1")


def part2_circuit(n: int) -> Operation:
    qc = QuantumCircuit(2 * n + 1)
    R = [i for i in range(n)]
    F = [i for i in range(n, 2 * n)]
    z = 2 * n

    for i in range(2, n // 2):
        # Step 1
        qc.append(zcx(), [z, F[1]])
        # Step 2
        qc.cx(F[2], z)
        # Step 3
        qc.cx(R[n-1], F[1])
        # Step 4
        qc.append(zcx(), [R[n-1], z])
        # Step 5
        qc.append(zcx(), [R[n-1], F[i+1]])
        # Step 6
        for j in range(i + 1, 2, -1):
            qc.swap(F[j], F[j-1])
        # Step 7
        R_sum_qubits = [R[j] for j in
                 range(n - 2 * i - 2, n)]
        F_sum_qubits = [F[j] for j in 
                 range(0, 2 * i + 2)]
        l = len(R_sum_qubits)
        qc.append(
            ctrl_add_sub_circuit(l),
            [z] + R_sum_qubits + F_sum_qubits)
    
    return qc.to_gate(name="PART 2")

def part3_circuit(n: int) -> Operation:
    qc = QuantumCircuit(2 * n + 1)
    R = [i for i in range(n)]
    F = [i for i in range(n, 2 * n)]
    z = 2 * n
    # Step 1
    qc.append(zcx(), [z, F[1]])
    # Step 2
    qc.cx(F[2], z)
    # Step 3
    qc.append(zcx(), [R[n-1], z])
    # Step 4
    qc.append(zcx(), [R[n-1], F[n//2+1]])
    # Step 5
    qc.x(z)
    # Step 6
    qc.append(ctrl_add_circuit(n), 
        [z] + R[:] + F[:])
    # Step 7
    qc.x(z)
    # Step 8
    for j in range(n//2 + 1, 2, -1):
        qc.swap(F[j], F[j-1])
    # Step 9
    qc.cx(F[2], z)

    return qc.to_gate(name="PART 3")


def square_root_circuit(n: int) -> Operation:
    qc = QuantumCircuit(2 * n + 1)
    R = [i for i in range(n)]
    F = [i for i in range(n, 2 * n)]
    z = 2 * n

    part1 = part1_circuit(n)
    part2 = part2_circuit(n)
    part3 = part3_circuit(n)
    qc.append(part1, R[:] + F[:] + [z])
    qc.append(part2, R[:] + F[:] + [z])
    qc.append(part3, R[:] + F[:] + [z])
    return qc.to_gate(name="ISQRT")

def isqrt(R: QuantumFloat) -> QuantumFloat:
    n = R.size
    F = QuantumFloat(R.size, 0, name="F")
    z = QuantumFloat(1, 0, name="z")
    F[:] = 1
    z[:] = 0

    qs = QuantumSession()
    qs.append(square_root_circuit(n),
        R[:] + F[:] + z[:])
    
    qs.x(F[0])
    for i in range(2, n // 2 + 2):
        qs.swap(F[i], F[i - 2])

    return F

if __name__ == "__main__":
    test_cases = [i for i in range(6, 26)]
    for a in test_cases:
        n = math.ceil(math.log2(a + 1))
        if(n % 2 == 1):
            n += 1
        elif(a & (1 << (n - 1))):
            n += 2

        qa = QuantumFloat(n, 0, name="a")
        qa[:] = a
        qf = isqrt(qa)
        print(n)
        print(a)
        print(qf.get_measurement())
        print(qa.get_measurement())