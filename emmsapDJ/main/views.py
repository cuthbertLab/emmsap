from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import os
from . import models

from .forms import UploadFileForm

# Create your views here.

def index(r):
    return render(r, 'main/index.html', {
       'allComposers': models.Composer.objects.order_by('name'),
    })

def how_to_do_index_the_long_way(request):
    allComposers = models.Composer.objects.order_by('name')
    template = loader.get_template('main/index.html')
    context = {
       'allComposers': allComposers,
    }                  
    return HttpResponse(template.render(context, request))


def composer(request, composerId):
    c = get_object_or_404(models.Composer, pk=composerId)    
    allPieces = models.Piece.objects.filter(composer=c)
    
    return render(request, 'main/composerDetail.html', {'composer': c,
                                                        'allPieces': allPieces,
                                                        })

def listComposers(request):
    allComposers = models.Composer.objects.order_by('name')
    out = '<br>\n'.join([c.name for c in allComposers])
    return HttpResponse(out)

def onePieceWithImage(r):
    pass

def assignComposer(r, pieceId):
    p = get_object_or_404(models.Piece, pk=pieceId)
    allComposers = models.Composer.objects.all()
    return render(r, 'main/assignComposers.html', {'piece': p,
                                                   'allComposers': allComposers,
                                                   })

def assignComposerFollowup(r, pieceId):
    p = get_object_or_404(models.Piece, pk=pieceId)
    try:
        selectedComposer = models.Composer.objects.get(pk=r.POST['composerChoice'])
    except (KeyError, models.Composer.DoesNotExist):
        # Redisplay the question voting form.
        return render(r, 'main/assignComposers.html', {
            'piece': p,
            'error_message': "Your composer choice sucked!",
        })
    else:
        p.composer = selectedComposer
        p.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('emmsap:index'))    


def uploadFile(r):
    if r.method == 'POST':
        form = UploadFileForm(r.POST, r.FILES)
        print(r.FILES)
        uploadedFile = r.FILES['file']
        pp = os.path.dirname(__file__)
        with open(pp + '/uploadFiles/t123.png', 'wb+') as destination:
            for chunk in uploadedFile.chunks():
                destination.write(chunk)
        return HttpResponseRedirect(reverse('emmsap:index'))
#         else:
#             return HttpResponse("Whoa! not valid, man!")
        
    else:
        form = UploadFileForm()
        return render(r, 'main/upload.html', {'form': form})
