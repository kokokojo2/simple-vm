from .exceptions import *
from .constants import *


class BaseOperation:
    OPERATION_CODE = None
    OPERANDS_SCHEMA = []
    NUM_OPERANDS = 0

    def __init__(self, at_program_counter, *operands):
        self.operand_types = [item[0] for item in operands]
        self.operand_values = [item[1] for item in operands]
        self.operands = operands
        self.validate_operands(at_program_counter)

    def validate_operands(self, program_counter):
        for idx, (op_type, acceptable_types) in enumerate(
            zip(self.operand_types, self.OPERANDS_SCHEMA)
        ):
            if op_type not in acceptable_types:
                raise InvalidOperand(
                    op_type, program_counter - self.NUM_OPERANDS + idx, acceptable_types
                )

    def run(self, data):
        raise NotImplementedError

    def dereference(self, type_, address, data):
        if type_ == InstructionType.MEM_ADDR.value:
            try:
                return data.memory[address]
            except IndexError:
                raise ValueError("Invalid memory address.")

        if type_ == InstructionType.REG_INDEX.value:
            try:
                return data.get_register_value(address)
            except AttributeError:
                raise ValueError("Invalid register index.")

    def get_operand_value(self, type_, address, data):
        value = self.dereference(type_, address, data)

        # the operand is not an address
        # might be negative or positive integer
        if value is None:
            value = address
            if type_ == InstructionType.NEG_INT.value:
                value = -value

        return value

    def set_to_address(self, type_, address, value, data):
        if type_ == InstructionType.MEM_ADDR.value:
            try:
                data.memory[address] = value
            except IndexError:
                raise ValueError("Invalid memory address.")

        if type_ == InstructionType.REG_INDEX.value:
            try:
                data.set_register_value(value, address)
            except AttributeError:
                raise ValueError("Invalid register index.")


class LoadOperation(BaseOperation):
    OPERATION_CODE = OperationCodes.LOAD.value
    OPERANDS_SCHEMA = [
        (
            InstructionType.POS_INT.value,
            InstructionType.NEG_INT.value,
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
        ),
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
        ),
    ]
    NUM_OPERANDS = 2

    def run(self, data):
        (source_type, value), (dest_type, dest_address) = self.operands
        value = self.get_operand_value(source_type, value, data)
        self.set_to_address(dest_type, dest_address, value, data)
        print(f"LOAD {value} to {dest_type}:{dest_address}")


class IncOperation(BaseOperation):
    OPERATION_CODE = OperationCodes.INC.value
    OPERANDS_SCHEMA = [
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
        ),
    ]

    NUM_OPERANDS = 1

    def run(self, data):
        ((source_type, source_address),) = self.operands
        value = self.dereference(source_type, source_address, data)
        self.set_to_address(source_type, source_address, value + 1, data)
        print(f"INC {value} in {source_type}:{source_address}")


class AddOperation(BaseOperation):
    OPERATION_CODE = OperationCodes.ADD.value
    OPERANDS_SCHEMA = [
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
            InstructionType.NEG_INT.value,
        ),
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
        ),
    ]
    NUM_OPERANDS = 2

    def run(self, data):
        (source_type, source_value), (dest_type, dest_address) = self.operands
        value1 = self.get_operand_value(source_type, source_value, data)
        value2 = self.dereference(dest_type, dest_address, data)
        self.set_to_address(dest_type, dest_address, value1 + value2, data)
        print(f"ADD {value1} {value2}, {dest_type}:{dest_address}")


class MultiplyOperation(BaseOperation):
    OPERATION_CODE = OperationCodes.MUL.value
    OPERANDS_SCHEMA = [
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
            InstructionType.NEG_INT.value,
        ),
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
        ),
    ]
    NUM_OPERANDS = 2

    def run(self, data):
        (source_type, source_value), (dest_type, dest_address) = self.operands
        value1 = self.get_operand_value(source_type, source_value, data)
        value2 = self.dereference(dest_type, dest_address, data)
        self.set_to_address(dest_type, dest_address, value1 * value2, data)
        print(f"MUL {value1} {value2}, {dest_type}:{dest_address}")


class JumpOperation(BaseOperation):
    OPERATION_CODE = OperationCodes.JUMP.value
    OPERANDS_SCHEMA = [
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
        ),
    ]
    NUM_OPERANDS = 1

    def run(self, data):
        ((jump_to_type, jump_to_address),) = self.operands
        address = self.get_operand_value(jump_to_type, jump_to_address, data)
        data.program_counter = address
        print(f"JUMP {address}")


class JumpIfNotZeroOperation(BaseOperation):
    OPERATION_CODE = OperationCodes.JUMP_NOT_ZERO.value
    OPERANDS_SCHEMA = [
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
        ),
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
            InstructionType.NEG_INT.value,
        ),
    ]
    NUM_OPERANDS = 2

    def run(self, data):
        (jump_to_type, jump_to_address), (value_type, value) = self.operands
        address = self.get_operand_value(jump_to_type, jump_to_address, data)
        value = self.get_operand_value(value_type, value, data)
        if value != 0:
            data.program_counter = address
        print(f"JUMP {address} if {value} != 0")


class JumpIfGTOperation(BaseOperation):
    OPERATION_CODE = OperationCodes.JUMP_GT_THAN.value
    OPERANDS_SCHEMA = [
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
        ),
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
            InstructionType.NEG_INT.value,
        ),
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
            InstructionType.NEG_INT.value,
        ),
    ]
    NUM_OPERANDS = 3

    def run(self, data):
        (
            (jump_to_type, jump_to_address),
            (value_type, value),
            (compared_value_type, compared_value),
        ) = self.operands
        address = self.get_operand_value(jump_to_type, jump_to_address, data)
        value = self.get_operand_value(value_type, value, data)
        compared_value = self.get_operand_value(
            compared_value_type, compared_value, data
        )
        if value > compared_value:
            data.program_counter = address
        print(f"JUMP {address} if {value} > {compared_value}")


class JumpIfLTOperation(BaseOperation):
    OPERATION_CODE = OperationCodes.JUMP_LT_THAN.value
    OPERANDS_SCHEMA = [
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
        ),
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
            InstructionType.NEG_INT.value,
        ),
        (
            InstructionType.MEM_ADDR.value,
            InstructionType.REG_INDEX.value,
            InstructionType.POS_INT.value,
            InstructionType.NEG_INT.value,
        ),
    ]
    NUM_OPERANDS = 3

    def run(self, data):
        (
            (jump_to_type, jump_to_address),
            (value_type, value),
            (compared_value_type, compared_value),
        ) = self.operands
        address = self.get_operand_value(jump_to_type, jump_to_address, data)
        value = self.get_operand_value(value_type, value, data)
        compared_value = self.get_operand_value(
            compared_value_type, compared_value, data
        )
        if value < compared_value:
            data.program_counter = address
        print(f"JUMP {address} if {value} < {compared_value}")


OPERATION_BY_CODES = {
    OperationCodes.LOAD.value: LoadOperation,
    OperationCodes.INC.value: IncOperation,
    OperationCodes.ADD.value: AddOperation,
    OperationCodes.MUL.value: MultiplyOperation,
    OperationCodes.JUMP.value: JumpOperation,
    OperationCodes.JUMP_NOT_ZERO.value: JumpIfNotZeroOperation,
    OperationCodes.JUMP_GT_THAN.value: JumpIfGTOperation,
    OperationCodes.JUMP_LT_THAN.value: JumpIfLTOperation,
}
