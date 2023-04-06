from enum import Enum


class InstructionSchema(Enum):
    INSTRUCTION_BODY_BITS = 12
    INSTRUCTION_TYPE_BITS = 4
    INSTRUCTION_SIZE_BITS = 16
    INSTRUCTION_BODY_BIT_MASK = 0xFFF


class InstructionType(Enum):
    POS_INT = 0x00  # positive integer
    NEG_INT = 0x01  # negative integer
    MEM_ADDR = 0x02  # memory address
    OPERATION = 0x03  # operation
    REG_INDEX = 0x04  # register index


class OperationCodes(Enum):
    EXIT = 0x000  # exit
    LOAD = 0x002  # load operand to register or memory location
    INC = 0x003  # increment value in register or at memory location
    ADD = 0x004  # add value of operand1 memory loc or register to operand2 and store in operand1
    MUL = 0x005  # multiply value of operand1 memory loc or register and operand2 and store in operand1
    # jump to the instruction with the address of operand1 in program memory
    JUMP = 0x006
    JUMP_NOT_ZERO = 0x007  # jump to operand1 if operand2 is not zero
    JUMP_GT_THAN = 0x008  # jump to operand1 if operand2 greater than operand3
    JUMP_LT_THAN = 0x009  # jump to operand1 if operand2 less than operand3
