import external.modified.irsdk as irsdk
from enum import Enum


class IRacingMemoryFlagType(Enum):
    # global flags
    checkered = 0x0001
    white = 0x0002
    green = 0x0004
    yellow = 0x0008
    red = 0x0010
    blue = 0x0020
    debris = 0x0040
    crossed = 0x0080
    yellow_waving = 0x0100
    one_lap_to_green = 0x0200
    green_held = 0x0400
    ten_to_go = 0x0800
    five_to_go = 0x1000
    random_waving = 0x2000
    caution = 0x4000
    caution_waving = 0x8000

    # drivers black flags
    black = 0x010000
    disqualify = 0x020000
    servicible = 0x040000  # car is allowed service (not a flag)
    furled = 0x080000
    repair = 0x100000

    # start lights
    start_hidden = 0x10000000
    start_ready = 0x20000000
    start_set = 0x40000000
    start_go = 0x80000000


class IRacingGUIFlagType(Enum):
    IRACING_NO_FLAG = 0
    IRACING_BLUE_FLAG = 1
    IRACING_MEATBALL_FLAG = 2
    IRACING_BLACK_FLAG = 3
    IRACING_YELLOW_FLAG = 4
    IRACING_GREEN_FLAG = 5
    IRACING_WHITE_FLAG = 6
    IRACING_CHEQUERED_FLAG = 7
    IRACING_RED_FLAG = 8


def get_flag() -> IRacingGUIFlagType:
    memory_flags = []
    gui_flags = []
    ir = irsdk.IRSDK()
    ir.startup()
    session_flag = ir['SessionFlags']

    if session_flag:
        for flag in IRacingMemoryFlagType:
            if IRacingMemoryFlagType(flag).value & session_flag == IRacingMemoryFlagType(flag).value:
                memory_flags.append(flag)

        if IRacingMemoryFlagType.blue in memory_flags:
            gui_flags.append(IRacingGUIFlagType.IRACING_BLUE_FLAG)
        if IRacingMemoryFlagType.repair in memory_flags:
            gui_flags.append(IRacingGUIFlagType.IRACING_MEATBALL_FLAG)
        if IRacingMemoryFlagType.black in memory_flags:
            gui_flags.append(IRacingGUIFlagType.IRACING_BLACK_FLAG)
        if IRacingMemoryFlagType.yellow in memory_flags or IRacingMemoryFlagType.yellow_waving in memory_flags:
            gui_flags.append(IRacingGUIFlagType.IRACING_YELLOW_FLAG)
        if IRacingMemoryFlagType.green in memory_flags:
            gui_flags.append(IRacingGUIFlagType.IRACING_GREEN_FLAG)
        if IRacingMemoryFlagType.white in memory_flags:
            gui_flags.append(IRacingGUIFlagType.IRACING_WHITE_FLAG)
        if IRacingMemoryFlagType.checkered in memory_flags:
            gui_flags.append(IRacingGUIFlagType.IRACING_CHEQUERED_FLAG)
        if IRacingMemoryFlagType.red in memory_flags:
            gui_flags.append(IRacingGUIFlagType.IRACING_RED_FLAG)

        if len(gui_flags) == 0 or len(gui_flags) > 1:
            return IRacingGUIFlagType.IRACING_NO_FLAG
        else:
            return gui_flags[0]

    else:
        return IRacingGUIFlagType.IRACING_NO_FLAG
