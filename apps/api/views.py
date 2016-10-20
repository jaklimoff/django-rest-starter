from inspect import getdoc
from urllib.parse import urljoin

import coreapi
import yaml
from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from somarket.api.serializers import SiteInfoSerializer, UpdateUserAvatarSerializer
from somarket.users.models import User


class TestSchema(schemas.SchemaGenerator):
    # FIXME: change expandable titles to urls

    def get_link(self, path, method, callback, view):
        """
        Return a `coreapi.Link` instance for the given endpoint.
        """
        view = callback.cls()

        fields = self.get_path_fields(path, method, callback, view)
        fields += self.get_serializer_fields(path, method, callback, view)
        fields += self.get_pagination_fields(path, method, callback, view)
        fields += self.get_filter_fields(path, method, callback, view)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, callback, view)
        else:
            encoding = None

        if hasattr(callback.cls, method.lower()):
            description = getdoc(getattr(callback.cls, method.lower()))
        else:
            description = getdoc(callback)

        if description:
            description = description.strip()

        return coreapi.Link(
            url=urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields, description=description
        )

    def get_serializer_fields(self, path, method, callback, view):
        """
        Return a list of `coreapi.Field` instances corresponding to any
        request body input, as determined by the serializer class.
        """
        if method not in ('PUT', 'PATCH', 'POST'):
            return []

        if not hasattr(view, 'serializer_class'):
            return []

        serializer = view.serializer_class

        fields = []
        if getdoc(serializer):
            doc_separated = getdoc(serializer).split('---')
            if len(doc_separated) == 2:
                yaml_doc = doc_separated[1]
                input_fields = yaml.load(yaml_doc).get('input')
                if input_fields:
                    for input in input_fields:
                        fields.append(
                            coreapi.Field(name=input, location='form', required=input_fields[input]['required'],
                                          description=input_fields[input]['description']))
        return fields


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = TestSchema(title='SOMARKET API')
    return response.Response(generator.get_schema(request=request))


@api_view(['GET'])
@permission_classes((AllowAny,))
def check_email(request):
    email = request.GET['email']
    try:
        user = User.objects.get(email=email)
        data = {'status': False}
    except User.DoesNotExist:
        data = {'status': True}
    return Response(data)


class UpdateUserAvatar(UpdateAPIView):
    serializer_class = UpdateUserAvatarSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class SiteInfoView(GenericAPIView):
    serializer_class = SiteInfoSerializer
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        return Response(self.get_serializer().data)
