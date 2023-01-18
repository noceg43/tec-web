from django.test import TestCase

# Create your tests here.
from django.urls import reverse
import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question


def create_question(question_text, days):
    """
    Creates a question: days represent the offset to now: negative 
    for questions published in the past, positive for those in the future 
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time)


class QuestionViewTests(TestCase):
    # caso con più assert sia risposta "no domande disponibili che lista domande recente vuota"
    def test_index_view_with_no_questions(self):
        """
        No questions --> "No polls are available" 
        message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be 
        displayed
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        print(response.context)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future --> not shown
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future polls exist, only past polls should be
        displayed.
        """
        create_question(question_text="Past poll.", days=-30)
        create_question(question_text="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past poll.>']
        )
