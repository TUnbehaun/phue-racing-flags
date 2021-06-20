import external.PySimpleGUI as sg
from external.phue import Bridge
from external.modified.rgbxy import Converter
from data import images
import sims.acc as acc
import sims.iracing as iracing
import sims.ac as ac
import threading
import json
import time

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

# Global Variables
SAVE_FILE_PATH = './phue-rf-save.json'
HUE_CONNECTION = {
    'ip': '',
    'lights': [],
    'brightness': 255,
    'sim': 'AC',
    'colors': {
        'AC': {
            'No_Flag': '',
            'Blue_Flag': GUI_COLOR_BLUE_FLAG,
            'Yellow_Flag': GUI_COLOR_YELLOW_FLAG,
            'Black_Flag': '',
            'White_Flag': GUI_COLOR_WHITE_FLAG,
            'Checkered_Flag': '',
            'Penalty_Flag': GUI_COLOR_PENALTY_FLAG
        },
        'ACC': {
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
        'iRacing': {
            'No_Flag': '',
            'Blue_Flag': GUI_COLOR_BLUE_FLAG,
            'Yellow_Flag': GUI_COLOR_YELLOW_FLAG,
            'Black_Flag': '',
            'White_Flag': GUI_COLOR_WHITE_FLAG,
            'Checkered_Flag': '',
            'Red_Flag': GUI_COLOR_PENALTY_FLAG,
            'Green_Flag': GUI_COLOR_GREEN_FLAG,
            'Meatball_Flag': GUI_COLOR_ORANGE_FLAG
        }
    },
    'auto_sync': False
}
STOP_SYNC = True


def open_window():
    global HUE_CONNECTION

    converter = Converter()

    disable_due_to_failed_connection = True
    show_30_seconds_info = False
    msg_bridge = ''

    bridge: Bridge
    light_options = []

    show_settings = False

    load_hue_connection_from_file()

    if bridge_connection_works():
        disable_due_to_failed_connection = False
        msg_bridge = 'Connection established.'
        bridge = Bridge(HUE_CONNECTION['ip'])
        light_options = get_lights_from_bridge(bridge)
        show_30_seconds_info = False
    else:
        disable_due_to_failed_connection = True
        msg_bridge = 'Connection failed.'
        show_30_seconds_info = True

    # GUI Frames

    flag_frame_layout = [
        [sg.Graph(canvas_size=(870, 100), graph_bottom_left=(0, 0), graph_top_right=(870, 100),
                  background_color=GUI_COLOR_NO_FLAG, key='CANVAS_FLAG')]
    ]

    bridge_status_frame_layout = [
        [sg.Text('Bridge status:', size=(10, 1), font=('Helvetica', 24)),
         sg.Text(size=(22, 1), key='MSG_BRIDGE', text=msg_bridge, font=('Helvetica', 24)),
         sg.Button('Open Settings', key='BTN_OPEN_SETTINGS', font=('Helvetica', 24))]
    ]

    sim_select_frame_layout = [
        [sg.Radio('Assetto Corsa', 'SIM_SELECT', font=('Helvetica', 24), disabled=disable_due_to_failed_connection,
                  key='SIM_SELECT_AC', enable_events=True, default=HUE_CONNECTION['sim'] == 'AC'),
         sg.Radio('Assetto Corsa Competizione', 'SIM_SELECT', font=('Helvetica', 24),
                  disabled=disable_due_to_failed_connection,
                  key='SIM_SELECT_ACC', enable_events=True, default=HUE_CONNECTION['sim'] == 'ACC'),
         sg.Radio('iRacing', 'SIM_SELECT', font=('Helvetica', 24), size=(8, 1),
                  disabled=disable_due_to_failed_connection,
                  key='SIM_SELECT_IRACING', enable_events=True, default=HUE_CONNECTION['sim'] == 'iRacing')]
    ]

    sync_controls_frame_layout = [
        [sg.Button('Start', key='BTN_SYNC_START', disabled=disable_due_to_failed_connection, font=('Helvetica', 24)),
         sg.Button('Stop', key='BTN_SYNC_STOP', disabled=disable_due_to_failed_connection, font=('Helvetica', 24))]
    ]

    sync_status_frame_layout = [
        [sg.Text(size=(34, 1), key='MSG_SYNC_STATUS', text='Stopped.', font=('Helvetica', 24))]
    ]

    frame_general_bridge_layout = [
        [sg.Text('Bridge IP:', size=(15, 1)), sg.Input(key='INPUT_IP', default_text=HUE_CONNECTION['ip'], size=(15, 1)),
         sg.Button('Connect', key='BTN_BRIDGE')]
    ]

    frame_general_lights_layout = [
        [sg.Text('Lights to use:', size=(15, 1)),
         sg.Listbox(values=light_options, key='MENU_LIGHT', disabled=disable_due_to_failed_connection,
                    default_values=HUE_CONNECTION['lights'], enable_events=True,
                    select_mode='multiple', size=(20, 5))],
        [sg.Text('Brightness:', size=(15, 1)),
         sg.Slider(range=(1, 255), default_value=int(HUE_CONNECTION['brightness']),
                   orientation='horizontal', enable_events=True, key='SLIDER_BRIGHTNESS')]
    ]

    frame_general_sync_layout = [
        [sg.Checkbox('Start live sync on app startup', default=HUE_CONNECTION['auto_sync'], key='CHECKBOX_AUTO_SYNC',
                     enable_events=True)]
    ]

    tab_general_layout = [
        [sg.Frame('bridge', frame_general_bridge_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Frame('lights', frame_general_lights_layout, font=('Helvetica', 10), title_color='#ffffff')],
        [sg.Frame('live sync', frame_general_sync_layout, font=('Helvetica', 10), title_color='#ffffff')]
    ]

    assetto_corsa_flags = [
        'No Flag',
        'Blue Flag',
        'Yellow Flag',
        'Black Flag',
        'White Flag',
        'Checkered Flag',
        'Penalty Flag'
    ]

    frame_assetto_corsa_flags_layout = [
        [sg.Text(flag + ':', size=(15, 1)),
         sg.Graph(canvas_size=(25, 25), graph_bottom_left=(0, 0), graph_top_right=(25, 25),
                  background_color=HUE_CONNECTION['colors']['AC'][flag.replace(' ', '_')] or '#000000',
                  key='CANVAS_ASSETTO_CORSA_' + flag.replace(' ', '_')),
         sg.Button('Pick Color', button_type=sg.BUTTON_TYPE_COLOR_CHOOSER,
                   target='INPUT_COLOR_ASSETTO_CORSA_' + flag.replace(' ', '_')),
         sg.Button('Set to off', key='BTN_SET_TO_OFF_ASSETTO_CORSA_' + flag.replace(' ', '_')),
         sg.Button('Test', key='BTN_TEST_ASSETTO_CORSA_' + flag.replace(' ', '_')),
         sg.Input(key='INPUT_COLOR_ASSETTO_CORSA_' + flag.replace(' ', '_'), enable_events=True, visible=False)]
        for flag in assetto_corsa_flags
    ]

    tab_assetto_corsa_layout = [
        [sg.Frame('flags', frame_assetto_corsa_flags_layout, font=('Helvetica', 10), title_color='#ffffff')]
    ]

    assetto_corsa_competizione_flags = [
        'No Flag',
        'Blue Flag',
        'Yellow Flag',
        'Black Flag',
        'White Flag',
        'Checkered Flag',
        'Penalty Flag',
        'Green Flag',
        'Orange Flag'
    ]

    frame_assetto_corsa_competizione_flags_layout = [
        [sg.Text(flag + ':', size=(15, 1)),
         sg.Graph(canvas_size=(25, 25), graph_bottom_left=(0, 0), graph_top_right=(25, 25),
                  background_color=HUE_CONNECTION['colors']['ACC'][flag.replace(' ', '_')] or '#000000',
                  key='CANVAS_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_')),
         sg.Button('Pick Color', button_type=sg.BUTTON_TYPE_COLOR_CHOOSER,
                   target='INPUT_COLOR_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_')),
         sg.Button('Set to off', key='BTN_SET_TO_OFF_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_')),
         sg.Button('Test', key='BTN_TEST_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_')),
         sg.Input(key='INPUT_COLOR_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_'), enable_events=True,
                  visible=False)]
        for flag in assetto_corsa_competizione_flags
    ]

    tab_assetto_corsa_competizione_layout = [
        [sg.Frame('flags', frame_assetto_corsa_competizione_flags_layout, font=('Helvetica', 10),
                  title_color='#ffffff')]
    ]

    iracing_flags = [
        'No Flag',
        'Blue Flag',
        'Yellow Flag',
        'Black Flag',
        'White Flag',
        'Checkered Flag',
        'Red Flag',
        'Green Flag',
        'Meatball Flag'
    ]

    frame_iracing_flags_layout = [
        [sg.Text(flag + ':', size=(15, 1)),
         sg.Graph(canvas_size=(25, 25), graph_bottom_left=(0, 0), graph_top_right=(25, 25),
                  background_color=HUE_CONNECTION['colors']['iRacing'][flag.replace(' ', '_')] or '#000000',
                  key='CANVAS_IRACING_' + flag.replace(' ', '_')),
         sg.Button('Pick Color', button_type=sg.BUTTON_TYPE_COLOR_CHOOSER,
                   target='INPUT_COLOR_IRACING_' + flag.replace(' ', '_')),
         sg.Button('Set to off', key='BTN_SET_TO_OFF_IRACING_' + flag.replace(' ', '_')),
         sg.Button('Test', key='BTN_TEST_IRACING_' + flag.replace(' ', '_')),
         sg.Input(key='INPUT_COLOR_IRACING_' + flag.replace(' ', '_'), enable_events=True,
                  visible=False)]
        for flag in iracing_flags
    ]

    tab_iracing_layout = [
        [sg.Frame('flags', frame_iracing_flags_layout, font=('Helvetica', 10), title_color='#ffffff')]
    ]

    frame_settings_layout = [
        [sg.TabGroup([[sg.Tab('General', tab_general_layout),
                       sg.Tab('Assetto Corsa', tab_assetto_corsa_layout, disabled=disable_due_to_failed_connection,
                              key='TAB_SETTINGS_ASSETTO_CORSA'),
                       sg.Tab('Assetto Corsa Competizione', tab_assetto_corsa_competizione_layout,
                              disabled=disable_due_to_failed_connection, key='TAB_SETTINGS_ASSETTO_CORSA_COMPETIZIONE'),
                       sg.Tab('iRacing', tab_iracing_layout, disabled=disable_due_to_failed_connection,
                              key='TAB_SETTINGS_IRACING')]])]
    ]

    # Window Layout

    layout = [
        [sg.pin(sg.Frame('general', bridge_status_frame_layout, font=('Helvetica', 10), title_color='#ffffff'))],
        [sg.pin(sg.Text(
            'Check Settings -> General -> Bridge IP\n\nIf you are connecting this app to your Bridge for the first time, you have to press the Pairing Button on your Bridge and then connect within 30 seconds.',
            size=(80, 4), text_color='#b71c1c', key='MSG_30_SECONDS',
            visible=show_30_seconds_info))],
        [sg.pin(sg.Frame('flag', flag_frame_layout, font=('Helvetica', 10), title_color='#ffffff'))],
        [sg.pin(sg.Frame('settings', frame_settings_layout, font=('Helvetica', 10), title_color='#ffffff',
                         visible=show_settings, key='FRAME_SETTINGS'))],
        [sg.pin(sg.Frame('sim', sim_select_frame_layout, font=('Helvetica', 10), title_color='#ffffff',
                         visible=(not show_settings), key='FRAME_SIM'))],
        [sg.pin(sg.Frame('live sync', sync_controls_frame_layout, font=('Helvetica', 10), title_color='#ffffff',
                         visible=(not show_settings), key='FRAME_SYNC_CONTROLS')),
         sg.pin(sg.Frame('sync status', sync_status_frame_layout, font=('Helvetica', 10), title_color='#ffffff',
                         visible=(not show_settings), key='FRAME_SYNC_STATUS'))]
    ]

    window = sg.Window('phue-racing-flags', layout, icon=images, font='Helvetica', finalize=True)

    if bridge_connection_works() and HUE_CONNECTION['auto_sync'] is True:
        if len(HUE_CONNECTION['lights']) == 0:
            show_error_window('No lights selected. Select lights under Settings -> General - Lights')
        else:
            window['MSG_SYNC_STATUS'].update('Running.')
            thread = threading.Thread(target=start_sync, args=(bridge, window,))
            thread.start()

    while True:
        event, values = window.read()

        # Main View

        if event == 'SIM_SELECT_AC':
            stop_sync()
            HUE_CONNECTION['sim'] = 'AC'
            save_hue_connection_to_file()

        if event == 'SIM_SELECT_ACC':
            stop_sync()
            HUE_CONNECTION['sim'] = 'ACC'
            save_hue_connection_to_file()

        if event == 'SIM_SELECT_IRACING':
            stop_sync()
            HUE_CONNECTION['sim'] = 'iRacing'
            save_hue_connection_to_file()

        if event == 'BTN_SYNC_START':
            if len(HUE_CONNECTION['lights']) == 0:
                show_error_window('No lights selected. Select lights under Settings -> General - Lights')
            else:
                window['MSG_SYNC_STATUS'].update('Running.')
                thread = threading.Thread(target=start_sync, args=(bridge, window,))
                thread.start()

        if event == 'BTN_SYNC_STOP':
            stop_sync()

        if event == 'BTN_OPEN_SETTINGS':
            show_settings = not show_settings
            window['FRAME_SETTINGS'].update(visible=show_settings)
            window['FRAME_SIM'].update(visible=(not show_settings))
            window['FRAME_SYNC_CONTROLS'].update(visible=(not show_settings))
            window['FRAME_SYNC_STATUS'].update(visible=(not show_settings))
            if show_settings:
                window['BTN_OPEN_SETTINGS'].update(text='Close Settings')
            else:
                window['BTN_OPEN_SETTINGS'].update(text='Open Settings')

        # General Settings

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

        if event == 'CHECKBOX_AUTO_SYNC':
            HUE_CONNECTION['auto_sync'] = values['CHECKBOX_AUTO_SYNC']
            save_hue_connection_to_file()

        # Assetto Corsa Settings

        for flag in assetto_corsa_flags:
            if event == 'BTN_TEST_ASSETTO_CORSA_' + flag.replace(' ', '_'):
                if flag == 'No Flag':
                    raise_ac_flag(ac.ACFlagType.AC_NO_FLAG, bridge, window)
                if flag == 'Blue Flag':
                    raise_ac_flag(ac.ACFlagType.AC_BLUE_FLAG, bridge, window)
                if flag == 'Yellow Flag':
                    raise_ac_flag(ac.ACFlagType.AC_YELLOW_FLAG, bridge, window)
                if flag == 'Black Flag':
                    raise_ac_flag(ac.ACFlagType.AC_BLACK_FLAG, bridge, window)
                if flag == 'White Flag':
                    raise_ac_flag(ac.ACFlagType.AC_WHITE_FLAG, bridge, window)
                if flag == 'Checkered Flag':
                    raise_ac_flag(ac.ACFlagType.AC_CHECKERED_FLAG, bridge, window)
                if flag == 'Penalty Flag':
                    raise_ac_flag(ac.ACFlagType.AC_PENALTY_FLAG, bridge, window)
            if event == 'BTN_SET_TO_OFF_ASSETTO_CORSA_' + flag.replace(' ', '_'):
                HUE_CONNECTION['colors']['AC'][flag.replace(' ', '_')] = ''
                window['CANVAS_ASSETTO_CORSA_' + flag.replace(' ', '_')].update(
                    background_color='#000000')
                save_hue_connection_to_file()
            if event == 'INPUT_COLOR_ASSETTO_CORSA_' + flag.replace(' ', '_') and values[
                'INPUT_COLOR_ASSETTO_CORSA_' + flag.replace(' ', '_')] != 'None':
                HUE_CONNECTION['colors']['AC'][flag.replace(' ', '_')] = values[
                    'INPUT_COLOR_ASSETTO_CORSA_' + flag.replace(' ', '_')]
                window['CANVAS_ASSETTO_CORSA_' + flag.replace(' ', '_')].update(
                    background_color=values['INPUT_COLOR_ASSETTO_CORSA_' + flag.replace(' ', '_')])
                save_hue_connection_to_file()

        # Assetto Corsa Competizione Settings

        for flag in assetto_corsa_competizione_flags:
            if event == 'BTN_TEST_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_'):
                if flag == 'No Flag':
                    raise_acc_flag(acc.ACCFlagType.ACC_NO_FLAG, bridge, window)
                if flag == 'Blue Flag':
                    raise_acc_flag(acc.ACCFlagType.ACC_BLUE_FLAG, bridge, window)
                if flag == 'Yellow Flag':
                    raise_acc_flag(acc.ACCFlagType.ACC_YELLOW_FLAG, bridge, window)
                if flag == 'Black Flag':
                    raise_acc_flag(acc.ACCFlagType.ACC_BLACK_FLAG, bridge, window)
                if flag == 'White Flag':
                    raise_acc_flag(acc.ACCFlagType.ACC_WHITE_FLAG, bridge, window)
                if flag == 'Checkered Flag':
                    raise_acc_flag(acc.ACCFlagType.ACC_CHECKERED_FLAG, bridge, window)
                if flag == 'Penalty Flag':
                    raise_acc_flag(acc.ACCFlagType.ACC_PENALTY_FLAG, bridge, window)
                if flag == 'Green Flag':
                    raise_acc_flag(acc.ACCFlagType.ACC_GREEN_FLAG, bridge, window)
                if flag == 'Orange Flag':
                    raise_acc_flag(acc.ACCFlagType.ACC_ORANGE_FLAG, bridge, window)
            if event == 'BTN_SET_TO_OFF_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_'):
                HUE_CONNECTION['colors']['ACC'][flag.replace(' ', '_')] = ''
                window['CANVAS_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_')].update(
                    background_color='#000000')
                save_hue_connection_to_file()
            if event == 'INPUT_COLOR_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_') and values[
                'INPUT_COLOR_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_')] != 'None':
                HUE_CONNECTION['colors']['ACC'][flag.replace(' ', '_')] = values[
                    'INPUT_COLOR_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_')]
                window['CANVAS_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_')].update(
                    background_color=values['INPUT_COLOR_ASSETTO_CORSA_COMPETIZIONE_' + flag.replace(' ', '_')])
                save_hue_connection_to_file()

        # iRacing Settings

        for flag in iracing_flags:
            if event == 'BTN_TEST_IRACING_' + flag.replace(' ', '_'):
                if flag == 'No Flag':
                    raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_NO_FLAG, bridge, window)
                if flag == 'Blue Flag':
                    raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_BLUE_FLAG, bridge, window)
                if flag == 'Yellow Flag':
                    raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_YELLOW_FLAG, bridge, window)
                if flag == 'Black Flag':
                    raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_BLACK_FLAG, bridge, window)
                if flag == 'White Flag':
                    raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_WHITE_FLAG, bridge, window)
                if flag == 'Checkered Flag':
                    raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_CHEQUERED_FLAG, bridge, window)
                if flag == 'Red Flag':
                    raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_RED_FLAG, bridge, window)
                if flag == 'Green Flag':
                    raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_GREEN_FLAG, bridge, window)
                if flag == 'Meatball Flag':
                    raise_iracing_flag(iracing.IRacingGUIFlagType.IRACING_MEATBALL_FLAG, bridge, window)
            if event == 'BTN_SET_TO_OFF_IRACING_' + flag.replace(' ', '_'):
                HUE_CONNECTION['colors']['iRacing'][flag.replace(' ', '_')] = ''
                window['CANVAS_IRACING_' + flag.replace(' ', '_')].update(
                    background_color='#000000')
                save_hue_connection_to_file()
            if event == 'INPUT_COLOR_IRACING_' + flag.replace(' ', '_') and values[
                'INPUT_COLOR_IRACING_' + flag.replace(' ', '_')] != 'None':
                HUE_CONNECTION['colors']['iRacing'][flag.replace(' ', '_')] = values[
                    'INPUT_COLOR_IRACING_' + flag.replace(' ', '_')]
                window['CANVAS_IRACING_' + flag.replace(' ', '_')].update(
                    background_color=values['INPUT_COLOR_IRACING_' + flag.replace(' ', '_')])
                save_hue_connection_to_file()

        if event == sg.WINDOW_CLOSED:
            stop_sync()
            window.close()
            break


def enable_interface(bridge: Bridge, window: sg.Window):
    window['MSG_BRIDGE'].update('Connection established.')
    window['MENU_LIGHT'].update(disabled=False)
    window['BTN_SYNC_START'].update(disabled=False)
    window['BTN_SYNC_STOP'].update(disabled=False)
    window['SIM_SELECT_AC'].update(disabled=False)
    window['SIM_SELECT_ACC'].update(disabled=False)
    window['SIM_SELECT_IRACING'].update(disabled=False)
    window['TAB_SETTINGS_ASSETTO_CORSA'].update(disabled=False)
    window['TAB_SETTINGS_ASSETTO_CORSA_COMPETIZIONE'].update(disabled=False)
    window['TAB_SETTINGS_IRACING'].update(disabled=False)
    window['MENU_LIGHT'].update(values=get_lights_from_bridge(bridge))
    window['MSG_30_SECONDS'].update(visible=False)


def disable_interface(window: sg.Window):
    window['MSG_BRIDGE'].update('Connection failed.')
    window['MENU_LIGHT'].update(disabled=True)
    window['BTN_SYNC_START'].update(disabled=True)
    window['BTN_SYNC_STOP'].update(disabled=True)
    window['SIM_SELECT_AC'].update(disabled=True)
    window['SIM_SELECT_ACC'].update(disabled=True)
    window['SIM_SELECT_IRACING'].update(disabled=True)
    window['TAB_SETTINGS_ASSETTO_CORSA'].update(disabled=True)
    window['TAB_SETTINGS_ASSETTO_CORSA_COMPETIZIONE'].update(disabled=True)
    window['TAB_SETTINGS_IRACING'].update(disabled=True)
    window['MENU_LIGHT'].update(values=[])
    window['MSG_30_SECONDS'].update(visible=True)


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
        HUE_CONNECTION['lights'] = ''
        HUE_CONNECTION['brightness'] = 255
        HUE_CONNECTION['sim'] = 'AC'
        HUE_CONNECTION['colors'] = {
            'AC': {
                'No_Flag': '',
                'Blue_Flag': GUI_COLOR_BLUE_FLAG,
                'Yellow_Flag': GUI_COLOR_YELLOW_FLAG,
                'Black_Flag': '',
                'White_Flag': GUI_COLOR_WHITE_FLAG,
                'Checkered_Flag': '',
                'Penalty_Flag': GUI_COLOR_PENALTY_FLAG
            },
            'ACC': {
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
            'iRacing': {
                'No_Flag': '',
                'Blue_Flag': GUI_COLOR_BLUE_FLAG,
                'Yellow_Flag': GUI_COLOR_YELLOW_FLAG,
                'Black_Flag': '',
                'White_Flag': GUI_COLOR_WHITE_FLAG,
                'Checkered_Flag': '',
                'Red_Flag': GUI_COLOR_PENALTY_FLAG,
                'Green_Flag': GUI_COLOR_GREEN_FLAG,
                'Meatball_Flag': GUI_COLOR_ORANGE_FLAG
            },
            'auto_sync': False
        }


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


def sync_ac_color(bridge: Bridge, window: sg.Window):
    global HUE_CONNECTION
    flag = ac.get_flag()
    raise_ac_flag(flag, bridge, window)


def sync_acc_color(bridge: Bridge, window: sg.Window):
    global HUE_CONNECTION
    flag = acc.get_flag()
    raise_acc_flag(flag, bridge, window)


def sync_iracing_color(bridge: Bridge, window: sg.Window):
    global HUE_CONNECTION
    flag = iracing.get_flag()
    raise_iracing_flag(flag, bridge, window)


def raise_ac_flag(flag: ac.ACFlagType, bridge: Bridge, window: sg.Window):
    if flag == ac.ACFlagType.AC_NO_FLAG:
        raise_color(HUE_CONNECTION['colors']['AC']['No_Flag'], bridge, window)
    if flag == ac.ACFlagType.AC_BLUE_FLAG:
        raise_color(HUE_CONNECTION['colors']['AC']['Blue_Flag'], bridge, window)
    if flag == ac.ACFlagType.AC_YELLOW_FLAG:
        raise_color(HUE_CONNECTION['colors']['AC']['Yellow_Flag'], bridge, window)
    if flag == ac.ACFlagType.AC_BLACK_FLAG:
        raise_color(HUE_CONNECTION['colors']['AC']['Black_Flag'], bridge, window)
    if flag == ac.ACFlagType.AC_WHITE_FLAG:
        raise_color(HUE_CONNECTION['colors']['AC']['White_Flag'], bridge, window)
    if flag == ac.ACFlagType.AC_CHECKERED_FLAG:
        raise_color(HUE_CONNECTION['colors']['AC']['Checkered_Flag'], bridge, window)
    if flag == ac.ACFlagType.AC_PENALTY_FLAG:
        raise_color(HUE_CONNECTION['colors']['AC']['Penalty_Flag'], bridge, window)


def raise_acc_flag(flag: acc.ACCFlagType, bridge: Bridge, window: sg.Window):
    if flag == acc.ACCFlagType.ACC_NO_FLAG:
        raise_color(HUE_CONNECTION['colors']['ACC']['No_Flag'], bridge, window)
    if flag == acc.ACCFlagType.ACC_BLUE_FLAG:
        raise_color(HUE_CONNECTION['colors']['ACC']['Blue_Flag'], bridge, window)
    if flag == acc.ACCFlagType.ACC_YELLOW_FLAG:
        raise_color(HUE_CONNECTION['colors']['ACC']['Yellow_Flag'], bridge, window)
    if flag == acc.ACCFlagType.ACC_BLACK_FLAG:
        raise_color(HUE_CONNECTION['colors']['ACC']['Black_Flag'], bridge, window)
    if flag == acc.ACCFlagType.ACC_WHITE_FLAG:
        raise_color(HUE_CONNECTION['colors']['ACC']['White_Flag'], bridge, window)
    if flag == acc.ACCFlagType.ACC_CHECKERED_FLAG:
        raise_color(HUE_CONNECTION['colors']['ACC']['Checkered_Flag'], bridge, window)
    if flag == acc.ACCFlagType.ACC_PENALTY_FLAG:
        raise_color(HUE_CONNECTION['colors']['ACC']['Penalty_Flag'], bridge, window)
    if flag == acc.ACCFlagType.ACC_GREEN_FLAG:
        raise_color(HUE_CONNECTION['colors']['ACC']['Green_Flag'], bridge, window)
    if flag == acc.ACCFlagType.ACC_ORANGE_FLAG:
        raise_color(HUE_CONNECTION['colors']['ACC']['Orange_Flag'], bridge, window)


def raise_iracing_flag(flag: iracing.IRacingGUIFlagType, bridge: Bridge, window: sg.Window):
    if flag == iracing.IRacingGUIFlagType.IRACING_NO_FLAG:
        raise_color(HUE_CONNECTION['colors']['iRacing']['No_Flag'], bridge, window)
    if flag == iracing.IRacingGUIFlagType.IRACING_BLUE_FLAG:
        raise_color(HUE_CONNECTION['colors']['iRacing']['Blue_Flag'], bridge, window)
    if flag == iracing.IRacingGUIFlagType.IRACING_YELLOW_FLAG:
        raise_color(HUE_CONNECTION['colors']['iRacing']['Yellow_Flag'], bridge, window)
    if flag == iracing.IRacingGUIFlagType.IRACING_BLACK_FLAG:
        raise_color(HUE_CONNECTION['colors']['iRacing']['Black_Flag'], bridge, window)
    if flag == iracing.IRacingGUIFlagType.IRACING_WHITE_FLAG:
        raise_color(HUE_CONNECTION['colors']['iRacing']['White_Flag'], bridge, window)
    if flag == iracing.IRacingGUIFlagType.IRACING_CHEQUERED_FLAG:
        raise_color(HUE_CONNECTION['colors']['iRacing']['Checkered_Flag'], bridge, window)
    if flag == iracing.IRacingGUIFlagType.IRACING_RED_FLAG:
        raise_color(HUE_CONNECTION['colors']['iRacing']['Red_Flag'], bridge, window)
    if flag == iracing.IRacingGUIFlagType.IRACING_GREEN_FLAG:
        raise_color(HUE_CONNECTION['colors']['iRacing']['Green_Flag'], bridge, window)
    if flag == iracing.IRacingGUIFlagType.IRACING_MEATBALL_FLAG:
        raise_color(HUE_CONNECTION['colors']['iRacing']['Meatball_Flag'], bridge, window)


def start_sync(bridge: Bridge, window: sg.Window):
    global STOP_SYNC
    if STOP_SYNC:
        STOP_SYNC = False
        while True:
            if HUE_CONNECTION['sim'] == 'AC':
                sync_ac_color(bridge, window)
                time.sleep(0.1)

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


def raise_color(color_hex: str, bridge: Bridge, window: sg.Window):
    if len(HUE_CONNECTION['lights']) == 0:
        show_error_window('No lights selected. Select lights under Settings -> General - Lights -> Lights to use')
    else:
        if color_hex == '':
            for light in HUE_CONNECTION['lights']:
                bridge.set_light(light, {'transitiontime': 0, 'on': False})
            window['CANVAS_FLAG'].update(background_color='#000000')
        else:
            converter = Converter()
            color_xy = converter.hex_to_xy(color_hex.replace('#', ''))
            for light in HUE_CONNECTION['lights']:
                bridge.set_light(light, {'transitiontime': 0, 'on': True, 'bri': int(HUE_CONNECTION['brightness']),
                                         'xy': color_xy})
            window['CANVAS_FLAG'].update(background_color=color_hex)


def show_error_window(error: str):
    layout = [
        [sg.Text(error, font=('Helvetica', 12), text_color='red')]
    ]

    window = sg.Window('Error', layout, icon=images, font='Helvetica', finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            window.close()
            break


if __name__ == "__main__":
    open_window()
