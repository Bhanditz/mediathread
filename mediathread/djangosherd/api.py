from django.db.models import Q
from mediathread.api import UserResource, ClassLevelAuthentication, TagResource
from mediathread.djangosherd.models import SherdNote
from mediathread.main import course_details
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource


class SherdNoteAuthorization(Authorization):

    def apply_limits(self, request, object_list):
        if request.user.is_authenticated():
            # only request user's global annotations
            object_list = object_list.exclude(~Q(author=request.user),
                                              range1__isnull=True)

            # Make sure the requesting user is allowed to see this note
            invisible = []
            for note in object_list:
                course = note.asset.course

                if not course.is_member(request.user):
                    invisible.append(note.id)
                elif (not course.is_faculty(request.user) and
                      not course_details.all_selections_are_visible(course)):
                    # apply per course limitations
                    # the user or a faculty member must be the selection author
                    authorized = list(course.faculty)
                    authorized.append(request.user)
                    if not note.author in authorized:
                        invisible.append(note.id)

            return object_list.exclude(id__in=invisible).order_by('id')
        elif request.public:
            return object_list.order_by('id')
        else:
            return []


class SherdNoteResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author', full=True)

    class Meta:
        queryset = SherdNote.objects.all().order_by("id")
        excludes = ['tags', 'body', 'added', 'modified']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {'author': ALL_WITH_RELATIONS}

        # User is logged into some course
        authentication = ClassLevelAuthentication()

        # User is authorized to look at this particular SherdNote
        authorization = SherdNoteAuthorization()

    def dehydrate(self, bundle):
        bundle.data['asset_id'] = str(bundle.obj.asset.id)
        bundle.data['is_global_annotation'] = \
            str(bundle.obj.is_global_annotation())
        bundle.data['is_null'] = bundle.obj.is_null()
        bundle.data['annotation'] = bundle.obj.annotation()
        bundle.data['editable'] = (bundle.request.user.id ==
                                   getattr(bundle.obj, 'author_id', -1))
        bundle.data['url'] = bundle.obj.get_absolute_url()

        bundle.data['metadata'] = {
            'tags': TagResource().render_list(bundle.request,
                                              bundle.obj.tags_split()),
            'body': bundle.obj.body,
            'primary_type': bundle.obj.asset.primary.label,
            'modified': bundle.obj.modified.strftime("%m/%d/%y %I:%M %p"),
            'timecode': bundle.obj.range_as_timecode(),
            'title': bundle.obj.title
        }
        return bundle

    def render_one(self, request, selection, asset_key):
        bundle = self.build_bundle(obj=selection, request=request)
        dehydrated = self.full_dehydrate(bundle)
        bundle.data['asset_key'] = '%s_%s' % (asset_key, bundle.obj.asset.id)
        return self._meta.serializer.to_simple(dehydrated, None)

    def render_list(self, request, lst, asset_key):
        data = []
        for item in lst:
            bundle = self.build_bundle(obj=item, request=request)
            bundle.data['asset_key'] = '%s_%s' % (
                asset_key, bundle.obj.asset.id)
            dehydrated = self.full_dehydrate(bundle)
            data.append(dehydrated.data)
        return data
