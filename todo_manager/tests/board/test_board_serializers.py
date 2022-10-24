from django.test import TestCase
from django.utils import timezone

from goals.models import Board
from goals.serializers import BoardCreateSerializer
from tests.factories import BoardFactory


class BoardSerializersTestCase(TestCase):

    def test_create_board_serializer(self):
        """
        BoardCreateSerializer
        """
        board: Board = BoardFactory()
        data = BoardCreateSerializer(board).data
        ex_data = {'id': board.id,
                   'created': timezone.localtime(board.created).isoformat(),
                   'updated': timezone.localtime(board.updated).isoformat(),
                   'title': board.title,
                   'is_deleted': False}

        self.assertDictEqual(data, ex_data)
