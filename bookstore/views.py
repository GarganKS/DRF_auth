from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Author, Book
from .permissions import IsBookOwner, P1Permission
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """Публічний довідник авторів: читати може будь-хто. Не змінюйте права тут."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [P1Permission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__name"]
    ordering_fields = ["price", "title"]

    def perform_create(self, serializer):
        owner = self.request.user if self.request.user.is_authenticated else None
        serializer.save(owner=owner)

    @action(
        detail=True,
        methods=["post"],
        url_path="cover",
        parser_classes=[MultiPartParser],
        permission_classes=[IsBookOwner],
    )
    def upload_cover(self, request, pk=None):
        book = self.get_object()

        cover = request.FILES.get("cover")

        if not cover:
            return Response(
                {"detail": "Файл cover обов'язковий."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        book.cover = cover
        book.save(update_fields=["cover"])

        return Response(
            {"cover": request.build_absolute_uri(book.cover.url)},
            status=status.HTTP_200_OK,
        )
