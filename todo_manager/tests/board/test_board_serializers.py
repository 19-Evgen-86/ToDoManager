from django.test import TestCase

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
        ex_data = {'id': board.id, 'created': board.created, 'updated': board.updated, 'title': board.title,
                   'is_deleted': False}
        self.assertEqual(ex_data, data)
