add_3_to_5 = [
    0x03002,  # LOAD
    0x00003,  # 3
    0x04001,  # ac_1
    0x03002,  # LOAD
    0x00005,  # 5
    0x02001,  # memory address 1
    0x03004,  # ADD
    0x02001,  # memory address 1
    0x04001,  # ac_1
]

multiply_3_and_minus_20 = [
    0x03002,  # LOAD
    0x00003,  # 3
    0x04001,  # ac_1
    0x03002,  # LOAD
    0x01014,  # - 20
    0x04002,  # ac_2
    0x03005,  # MUL
    0x04001,  # ac_1
    0x04002,  # ac_2
]

compute_2_exp_10 = [
    # loading value
    0x03002,  # LOAD
    0x00002,  # 2
    0x04001,  # ac_1
    # loading exp counter
    0x03002,  # LOAD
    0x00001,  # 1
    0x04002,  # ac_2
    # finding ac_1 ^ 2
    0x03005,  # MUL, line 6
    0x00002,  # 2
    0x04001,  # ac_1
    # increment exp counter
    0x03003,  # INC
    0x04002,  # ac_2
    # jump to MUL if exp counter < 10
    0x03009,  # JUMP IF <
    0x00006,  # to line 6
    0x04002,  # ac_2
    0x0000A,  # 10
]
