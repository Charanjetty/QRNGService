
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

circuit = QuantumCircuit(1, 1)
circuit.h(0)
circuit.measure(0, 0)
simulator = AerSimulator()


def generate_random_bits(n: int) -> str:
    # Generate n random bits using a simulated qubit in superposition.
    # Each bit comes from: Hadamard(|0>) -> measure -> a single '0'/'1' outcome per shot.
    if n == 0:
        return ""
    job = simulator.run(circuit, shots=n, memory=True)
    memory = job.result().get_memory(circuit)
    return "".join(memory)


from scipy.stats import chi2


def validate_randomness(bits: str, alpha: float = 0.05) -> dict:
    """
    Chi-square goodness-of-fit test for unbiased random bits.
    """

    n = len(bits)

    if n == 0:
        return {
            "n": 0,
            "passed": None,
            "reason": "empty sample",
        }

    zeros = bits.count("0")
    ones = bits.count("1")

    expected = n / 2

    stat = ((zeros - expected) ** 2 / expected) + (
        (ones - expected) ** 2 / expected
    )

    p_value = chi2.sf(stat, 1)

    return {
        "n": int(n),
        "zeros": int(zeros),
        "ones": int(ones),
        "chi_square": float(round(stat, 4)),
        "p_value": float(round(p_value, 6)),
        "passed": bool(p_value > alpha),
    }