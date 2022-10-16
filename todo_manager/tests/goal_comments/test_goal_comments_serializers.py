from django.test import TestCase

from goals.models import GoalComment
from goals.serializers import GoalCommentsCreateSerializer
from tests.factories import GoalCommentFactory


class GoalCommentSerializersTestCase(TestCase):

    def test_create_goal_comments_serializer(self):
        """
        GoalCommentsCreateSerializer
        """
        goal_comment: GoalComment = GoalCommentFactory()
        data = GoalCommentsCreateSerializer(goal_comment).data
        ex_data = {'id': goal_comment.id, 'created': goal_comment.created, 'updated': goal_comment.updated,
                   'text': goal_comment.text, 'goal': goal_comment.goal.id}
        self.assertEqual(ex_data, data)
