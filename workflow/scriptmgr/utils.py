from .betrieb import RechnungErstellen
import sys, os
import importlib.util

def test1():
    pass

def test2(bla, test='Test'):
    '''A print function'''
    print(bla, test)

def testRechnung():
    testmeta = {
        'lang': 'english',
        'to': [
            'Merlin Buczek',
            'Grazer Damm 166',
            '12159 Berlin'
        ]
    }
    RechnungErstellen(testmeta)

def ReemdaTutWas():
    '''
    Reemda guckt Youtube.
    '''
    print('BLABLABLABLABLABLBALBAL')

def ImportForeign(module, path, venv=None):
    '''
    venv -- Path to venv
    '''
    if venv:
        # os.chdir(os.path.join(venv,'lib'))
        python_name = os.listdir(os.path.join(venv,'lib'))[0]
        search = os.path.join(venv, "lib/%s/site-packages/" % python_name)
        sys.path.append(search)
    #     spec = importlib.util.spec_from_file_location(module, path, submodule_search_locations=search)
    # else:
    spec = importlib.util.spec_from_file_location(module, path)

    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo
