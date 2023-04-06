import instruction_set


class VirtualMachine:
    class DataStorages:
        def __init__(self, memory_size):
            self.ac1_register = 0
            self.ac2_register = 0
            self.ac3_register = 0
            self.ac4_register = 0
            self.program_counter = 0

            self.memory = [0] * memory_size

        def get_register_value(self, index):
            return getattr(self, f"ac{index}_register", 0)

        def set_register_value(self, value, index):
            self.get_register_value(index)  # verify if this register exists
            return setattr(self, f"ac{index}_register", value)

    def __init__(self, program, memory_size):
        print("Starting VM....")
        self.instruction_register = 0
        self.program = program
        self.data = self.DataStorages(memory_size)

    def run(self):
        print(f"Executing {len(self.program)} instructions:")
        while self.data.program_counter < len(self.program):
            operation_type, operation_code = self.fetch_decode()
            print(
                f"Instruction {hex(self.instruction_register)} at {self.data.program_counter - 1}"
            )
            self.execute(operation_type, operation_code)
            print("Done.")
            print("State:\nPC:", self.data.program_counter, end=" ")
            print("AC1:", self.data.ac1_register, end=" ")
            print("AC2:", self.data.ac2_register, end=" ")
            print("AC3:", self.data.ac3_register, end=" ")
            print("AC4:", self.data.ac4_register)
            print("Memory:", self.data.memory)

    def fetch(self):
        self.instruction_register = self.program[self.data.program_counter]
        self.data.program_counter += 1

    def decode(self):
        type_ = (
            self.instruction_register
            >> instruction_set.constants.InstructionSchema.INSTRUCTION_BODY_BITS.value
        )
        body = (
            self.instruction_register
            & instruction_set.constants.InstructionSchema.INSTRUCTION_BODY_BIT_MASK.value
        )
        return type_, body

    def fetch_decode(self):
        self.fetch()
        return self.decode()

    def execute(self, type_, operation_code):
        if type_ != instruction_set.constants.InstructionType.OPERATION.value:
            return

        if operation_code == instruction_set.constants.OperationCodes.EXIT.value:
            exit(0)

        operation_class = instruction_set.operations.OPERATION_BY_CODES.get(
            operation_code
        )

        if not operation_class:
            raise ValueError("Unsupported operation.")

        operands = self.get_operands(operation_class.NUM_OPERANDS)

        operation = operation_class(self.data.program_counter, *operands)
        operation.run(self.data)

    def get_operands(self, num_operands):
        operands = []
        for _ in range(num_operands):
            self.fetch()
            type_, value = self.decode()
            operands.append((type_, value))

        return operands
