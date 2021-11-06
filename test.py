import eel


eel.init('web')


@eel.expose
def test_python_function():
    eel.test_js_function()


eel.start('index.html', mode='edge')
