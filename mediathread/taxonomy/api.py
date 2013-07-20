from courseaffils.models import Course
from django.contrib.contenttypes.models import ContentType
from mediathread.api import ClassLevelAuthentication, ToManyFieldEx
from mediathread.taxonomy.models import Vocabulary, Term
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class TermResource(ModelResource):

    class Meta:
        queryset = Term.objects.all().order_by('id')
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = ClassLevelAuthentication()


class VocabularyAuthorization(Authorization):

    def apply_limits(self, request, object_list):
        course_type = ContentType.objects.get_for_model(request.course)
        invisible = []
        for vocabulary in object_list:
            if (vocabulary.content_type == course_type and
                    not vocabulary.content_object == request.course):
                invisible.append(vocabulary.id)

        object_list = object_list.exclude(id__in=invisible)
        return object_list.order_by('id')


class VocabularyResource(ModelResource):
    term_set = ToManyFieldEx(
        'mediathread.taxonomy.api.TermResource',
        'term_set',
        blank=True, null=True, full=True)

    class Meta:
        queryset = Vocabulary.objects.all().order_by('id')
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'delete']
        authentication = ClassLevelAuthentication()
        authorization = VocabularyAuthorization()

        ordering = ['id', 'title']

    def dehydrate(self, bundle):
        return bundle

    def hydrate(self, bundle):
        bundle.obj.content_type = ContentType.objects.get(
            id=bundle.data['content_type_id'])
        bundle.obj.course = Course.objects.get(id=bundle.data['object_id'])
        return bundle
