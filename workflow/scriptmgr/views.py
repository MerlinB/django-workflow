from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .forms import Rechnung2PdfForm
import inspect
from . import utils


skripte_dir = "/home/scholarium/Skripte/"
python_bin = skripte_dir+"venv/bin/python3.6"


@staff_member_required
def control_view(request):
    functions = inspect.getmembers(utils, inspect.isfunction)
    skripte = {}
    context = {
        'skripte': functions,
    }
    for f in functions:
        print(str(inspect.signature(utils.f)))
    return render(request, 'workflow/skripte-view.html', context)

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
    return render(request, 'workflow/form-view.html', context)
