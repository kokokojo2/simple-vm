import instruction_set
from vm import VirtualMachine


if __name__ == "__main__":
    print("Example 1: Add 3 and 5")
    machine = VirtualMachine(instruction_set.example.add_3_to_5, 4)
    machine.run()
    print()

    print("Example 2: Multiply 3 and -20")
    machine = VirtualMachine(instruction_set.example.multiply_3_and_minus_20, 0)
    machine.run()
    print()

    print("Example 3: Find 2^10")
    machine = VirtualMachine(instruction_set.example.compute_2_exp_10, 0)
    machine.run()
