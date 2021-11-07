import eel


if __name__ == '__main__':
    eel.init('web')
    eel.start('index.html', mode='default', size=(1024, 768), position=(0, 0))
