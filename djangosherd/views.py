from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from djangosherd.models import Asset, SherdNote
from djangosherd.models import NULL_FIELDS

from djangohelpers.lib import allow_http
from djangohelpers.lib import rendered_with

from assetmgr.lib import annotated_by
from courseaffils.lib import in_course_or_404

formfields = "tags title range1 range2 body annotation_data".split()
annotationfields = set("title range1 range2".split())

class AnnotationForm(forms.ModelForm):
    body = forms.CharField(label='Notes')
    range1 = forms.FloatField(widget=forms.widgets.HiddenInput,initial=0)
    range2 = forms.FloatField(widget=forms.widgets.HiddenInput,initial=0)
    annotation_data = forms.CharField(widget=forms.widgets.HiddenInput)
    tags = forms.CharField(help_text="<span class='helptext'>For multi-word tags, use underscores. Use commas in between tags.<br />Example: Vietnam_War, Fall_of_Saigon</span>")
    class Meta:
        model = SherdNote
        exclude = ('author', 'asset')

class GlobalAnnotationForm(forms.ModelForm):
    body = forms.CharField(label='My Item Notes')
    tags = forms.CharField(label='My Item Tags', help_text="<span class='helptext'>For multi-word tags, use underscores. Use commas to separate tags.<br />Example: Vietnam_War, Fall_of_Saigon</span>")
    class Meta:
        model = SherdNote
        exclude = ('annotation_data', 'author', 'asset', 'range1', 'range2', 'title')

@login_required
@allow_http("POST")
def create_annotation(request):
    asset = get_object_or_404(Asset,
                              pk=request.POST['annotation-context_pk'])

    form = dict((key[len('annotation-'):], val) for key, val in request.POST.items()
                if key.startswith('annotation-'))
        
    del form['context_pk']

    data = {'author': request.user,
            'asset': asset}

    for field in formfields:
        if form.get(field) != '':
            data[field] = form[field]

    clipping = False
    for field in NULL_FIELDS:
        if field in data:
            clipping = True
                
    assert clipping
    assert annotationfields.intersection(data)
    # ^^ the model will take care of the edge case

    annotation = SherdNote(**data)
    annotation.save()
    #new annotations should redirect 'back' to the asset
    # at the endpoint of the last annotation
    # so someone can create a new annotation ~lizday
    url_fragment = ''
    if annotation.range2:
        url_fragment = '#start=%s' % str(annotation.range2)

    redirect_to = request.GET.get('next',
                                  annotation.asset.get_absolute_url() + url_fragment  )
    return HttpResponseRedirect(redirect_to)

@allow_http("POST", "DELETE")
def annotation_dispatcher(request, annot_id):
    if request.method == "DELETE":
        return delete_annotation(request, annot_id)
    if request.method == "POST":
        return edit_annotation(request, annot_id)
    #if request.method == "GET":
    #    return view_annotation(request, annot_id)

@login_required
def delete_annotation(request, annot_id):
    annotation = get_object_or_404(SherdNote, pk=annot_id)

    if annotation.author != request.user:
        return HttpResponseForbidden

    annotation.delete()
    redirect_to = request.GET.get('next', '/')
    return HttpResponseRedirect(redirect_to)

@login_required
def edit_annotation(request, annot_id):
    annotation = get_object_or_404(SherdNote, pk=annot_id)

    if annotation.author != request.user:
        return HttpResponseForbidden("forbidden")

    form = dict((key[len('annotation-'):], val) for key, val in request.POST.items()
                if key.startswith('annotation-'))

    # don't let a global annotation turn into a clip, or v.v.
    if form.get('range1') or form.get('range2'):
        assert not annotation.is_null()
    else:
        assert annotation.is_null()

    for field in formfields:
        if field not in form: continue
        default = None
        if field == 'tags': default = ''
        setattr(annotation, field,
                form[field] or default)
    annotation.save()

    if request.is_ajax():
        response = dict(title=annotation.title,
                        tags=annotation.tags,
                        body=annotation.body)
        import simplejson
        response = simplejson.dumps(response)
        return HttpResponse(response, mimetype="application/json")
    
    redirect_to = request.GET.get('next', '.')
    return HttpResponseRedirect(redirect_to)


@login_required
@rendered_with('assetmgr/asset_table.html')
def annotations_collection_fragment(request,username):
    space_viewer = in_course_or_404(username, request.course)
    assets = annotated_by(Asset.objects.filter(course=request.course),
                          space_viewer)
    return {
        'space_viewer':space_viewer,
        'assets':assets,
        }
