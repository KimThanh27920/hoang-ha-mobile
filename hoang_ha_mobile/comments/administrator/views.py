from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from comments.models import Comment
from comments.administrator.serializers import CommentSerializer
from rest_framework.permissions import IsAdminUser
from comments.administrator.permissions import IsOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().select_related()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action != 'update':
            return super().get_permissions()
        list_of_permission = super().get_permissions()
        is_owner = IsOwner()
        list_of_permission.append(is_owner)
        return list_of_permission 

    def perform_create(self, serializer):
        serializer.save(
            updated_by = self.request.user, 
            created_by = self.request.user,
            name = self.request.user.full_name,
            email = self.request.user.email,
            phone = self.request.user.phone
        )

    def perform_update(self, serializer):
        serializer.save(updated_by = self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user 
        instance.deleted_at = datetime.now()
        instance.save()