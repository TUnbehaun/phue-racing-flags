import eel
import json
import sims.acc as acc
import sims.iracing as iracing
import sims.ac as ac
from external.phue import Bridge
from external.modified.rgbxy import Converter


# GUI Theme Customization
GUI_COLOR_NO_FLAG = '#000000'
GUI_COLOR_BLUE_FLAG = '#0D47A1'
GUI_COLOR_YELLOW_FLAG = '#FFEB3B'
GUI_COLOR_BLACK_FLAG = '#000000'
GUI_COLOR_WHITE_FLAG = '#ffffff'
GUI_COLOR_CHECKERED_FLAG = '#000000'
GUI_COLOR_PENALTY_FLAG = '#b71c1c'
GUI_COLOR_GREEN_FLAG = '#388E3C'
GUI_COLOR_ORANGE_FLAG = '#FF6F00'

SAVE_FILE_PATH = './phue-rf-save.json'
HUE_CONNECTION = {
    'ip': '',
    'lights': [],
    'brightness': 255,
    'sim': 'AC',
    'colors': {
        'No_Flag': '',
        'Blue_Flag': GUI_COLOR_BLUE_FLAG,
        'Yellow_Flag': GUI_COLOR_YELLOW_FLAG,
        'Black_Flag': '',
        'White_Flag': GUI_COLOR_WHITE_FLAG,
        'Checkered_Flag': '',
        'Penalty_Flag': GUI_COLOR_PENALTY_FLAG,
        'Green_Flag': GUI_COLOR_GREEN_FLAG,
        'Orange_Flag': GUI_COLOR_ORANGE_FLAG
    },
    'auto_sync': False
}
STOP_SYNC = True


@eel.expose
def init_bridge_connection():
    load_hue_connection_from_file()
    eel.mutate_connection_works(bridge_connection_works())
    eel.mutate_hue_connection(HUE_CONNECTION)
    eel.mutate_available_lights(get_lights_from_bridge(Bridge(HUE_CONNECTION['ip'])))


@eel.expose
def connect(ip: str):
    HUE_CONNECTION['ip'] = ip
    save_hue_connection_to_file()
    init_bridge_connection()


@eel.expose
def sync_and_save_hue_connection(hueConnection):
    global HUE_CONNECTION
    HUE_CONNECTION = hueConnection
    save_hue_connection_to_file()


@eel.expose
def test_light(key: str):
    color_hex = HUE_CONNECTION['colors'][key]
    raise_color(color_hex)


@eel.expose
def start_sync():
    global STOP_SYNC
    if STOP_SYNC:
        STOP_SYNC = False
        while True:
            if HUE_CONNECTION['sim'] == 'AC':
                sync_ac_color()
                eel.sleep(0.1)

            if HUE_CONNECTION['sim'] == 'ACC':
                sync_acc_color()
                eel.sleep(0.1)

            if HUE_CONNECTION['sim'] == 'iRacing':
                sync_iracing_color()
                eel.sleep(0.1)

            if STOP_SYNC:
                break


@eel.expose
def stop_sync():
    global STOP_SYNC
    STOP_SYNC = True


def save_hue_connection_to_file():
    save_file = open(SAVE_FILE_PATH, 'w')
    json.dump(HUE_CONNECTION, save_file)


def load_hue_connection_from_file():
    try:
        save_file = open(SAVE_FILE_PATH, 'r')
        data = json.load(save_file)
        HUE_CONNECTION['ip'] = data['ip']
        HUE_CONNECTION['lights'] = data['lights']
        HUE_CONNECTION['brightness'] = data['brightness']
        HUE_CONNECTION['sim'] = data['sim'] or 'AC'
        HUE_CONNECTION['colors'] = data['colors']
        HUE_CONNECTION['auto_sync'] = data['auto_sync']
    except (FileNotFoundError, KeyError) as error:
        print(error)
        HUE_CONNECTION['ip'] = ''
        HUE_CONNECTION['lights'] = []
        HUE_CONNECTION['brightness'] = 255
        HUE_CONNECTION['sim'] = 'AC'
        HUE_CONNECTION['colors'] = {
            'No_Flag': '',
            'Blue_Flag': GUI_COLOR_BLUE_FLAG,
            'Yellow_Flag': GUI_COLOR_YELLOW_FLAG,
            'Black_Flag': '',
            'White_Flag': GUI_COLOR_WHITE_FLAG,
            'Checkered_Flag': '',
            'Penalty_Flag': GUI_COLOR_PENALTY_FLAG,
            'Green_Flag': GUI_COLOR_GREEN_FLAG,
            'Orange_Flag': GUI_COLOR_ORANGE_FLAG
        }
        HUE_CONNECTION['auto_sync'] = False


def bridge_connection_works() -> bool:
    if HUE_CONNECTION['ip'] == '':
        return False
    else:
        try:
            Bridge(HUE_CONNECTION['ip'])
            return True
        except:
            return False


def get_lights_from_bridge(bridge: Bridge) -> []:
    light_options = []
    for light in bridge.get_light_objects():
        light_options.append(light.name)
    return light_options


def raise_color(color_hex: str):
    if color_hex == '' or color_hex == '#000000':
        for light in HUE_CONNECTION['lights']:
            Bridge(HUE_CONNECTION['ip']).set_light(light, {'transitiontime': 0, 'on': False})
    else:
        converter = Converter()
        color_xy = converter.hex_to_xy(color_hex.replace('#', ''))
        for light in HUE_CONNECTION['lights']:
            Bridge(HUE_CONNECTION['ip']).set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                                           'xy': color_xy})


def raise_ac_flag(flag: ac.ACFlagType):
    if flag == ac.ACFlagType.AC_NO_FLAG:
        raise_color(HUE_CONNECTION['colors']['No_Flag'])
    if flag == ac.ACFlagType.AC_BLUE_FLAG:
        raise_color(HUE_CONNECTION['colors']['Blue_Flag'])
    if flag == ac.ACFlagType.AC_YELLOW_FLAG:
        raise_color(HUE_CONNECTION['colors']['Yellow_Flag'])
    if flag == ac.ACFlagType.AC_BLACK_FLAG:
        raise_color(HUE_CONNECTION['colors']['Black_Flag'])
    if flag == ac.ACFlagType.AC_WHITE_FLAG:
        raise_color(HUE_CONNECTION['colors']['White_Flag'])
    if flag == ac.ACFlagType.AC_CHECKERED_FLAG:
        raise_color(HUE_CONNECTION['colors']['Checkered_Flag'])
    if flag == ac.ACFlagType.AC_PENALTY_FLAG:
        raise_color(HUE_CONNECTION['colors']['Penalty_Flag'])


def raise_acc_flag(flag: acc.ACCFlagType):
    if flag == acc.ACCFlagType.ACC_NO_FLAG:
        raise_color(HUE_CONNECTION['colors']['No_Flag'])
    if flag == acc.ACCFlagType.ACC_BLUE_FLAG:
        raise_color(HUE_CONNECTION['colors']['Blue_Flag'])
    if flag == acc.ACCFlagType.ACC_YELLOW_FLAG:
        raise_color(HUE_CONNECTION['colors']['Yellow_Flag'])
    if flag == acc.ACCFlagType.ACC_BLACK_FLAG:
        raise_color(HUE_CONNECTION['colors']['Black_Flag'])
    if flag == acc.ACCFlagType.ACC_WHITE_FLAG:
        raise_color(HUE_CONNECTION['colors']['White_Flag'])
    if flag == acc.ACCFlagType.ACC_CHECKERED_FLAG:
        raise_color(HUE_CONNECTION['colors']['Checkered_Flag'])
    if flag == acc.ACCFlagType.ACC_PENALTY_FLAG:
        raise_color(HUE_CONNECTION['colors']['Penalty_Flag'])
    if flag == acc.ACCFlagType.ACC_GREEN_FLAG:
        raise_color(HUE_CONNECTION['colors']['Green_Flag'])
    if flag == acc.ACCFlagType.ACC_ORANGE_FLAG:
        raise_color(HUE_CONNECTION['colors']['Orange_Flag'])


def raise_iracing_flag(flag: iracing.IRacingGUIFlagType):
    if flag == iracing.IRacingGUIFlagType.IRACING_NO_FLAG:
        raise_color(HUE_CONNECTION['colors']['No_Flag'])
    if flag == iracing.IRacingGUIFlagType.IRACING_BLUE_FLAG:
        raise_color(HUE_CONNECTION['colors']['Blue_Flag'])
    if flag == iracing.IRacingGUIFlagType.IRACING_YELLOW_FLAG:
        raise_color(HUE_CONNECTION['colors']['Yellow_Flag'])
    if flag == iracing.IRacingGUIFlagType.IRACING_BLACK_FLAG:
        raise_color(HUE_CONNECTION['colors']['Black_Flag'])
    if flag == iracing.IRacingGUIFlagType.IRACING_WHITE_FLAG:
        raise_color(HUE_CONNECTION['colors']['White_Flag'])
    if flag == iracing.IRacingGUIFlagType.IRACING_CHEQUERED_FLAG:
        raise_color(HUE_CONNECTION['colors']['Checkered_Flag'])
    if flag == iracing.IRacingGUIFlagType.IRACING_RED_FLAG:
        raise_color(HUE_CONNECTION['colors']['Penalty_Flag'])
    if flag == iracing.IRacingGUIFlagType.IRACING_GREEN_FLAG:
        raise_color(HUE_CONNECTION['colors']['Green_Flag'])
    if flag == iracing.IRacingGUIFlagType.IRACING_MEATBALL_FLAG:
        raise_color(HUE_CONNECTION['colors']['Orange_Flag'])


def sync_ac_color():
    flag = ac.get_flag()
    raise_ac_flag(flag)


def sync_acc_color():
    flag = acc.get_flag()
    raise_acc_flag(flag)


def sync_iracing_color():
    flag = iracing.get_flag()
    raise_iracing_flag(flag)


def close_callback(route, websockets):
    if not websockets:
        stop_sync()
        exit()


if __name__ == '__main__':
    eel.init('web')
    eel.start('index.html', mode='default', size=(1600, 900))
