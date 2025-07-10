# Quantum Square Root Implementation

Implementation of a non-restoring quantum square root algorithm using the Qrisp framework.

## Description

This project contains an implementation of a T-count optimized quantum square root algorithm originally proposed by Thapliyal et al. (https://arxiv.org/pdf/1706.05113). The implementation uses the Qrisp framework for quantum circuit construction.

### Key Features

- Optimized T-gate count (T-count: 14n-14)
- No garbage qubits
- Modular design using basic quantum components
- Complete implementation of all three algorithm stages:
  - Initial subtraction
  - Conditional addition/subtraction
  - Remainder restoration

## Requirements

- Python 3.8+
- Qrisp

## Installation

```bash
pip install qrisp
```

## Usage

```python
from q_isqrt.py import isqrt
from qrisp import QuantumFloat

# Prepare quantum register for input number
# Quantum float should be 2's complement and have even number of qubits
qa = QuantumFloat(5, signed=True)
qa[:] = 16  # number to calculate square root of

# Calculate square root
qf = isqrt(qa)

# Get results
root = qf.get_measurement()  # square root
remainder = qa.get_measurement()  # remainder

print(f'Input number = 16')
print(f'Square root = {root}')
print(f'Remainder = {remainder}')
```

## Code Structure

- `zcx()` - Implementation of inverted controlled NOT gate
- `peres_gate()` - Implementation of Peres gate
- `add_circuit(n)` - n-bit addition circuit
- `ctrl_add_sub_circuit(n)` - Controlled addition/subtraction circuit
- `ctrl_add_circuit(n)` - Controlled addition circuit
- `part1_circuit(n)` - First stage of algorithm (initial subtraction)
- `part2_circuit(n)` - Second stage of algorithm (iterative addition/subtraction)
- `part3_circuit(n)` - Third stage of algorithm (remainder restoration)
- `square_root_circuit(n)` - Main square root circuit
- `isqrt(R)` - High-level function for square root calculation

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Authors

- Heorhi Kupryianau (heorhi.kupryianau@tele.agh.edu.pl)

## Acknowledgments

This work was supported by the EU Horizon Europe Framework Program under Grant Agreement no. 101119547 (PQ-REACT). 
