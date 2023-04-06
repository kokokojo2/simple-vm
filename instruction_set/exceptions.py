class InvalidOperand(Exception):
    def __init__(self, op_type, pc, acceptable_ops):
        super().__init__(
            f"Unacceptable operand of type {op_type} at line {pc}. "
            f"Operation only accepts {acceptable_ops}."
        )


class InvalidNumberOfOperands(Exception):
    def __init__(self, num, acceptable_num, pc):
        super(
            f"Unacceptable number of operands for command at line {pc - num - 1}. "
            f"Operation only accepts {acceptable_num} operands."
        )
