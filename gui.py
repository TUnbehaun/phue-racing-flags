import external.PySimpleGUI as sg
from external.phue import Bridge
import threading
import json
import acc
import time

SAVE_FILE_PATH = './sf.json'
HUE_CONNECTION = {
    'ip': '',
    'light': '',
    'brightness': 255
}
sg.theme('Black')
STOP_SYNC: bool


def open_window():
    global HUE_CONNECTION
    disable_lights_menu = True
    msg_bridge = ''
    bridge: Bridge
    light_options = []
    show_30_seconds_info = False
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

    flag_frame_layout = [
        [sg.Graph(canvas_size=(895, 100), graph_bottom_left=(0, 0), graph_top_right=(895, 100), background_color='#000000', key='CANVAS_FLAG')]
    ]

    bridge_ip_frame_layout = [
        [sg.Input(key='INPUT_IP', default_text=HUE_CONNECTION['ip'], font=('Helvetica', 24), size=(15, 1)), sg.Button('Connect', key='BTN_BRIDGE', font=('Helvetica', 24))]
    ]

    bridge_status_frame_layout = [
        [sg.Text(size=(23, 1), key='MSG_BRIDGE', text=msg_bridge, font=('Helvetica', 24))]
    ]

    light_menu_frame_layout = [
        [sg.Combo(values=light_options, key='MENU_LIGHT', disabled=disable_lights_menu, default_value=HUE_CONNECTION['light'], enable_events=True, font=('Helvetica', 24))]
    ]

    brightness_menu_frame_layout = [
        [sg.Slider(range=(1, 255), default_value=int(HUE_CONNECTION['brightness']), size=(20, 20), orientation='horizontal', font=('Helvetica', 24), enable_events=True, key='SLIDER_BRIGHTNESS')]
    ]

    color_test_frame_layout = [
        [sg.Button('No Flag', key='BTN_NO_FLAG', button_color=('#ffffff', '#000000'), disabled=disable_lights_menu, font=('Helvetica', 24)), sg.Button('Blue Flag', key='BTN_BLUE_FLAG', button_color=('#ffffff', '#0D47A1'), disabled=disable_lights_menu, font=('Helvetica', 24)), sg.Button('Yellow Flag', key='BTN_YELLOW_FLAG', button_color=('#000000', '#FFEB3B'), disabled=disable_lights_menu, font=('Helvetica', 24)), sg.Button('Black Flag', key='BTN_BLACK_FLAG', button_color=('#ffffff', '#000000'), disabled=disable_lights_menu, font=('Helvetica', 24)), sg.Button('White Flag', key='BTN_WHITE_FLAG', button_color=('#000000', '#ffffff'), disabled=disable_lights_menu, font=('Helvetica', 24))],
        [sg.Button('Checkered Flag', key='BTN_CHECKERED_FLAG', button_color=('#ffffff', '#000000'), disabled=disable_lights_menu, font=('Helvetica', 24)), sg.Button('Penalty Flag', key='BTN_PENALTY_FLAG', button_color=('#ffffff', '#b71c1c'), disabled=disable_lights_menu, font=('Helvetica', 24)), sg.Button('Green Flag', key='BTN_GREEN_FLAG', button_color=('#ffffff', '#388E3C'), disabled=disable_lights_menu, font=('Helvetica', 24)), sg.Button('Orange Flag', key='BTN_ORANGE_FLAG', button_color=('#ffffff', '#FF6F00'), disabled=disable_lights_menu, font=('Helvetica', 24))]
    ]

    acc_status_frame_layout = [
        [sg.Text(size=(30, 1), key='MSG_ACC_SYNC_STATUS', text='Stopped.', font=('Helvetica', 24))]
    ]

    acc_controls_frame_layout = [
        [sg.Button('Start', key='BTN_ACC_START', disabled=disable_lights_menu, font=('Helvetica', 24)),
         sg.Button('Stop', key='BTN_ACC_STOP', disabled=disable_lights_menu, font=('Helvetica', 24))]
    ]

    layout = [
        [sg.Frame('flag', flag_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Frame('bridge ip', bridge_ip_frame_layout, font=('Helvetica', 10), title_color='#ffffff'), sg.Frame('bridge status', bridge_status_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Frame('light', light_menu_frame_layout, font=('Helvetica', 10), title_color='#ffffff'), sg.Frame('brightness', brightness_menu_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Frame('flag test', color_test_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Frame('acc sync', acc_controls_frame_layout, font=('Helvetica', 10), title_color='#ffffff'), sg.Frame('sync status', acc_status_frame_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Text('If you are connecting this app to your Bridge for the first time, you have to press the Pairing Button on your Bridge and then connect within 30 seconds.', size=(80, 2), text_color='#b71c1c', key='MSG_30_SECONDS', visible=show_30_seconds_info)],
    ]

    window = sg.Window('Philips Hue Racing Flags for ACC', layout, font='Helvetica', finalize=True)

    while True:
        event, values = window.read()

        if event == 'BTN_BRIDGE':
            HUE_CONNECTION['ip'] = values['INPUT_IP']
            window['MENU_LIGHT'].update('')
            if (bridge_connection_works()):
                save_hue_connection_to_file()
                bridge = Bridge(HUE_CONNECTION['ip'])
                window['MSG_BRIDGE'].update('Connection established.')
                window['MENU_LIGHT'].update(disabled=False)
                window['BTN_NO_FLAG'].update(disabled=False)
                window['BTN_BLUE_FLAG'].update(disabled=False)
                window['BTN_YELLOW_FLAG'].update(disabled=False)
                window['BTN_BLACK_FLAG'].update(disabled=False)
                window['BTN_WHITE_FLAG'].update(disabled=False)
                window['BTN_CHECKERED_FLAG'].update(disabled=False)
                window['BTN_CHECKERED_FLAG'].update(disabled=False)
                window['BTN_PENALTY_FLAG'].update(disabled=False)
                window['BTN_GREEN_FLAG'].update(disabled=False)
                window['BTN_ORANGE_FLAG'].update(disabled=False)
                window['BTN_ACC_START'].update(disabled=False)
                window['BTN_ACC_STOP'].update(disabled=False)
                window['MENU_LIGHT'].update(values=get_lights_from_bridge(bridge))
                window['MSG_30_SECONDS'].update(visible=False)
            else:
                window['MSG_BRIDGE'].update('Connection failed.')
                window['MENU_LIGHT'].update(disabled=True)
                window['BTN_NO_FLAG'].update(disabled=True)
                window['BTN_BLUE_FLAG'].update(disabled=True)
                window['BTN_YELLOW_FLAG'].update(disabled=True)
                window['BTN_BLACK_FLAG'].update(disabled=True)
                window['BTN_WHITE_FLAG'].update(disabled=True)
                window['BTN_CHECKERED_FLAG'].update(disabled=True)
                window['BTN_CHECKERED_FLAG'].update(disabled=True)
                window['BTN_PENALTY_FLAG'].update(disabled=True)
                window['BTN_GREEN_FLAG'].update(disabled=True)
                window['BTN_ORANGE_FLAG'].update(disabled=True)
                window['BTN_ACC_START'].update(disabled=True)
                window['BTN_ACC_STOP'].update(disabled=True)
                window['MENU_LIGHT'].update(values=[])
                window['MSG_30_SECONDS'].update(visible=True)

        if event == 'MENU_LIGHT':
            HUE_CONNECTION['light'] = values['MENU_LIGHT']
            save_hue_connection_to_file()

        if event == 'SLIDER_BRIGHTNESS':
            HUE_CONNECTION['brightness'] = values['SLIDER_BRIGHTNESS']
            save_hue_connection_to_file()

        if event == 'BTN_NO_FLAG':
            bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': False})
            window['CANVAS_FLAG'].update(background_color='#000000')

        if event == 'BTN_BLUE_FLAG':
            bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.1532, 0.0475]})
            window['CANVAS_FLAG'].update(background_color='#0D47A1')

        if event == 'BTN_YELLOW_FLAG':
            bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.4787, 0.4681]})
            window['CANVAS_FLAG'].update(background_color='#FFEB3B')

        if event == 'BTN_BLACK_FLAG':
            bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': False})
            window['CANVAS_FLAG'].update(background_color='#000000')

        if event == 'BTN_WHITE_FLAG':
            bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.3089, 0.3269]})
            window['CANVAS_FLAG'].update(background_color='#ffffff')

        if event == 'BTN_CHECKERED_FLAG':
            bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': False})
            window['CANVAS_FLAG'].update(background_color='#000000')

        if event == 'BTN_PENALTY_FLAG':
            bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.6897, 0.3074]})
            window['CANVAS_FLAG'].update(background_color='#b71c1c')

        if event == 'BTN_GREEN_FLAG':
            bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.17, 0.7]})
            window['CANVAS_FLAG'].update(background_color='#388E3C')

        if event == 'BTN_ORANGE_FLAG':
            bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.633, 0.3522]})
            window['CANVAS_FLAG'].update(background_color='#FF6F00')

        if event == 'BTN_ACC_START':
            window['MSG_ACC_SYNC_STATUS'].update('Running.')
            thread = threading.Thread(target=start_acc_sync, args=(bridge, window,))
            thread.start()

        if event == 'BTN_ACC_STOP':
            window['MSG_ACC_SYNC_STATUS'].update('Stopped.')
            stop_acc_sync()

        if event == sg.WINDOW_CLOSED:
            stop_acc_sync()
            window.close()
            break


def load_hue_connection_from_file():
    try:
        save_file = open(SAVE_FILE_PATH, 'r')
        data = json.load(save_file)
        HUE_CONNECTION['ip'] = data['ip']
        HUE_CONNECTION['light'] = data['light']
        HUE_CONNECTION['brightness'] = data['brightness']
    except FileNotFoundError as error:
        print(error)
        HUE_CONNECTION['ip'] = ''
        HUE_CONNECTION['light'] = ''
        HUE_CONNECTION['brightness'] = 255


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


def sync_color(bridge: Bridge, window):
    global HUE_CONNECTION
    flag = acc.get_flag()
    if flag == acc.ACCFlagType.ACC_NO_FLAG:
        bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': False})
        window['CANVAS_FLAG'].update(background_color='#000000')
    if flag == acc.ACCFlagType.ACC_BLUE_FLAG:
        bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.1532, 0.0475]})
        window['CANVAS_FLAG'].update(background_color='#0D47A1')
    if flag == acc.ACCFlagType.ACC_YELLOW_FLAG:
        bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.4787, 0.4681]})
        window['CANVAS_FLAG'].update(background_color='#FFEB3B')
    if flag == acc.ACCFlagType.ACC_BLACK_FLAG:
        bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': False})
        window['CANVAS_FLAG'].update(background_color='#000000')
    if flag == acc.ACCFlagType.ACC_WHITE_FLAG:
        bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.3089, 0.3269]})
        window['CANVAS_FLAG'].update(background_color='#ffffff')
    if flag == acc.ACCFlagType.ACC_CHECKERED_FLAG:
        bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': False})
        window['CANVAS_FLAG'].update(background_color='#000000')
    if flag == acc.ACCFlagType.ACC_PENALTY_FLAG:
        bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.6897, 0.3074]})
        window['CANVAS_FLAG'].update(background_color='#b71c1c')
    if flag == acc.ACCFlagType.ACC_GREEN_FLAG:
        bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.17, 0.7]})
        window['CANVAS_FLAG'].update(background_color='#388E3C')
    if flag == acc.ACCFlagType.ACC_ORANGE_FLAG:
        bridge.set_light(HUE_CONNECTION['light'], {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']), 'xy': [0.633, 0.3522]})
        window['CANVAS_FLAG'].update(background_color='#FF6F00')


def start_acc_sync(bridge: Bridge, window):
    global STOP_SYNC
    STOP_SYNC = False
    while True:
        sync_color(bridge, window)
        time.sleep(0.1)

        if STOP_SYNC:
            break


def stop_acc_sync():
    global STOP_SYNC
    STOP_SYNC = True


open_window()
