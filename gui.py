import external.PySimpleGUI as sg
from external.phue import Bridge
import acc
import iracing
import threading
import json
import time

# Global Variables
SAVE_FILE_PATH = './phue-rf-save.json'
HUE_CONNECTION = {
    'ip': '',
    'lights': [],
    'brightness': 255,
    'sim': 'ACC'
}

STOP_SYNC = True

# Hue Colors
HUE_COLOR_NO_FLAG = None
HUE_COLOR_BLUE_FLAG = [0.1532, 0.0475]
HUE_COLOR_YELLOW_FLAG = [0.4787, 0.4681]
HUE_COLOR_BLACK_FLAG = None
HUE_COLOR_WHITE_FLAG = [0.3089, 0.3269]
HUE_COLOR_CHECKERED_FLAG = None
HUE_COLOR_PENALTY_FLAG = [0.6897, 0.3074]
HUE_COLOR_GREEN_FLAG = [0.17, 0.7]
HUE_COLOR_ORANGE_FLAG = [0.633, 0.3522]

# GUI Theme Customization
sg.theme('Black')
GUI_COLOR_NO_FLAG = '#000000'
GUI_COLOR_BLUE_FLAG = '#0D47A1'
GUI_COLOR_YELLOW_FLAG = '#FFEB3B'
GUI_COLOR_BLACK_FLAG = '#000000'
GUI_COLOR_WHITE_FLAG = '#ffffff'
GUI_COLOR_CHECKERED_FLAG = '#000000'
GUI_COLOR_PENALTY_FLAG = '#b71c1c'
GUI_COLOR_GREEN_FLAG = '#388E3C'
GUI_COLOR_ORANGE_FLAG = '#FF6F00'


def open_window():
    global HUE_CONNECTION

    disable_lights_menu = True
    show_30_seconds_info = False
    msg_bridge = ''

    bridge: Bridge
    light_options = []

    load_hue_connection_from_file()

    if bridge_connection_works():
        disable_lights_menu = False
        msg_bridge = 'Connection established.'
        bridge = Bridge(HUE_CONNECTION['ip'])
        light_options = get_lights_from_bridge(bridge)
        show_30_seconds_info = False
    else:
        disable_lights_menu = True
        msg_bridge = 'Connection failed.'
        show_30_seconds_info = True

    # GUI Frames

    flag_frame_layout = [
        [sg.Graph(canvas_size=(875, 100), graph_bottom_left=(0, 0), graph_top_right=(875, 100),
                  background_color=GUI_COLOR_NO_FLAG, key='CANVAS_FLAG')]
    ]

    bridge_ip_frame_layout = [
        [sg.Input(key='INPUT_IP', default_text=HUE_CONNECTION['ip'], font=('Helvetica', 24), size=(15, 1)),
         sg.Button('Connect', key='BTN_BRIDGE', font=('Helvetica', 24))]
    ]

    bridge_status_frame_layout = [
        [sg.Text(size=(22, 1), key='MSG_BRIDGE', text=msg_bridge, font=('Helvetica', 24))]
    ]

    light_menu_frame_layout = [
        [sg.Listbox(values=light_options, key='MENU_LIGHT', disabled=disable_lights_menu,
                    default_values=HUE_CONNECTION['lights'], enable_events=True, font=('Helvetica', 24), size=(23, 4),
                    select_mode='multiple')]
    ]

    brightness_menu_frame_layout = [
        [sg.Slider(range=(1, 255), default_value=int(HUE_CONNECTION['brightness']), size=(20, 20),
                   orientation='horizontal', font=('Helvetica', 24), enable_events=True, key='SLIDER_BRIGHTNESS')]
    ]

    sim_select_frame_layout = [
        [sg.Radio('Assetto Corsa Competizione', 'SIM_SELECT', font=('Helvetica', 24), disabled=disable_lights_menu,
                  key='SIM_SELECT_ACC', enable_events=True, default=HUE_CONNECTION['sim'] == 'ACC'),
         sg.Radio('iRacing', 'SIM_SELECT', font=('Helvetica', 24), size=(21, 1), disabled=disable_lights_menu,
                  key='SIM_SELECT_IRACING', enable_events=True, default=HUE_CONNECTION['sim'] == 'iRacing')]
    ]

    acc_color_test_frame_layout = [
        [sg.Button('No Flag', key='BTN_ACC_NO_FLAG', button_color=('#ffffff', GUI_COLOR_NO_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Blue Flag', key='BTN_ACC_BLUE_FLAG', button_color=('#ffffff', GUI_COLOR_BLUE_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Yellow Flag', key='BTN_ACC_YELLOW_FLAG', button_color=('#000000', GUI_COLOR_YELLOW_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Black Flag', key='BTN_ACC_BLACK_FLAG', button_color=('#ffffff', GUI_COLOR_BLACK_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('White Flag', key='BTN_ACC_WHITE_FLAG', button_color=('#000000', GUI_COLOR_WHITE_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24))],
        [sg.Button('Checkered Flag', key='BTN_ACC_CHECKERED_FLAG', button_color=('#ffffff', GUI_COLOR_CHECKERED_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Penalty Flag', key='BTN_ACC_PENALTY_FLAG', button_color=('#ffffff', GUI_COLOR_PENALTY_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Green Flag', key='BTN_ACC_GREEN_FLAG', button_color=('#ffffff', GUI_COLOR_GREEN_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Orange Flag', key='BTN_ACC_ORANGE_FLAG', button_color=('#ffffff', GUI_COLOR_ORANGE_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24))]
    ]

    iracing_color_test_frame_layout = [
        [sg.Button('No Flag', key='BTN_IRACING_NO_FLAG', button_color=('#ffffff', GUI_COLOR_NO_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Blue Flag', key='BTN_IRACING_BLUE_FLAG', button_color=('#ffffff', GUI_COLOR_BLUE_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Yellow Flag', key='BTN_IRACING_YELLOW_FLAG', button_color=('#000000', GUI_COLOR_YELLOW_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Black Flag', key='BTN_IRACING_BLACK_FLAG', button_color=('#ffffff', GUI_COLOR_BLACK_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('White Flag', key='BTN_IRACING_WHITE_FLAG', button_color=('#000000', GUI_COLOR_WHITE_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24))],
        [sg.Button('Checkered Flag', key='BTN_IRACING_CHEQUERED_FLAG',
                   button_color=('#ffffff', GUI_COLOR_CHECKERED_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Red Flag', key='BTN_IRACING_RED_FLAG', button_color=('#ffffff', GUI_COLOR_PENALTY_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Green Flag', key='BTN_IRACING_GREEN_FLAG', button_color=('#ffffff', GUI_COLOR_GREEN_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Meatball Flag', key='BTN_IRACING_MEATBALL_FLAG', button_color=('#ffffff', GUI_COLOR_ORANGE_FLAG),
                   disabled=disable_lights_menu, font=('Helvetica', 24))]
    ]

    sync_controls_frame_layout = [
        [sg.Button('Start', key='BTN_SYNC_START', disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Stop', key='BTN_SYNC_STOP', disabled=disable_lights_menu, font=('Helvetica', 24))]
    ]

    sync_status_frame_layout = [
        [sg.Text(size=(34, 1), key='MSG_SYNC_STATUS', text='Stopped.', font=('Helvetica', 24))]
    ]

    # Window Layout

    layout = [
        [sg.Frame('flag', flag_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Frame('bridge ip', bridge_ip_frame_layout, font=('Helvetica', 10), title_color='#ffffff'),
         sg.Frame('bridge status', bridge_status_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Frame('lights', light_menu_frame_layout, font=('Helvetica', 10), title_color='#ffffff'),
         sg.Frame('brightness', brightness_menu_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Frame('sim', sim_select_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.pin(sg.Frame('flag test', acc_color_test_frame_layout, font=('Helvetica', 10), title_color='#ffffff',
                  visible=HUE_CONNECTION['sim'] == 'ACC', key='FRAME_ACC_FLAGS'))],
        [sg.pin(sg.Frame('flag test', iracing_color_test_frame_layout, font=('Helvetica', 10), title_color='#ffffff',
                  visible=HUE_CONNECTION['sim'] == 'iRacing', key='FRAME_IRACING_FLAGS'))],
        [sg.Frame('live sync', sync_controls_frame_layout, font=('Helvetica', 10), title_color='#ffffff'),
         sg.Frame('sync status', sync_status_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Text(
            'If you are connecting this app to your Bridge for the first time, you have to press the Pairing Button on your Bridge and then connect within 30 seconds.',
            size=(80, 2), text_color='#b71c1c', key='MSG_30_SECONDS', visible=show_30_seconds_info)],
    ]

    window = sg.Window('phue-racing-flags', layout, font='Helvetica', finalize=True)

    while True:
        event, values = window.read()

        if event == 'BTN_BRIDGE':
            HUE_CONNECTION['ip'] = values['INPUT_IP']
            window['MENU_LIGHT'].update([])
            if (bridge_connection_works()):
                save_hue_connection_to_file()
                bridge = Bridge(HUE_CONNECTION['ip'])
                enable_interface(bridge, window)
            else:
                disable_interface(window)

        if event == 'MENU_LIGHT':
            HUE_CONNECTION['lights'] = values['MENU_LIGHT']
            save_hue_connection_to_file()

        if event == 'SLIDER_BRIGHTNESS':
            HUE_CONNECTION['brightness'] = values['SLIDER_BRIGHTNESS']
            save_hue_connection_to_file()

        if event == 'SIM_SELECT_ACC':
            stop_sync()
            HUE_CONNECTION['sim'] = 'ACC'
            window['FRAME_ACC_FLAGS'].update(visible=True)
            window['FRAME_IRACING_FLAGS'].update(visible=False)
            save_hue_connection_to_file()

        if event == 'SIM_SELECT_IRACING':
            stop_sync()
            HUE_CONNECTION['sim'] = 'iRacing'
            window['FRAME_ACC_FLAGS'].update(visible=False)
            window['FRAME_IRACING_FLAGS'].update(visible=True)
            save_hue_connection_to_file()

        # ACC Flag Buttons

        if event == 'BTN_ACC_NO_FLAG':
            raise_acc_flag(acc.ACCFlagType.ACC_NO_FLAG, bridge, window)

        if event == 'BTN_ACC_BLUE_FLAG':
            raise_acc_flag(acc.ACCFlagType.ACC_BLUE_FLAG, bridge, window)

        if event == 'BTN_ACC_YELLOW_FLAG':
            raise_acc_flag(acc.ACCFlagType.ACC_YELLOW_FLAG, bridge, window)

        if event == 'BTN_ACC_BLACK_FLAG':
            raise_acc_flag(acc.ACCFlagType.ACC_BLACK_FLAG, bridge, window)

        if event == 'BTN_ACC_WHITE_FLAG':
            raise_acc_flag(acc.ACCFlagType.ACC_WHITE_FLAG, bridge, window)

        if event == 'BTN_ACC_CHECKERED_FLAG':
            raise_acc_flag(acc.ACCFlagType.ACC_CHECKERED_FLAG, bridge, window)

        if event == 'BTN_ACC_PENALTY_FLAG':
            raise_acc_flag(acc.ACCFlagType.ACC_PENALTY_FLAG, bridge, window)

        if event == 'BTN_ACC_GREEN_FLAG':
            raise_acc_flag(acc.ACCFlagType.ACC_GREEN_FLAG, bridge, window)

        if event == 'BTN_ACC_ORANGE_FLAG':
            raise_acc_flag(acc.ACCFlagType.ACC_ORANGE_FLAG, bridge, window)

        # iRacing Flag Buttons

        if event == 'BTN_IRACING_NO_FLAG':
            raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_NO_FLAG, bridge, window)

        if event == 'BTN_IRACING_BLUE_FLAG':
            raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_BLUE_FLAG, bridge, window)

        if event == 'BTN_IRACING_YELLOW_FLAG':
            raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_YELLOW_FLAG, bridge, window)

        if event == 'BTN_IRACING_BLACK_FLAG':
            raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_BLACK_FLAG, bridge, window)

        if event == 'BTN_IRACING_WHITE_FLAG':
            raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_WHITE_FLAG, bridge, window)

        if event == 'BTN_IRACING_CHEQUERED_FLAG':
            raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_CHEQUERED_FLAG, bridge, window)

        if event == 'BTN_IRACING_RED_FLAG':
            raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_RED_FLAG, bridge, window)

        if event == 'BTN_IRACING_GREEN_FLAG':
            raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_GREEN_FLAG, bridge, window)

        if event == 'BTN_IRACING_MEATBALL_FLAG':
            raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_MEATBALL_FLAG, bridge, window)

        if event == 'BTN_SYNC_START':
            window['MSG_SYNC_STATUS'].update('Running.')
            thread = threading.Thread(target=start_sync, args=(bridge, window,))
            thread.start()

        if event == 'BTN_SYNC_STOP':
            stop_sync()

        if event == sg.WINDOW_CLOSED:
            stop_sync()
            window.close()
            break


def enable_interface(bridge: Bridge, window: sg.Window):
    window['MSG_BRIDGE'].update('Connection established.')
    window['MENU_LIGHT'].update(disabled=False)

    # ACC Flag Buttons
    window['BTN_ACC_NO_FLAG'].update(disabled=False)
    window['BTN_ACC_BLUE_FLAG'].update(disabled=False)
    window['BTN_ACC_YELLOW_FLAG'].update(disabled=False)
    window['BTN_ACC_BLACK_FLAG'].update(disabled=False)
    window['BTN_ACC_WHITE_FLAG'].update(disabled=False)
    window['BTN_ACC_CHECKERED_FLAG'].update(disabled=False)
    window['BTN_ACC_PENALTY_FLAG'].update(disabled=False)
    window['BTN_ACC_GREEN_FLAG'].update(disabled=False)
    window['BTN_ACC_ORANGE_FLAG'].update(disabled=False)

    # iRacing Flag Buttons
    window['BTN_IRACING_NO_FLAG'].update(disabled=False)
    window['BTN_IRACING_BLUE_FLAG'].update(disabled=False)
    window['BTN_IRACING_YELLOW_FLAG'].update(disabled=False)
    window['BTN_IRACING_BLACK_FLAG'].update(disabled=False)
    window['BTN_IRACING_WHITE_FLAG'].update(disabled=False)
    window['BTN_IRACING_CHEQUERED_FLAG'].update(disabled=False)
    window['BTN_IRACING_RED_FLAG'].update(disabled=False)
    window['BTN_IRACING_GREEN_FLAG'].update(disabled=False)
    window['BTN_IRACING_MEATBALL_FLAG'].update(disabled=False)

    window['BTN_SYNC_START'].update(disabled=False)
    window['BTN_SYNC_STOP'].update(disabled=False)
    window['SIM_SELECT_ACC'].update(disabled=False)
    window['SIM_SELECT_IRACING'].update(disabled=False)
    window['MENU_LIGHT'].update(values=get_lights_from_bridge(bridge))
    window['MSG_30_SECONDS'].update(visible=False)


def disable_interface(window: sg.Window):
    window['MSG_BRIDGE'].update('Connection failed.')
    window['MENU_LIGHT'].update(disabled=True)

    # ACC Flag Buttons
    window['BTN_ACC_NO_FLAG'].update(disabled=True)
    window['BTN_ACC_BLUE_FLAG'].update(disabled=True)
    window['BTN_ACC_YELLOW_FLAG'].update(disabled=True)
    window['BTN_ACC_BLACK_FLAG'].update(disabled=True)
    window['BTN_ACC_WHITE_FLAG'].update(disabled=True)
    window['BTN_ACC_CHECKERED_FLAG'].update(disabled=True)
    window['BTN_ACC_CHECKERED_FLAG'].update(disabled=True)
    window['BTN_ACC_PENALTY_FLAG'].update(disabled=True)
    window['BTN_ACC_GREEN_FLAG'].update(disabled=True)
    window['BTN_ACC_ORANGE_FLAG'].update(disabled=True)

    # iRacing Flag Buttons
    window['BTN_IRACING_NO_FLAG'].update(disabled=True)
    window['BTN_IRACING_BLUE_FLAG'].update(disabled=True)
    window['BTN_IRACING_YELLOW_FLAG'].update(disabled=True)
    window['BTN_IRACING_BLACK_FLAG'].update(disabled=True)
    window['BTN_IRACING_WHITE_FLAG'].update(disabled=True)
    window['BTN_IRACING_CHEQUERED_FLAG'].update(disabled=True)
    window['BTN_IRACING_RED_FLAG'].update(disabled=True)
    window['BTN_IRACING_GREEN_FLAG'].update(disabled=True)
    window['BTN_IRACING_MEATBALL_FLAG'].update(disabled=True)

    window['BTN_SYNC_START'].update(disabled=True)
    window['BTN_SYNC_STOP'].update(disabled=True)
    window['SIM_SELECT_ACC'].update(disabled=True)
    window['SIM_SELECT_IRACING'].update(disabled=True)
    window['MENU_LIGHT'].update(values=[])
    window['MSG_30_SECONDS'].update(visible=True)


def load_hue_connection_from_file():
    try:
        save_file = open(SAVE_FILE_PATH, 'r')
        data = json.load(save_file)
        HUE_CONNECTION['ip'] = data['ip']
        HUE_CONNECTION['lights'] = data['lights']
        HUE_CONNECTION['brightness'] = data['brightness']
        HUE_CONNECTION['sim'] = data['sim'] or 'ACC'
    except (FileNotFoundError, KeyError) as error:
        print(error)
        HUE_CONNECTION['ip'] = ''
        HUE_CONNECTION['lights'] = ''
        HUE_CONNECTION['brightness'] = 255
        HUE_CONNECTION['sim'] = 'ACC'


def save_hue_connection_to_file():
    save_file = open(SAVE_FILE_PATH, 'w')
    json.dump(HUE_CONNECTION, save_file)


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


def sync_acc_color(bridge: Bridge, window: sg.Window):
    global HUE_CONNECTION
    flag = acc.get_flag()
    raise_acc_flag(flag, bridge, window)


def sync_iracing_color(bridge: Bridge, window: sg.Window):
    global HUE_CONNECTION
    flag = iracing.get_flag()
    raise_iracing_flag(flag, bridge, window)


def raise_acc_flag(flag: acc.ACCFlagType, bridge: Bridge, window: sg.Window):
    if flag == acc.ACCFlagType.ACC_NO_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': False})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_NO_FLAG)
    if flag == acc.ACCFlagType.ACC_BLUE_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_BLUE_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_BLUE_FLAG)
    if flag == acc.ACCFlagType.ACC_YELLOW_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_YELLOW_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_YELLOW_FLAG)
    if flag == acc.ACCFlagType.ACC_BLACK_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': False})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_BLACK_FLAG)
    if flag == acc.ACCFlagType.ACC_WHITE_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_WHITE_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_WHITE_FLAG)
    if flag == acc.ACCFlagType.ACC_CHECKERED_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': False})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_CHECKERED_FLAG)
    if flag == acc.ACCFlagType.ACC_PENALTY_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_PENALTY_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_PENALTY_FLAG)
    if flag == acc.ACCFlagType.ACC_GREEN_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_GREEN_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_GREEN_FLAG)
    if flag == acc.ACCFlagType.ACC_ORANGE_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_ORANGE_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_ORANGE_FLAG)


def raise_iracing_flag(flag: iracing.IRacingGUIFlagType, bridge: Bridge, window: sg.Window):
    if flag == iracing.IRacingGUIFlagType.IRACING_NO_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': False})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_NO_FLAG)
    if flag == iracing.IRacingGUIFlagType.IRACING_BLUE_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_BLUE_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_BLUE_FLAG)
    if flag == iracing.IRacingGUIFlagType.IRACING_YELLOW_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_YELLOW_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_YELLOW_FLAG)
    if flag == iracing.IRacingGUIFlagType.IRACING_BLACK_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': False})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_BLACK_FLAG)
    if flag == iracing.IRacingGUIFlagType.IRACING_WHITE_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_WHITE_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_WHITE_FLAG)
    if flag == iracing.IRacingGUIFlagType.IRACING_CHEQUERED_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': False})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_CHECKERED_FLAG)
    if flag == iracing.IRacingGUIFlagType.IRACING_RED_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_PENALTY_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_PENALTY_FLAG)
    if flag == iracing.IRacingGUIFlagType.IRACING_GREEN_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_GREEN_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_GREEN_FLAG)
    if flag == iracing.IRacingGUIFlagType.IRACING_MEATBALL_FLAG:
        for light in HUE_CONNECTION['lights']:
            bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                     'xy': HUE_COLOR_ORANGE_FLAG})
        window['CANVAS_FLAG'].update(background_color=GUI_COLOR_ORANGE_FLAG)


def start_sync(bridge: Bridge, window: sg.Window):
    global STOP_SYNC
    if STOP_SYNC:
        STOP_SYNC = False
        while True:
            if HUE_CONNECTION['sim'] == 'ACC':
                sync_acc_color(bridge, window)
                time.sleep(0.1)

            if HUE_CONNECTION['sim'] == 'iRacing':
                sync_iracing_color(bridge, window)
                time.sleep(0.1)

            if STOP_SYNC:
                window['MSG_SYNC_STATUS'].update('Stopped.')
                break


def stop_sync():
    global STOP_SYNC
    STOP_SYNC = True


open_window()
