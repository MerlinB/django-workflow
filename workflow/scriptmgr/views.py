from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .forms import Rechnung2PdfForm
import inspect
from . import utils, betrieb
from pprint import pprint
from celery import shared_task
from .celery import MyFunction
import sys

pyzot = utils.ImportForeign('pyzot','/home/merlin/Documents/Exzerpte/pyzot.py', venv='/home/merlin/Documents/Exzerpte/venv')

skripte_dir = "/home/scholarium/Skripte/"
python_bin = skripte_dir+"venv/bin/python3.6"


@staff_member_required
def control_view(request):
    if request.method == "POST":
        module = globals()[request.POST['module'].split('.')[-1]]
        method = getattr(module, request.POST['function'])
        MyFct = MyFunction(method)
        MyFct.run()

    modules = {}
    imports = [
        betrieb,
        utils,
        pyzot,
    ]
    for i in imports:
        functions = inspect.getmembers(i, inspect.isfunction)
        skripte = []
        for f in functions:
            source = {
                'name': f[0],
                'sig': inspect.signature(f[1]),
                'doc': inspect.getdoc(f[1]),
                'module': f[1].__module__
            }
            skripte.append(source)
        for item in skripte:
            modules.setdefault(item['module'], []).append(item)
    # pprint(modules)
    context = {
        'modules': modules,
        # 'module': module,
    }
    return render(request, 'scriptmgr/skripte-view.html', context)

def rechnung_view(request):
    if request.method == 'POST':
        subprocess.Popen([python_bin, skripte_dir+'Text/Rechnung2Pdf.py'])

    form = Rechnung2PdfForm

    # skripte = {
    #     'Rechnung2Pdf': '/home/scholarium/Skripte/Text/Rechnung2Pdf'
    # }
    context = {
        'form': form
    }
    return render(request, 'scriptmgr/form-view.html', context)
