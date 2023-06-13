from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (
    CodeConfirmSerializer,
    CustomUserCreationSerializer,
    CustomUserSerializer,
)
from api.permissions import IsAdmin

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ['username']

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data)

    @me.mapping.patch
    def update_me(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(data=serializer.data)


class UserSignUpView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        serializer = CustomUserCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data['username']
        try:
            user, _ = User.objects.get_or_create(
                email=email, username=username
            )
        except IntegrityError:
            return Response(
                'Указанный email или username уже существуют.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        confirmation_code = user.confirmation_code

        send_mail(
            subject='Code confirmation',
            message=f'Ваше подтверждение: ' f'{confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(
            {'email': email, 'username': username}, status=status.HTTP_200_OK
        )


class TokenObtainView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CodeConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if user and confirmation_code == user.confirmation_code:
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
