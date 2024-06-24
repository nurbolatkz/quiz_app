# quiz/management/commands/populate_quizzes.py
from django.core.management.base import BaseCommand
from quiz.models import Question, Option, Example, Topic


class Command(BaseCommand):
    help = 'Populates the database with initial quiz data'

    def handle(self, *args, **kwargs):
        topic, created = Topic.objects.get_or_create(
            name="Prepositions in English")

        # Example questions about prepositions
        questions_data = [
            {
                "question_text": "I usually go __________ work by car.",
                "correct_answer": "to",
                "explanation": "The correct preposition is 'to' when indicating movement towards a place.",
                "options": {
                    "A": "at",
                    "B": "to",
                    "C": "in",
                    "D": "on"
                },
                "examples": [
                    {"sentence": "She walked __________ the door.",
                        "highlight": "walked to"},
                    {"sentence": "He jumped __________ the river.",
                        "highlight": "jumped into"},
                    {"sentence": "They live __________ London.",
                        "highlight": "live in"}
                ]
            },
            {
                "question_text": "We're going __________ holiday next week.",
                "correct_answer": "on",
                "explanation": "The correct preposition is 'on' when talking about a holiday or vacation.",
                "options": {
                    "A": "in",
                    "B": "on",
                    "C": "at",
                    "D": "by"
                },
                "examples": [
                    {"sentence": "She went __________ a trip to Paris.",
                        "highlight": "went on"},
                    {"sentence": "We traveled __________ the weekend.",
                        "highlight": "traveled over"}
                ]
            },
            {
                "question_text": "He is good __________ playing the guitar.",
                "correct_answer": "at",
                "explanation": "The correct preposition is 'at' when indicating skill or ability.",
                "options": {
                    "A": "on",
                    "B": "at",
                    "C": "for",
                    "D": "with"
                },
                "examples": [
                    {"sentence": "She's very talented __________ drawing.",
                        "highlight": "talented at"},
                    {"sentence": "They are experienced __________ managing projects.",
                        "highlight": "experienced at"}
                ]
            },
            {
                "question_text": "She was born __________ 10th May.",
                "correct_answer": "on",
                "explanation": "The correct preposition is 'on' when specifying dates.",
                "options": {
                    "A": "in",
                    "B": "at",
                    "C": "on",
                    "D": "by"
                },
                "examples": [
                    {"sentence": "My birthday is __________ July.",
                        "highlight": "is in"},
                    {"sentence": "The concert is __________ Friday.",
                        "highlight": "is on"}
                ]
            },
            {
                "question_text": "He arrived __________ the airport.",
                "correct_answer": "at",
                "explanation": "The correct preposition is 'at' when indicating arrival at a specific place.",
                "options": {
                    "A": "to",
                    "B": "in",
                    "C": "at",
                    "D": "by"
                },
                "examples": [
                    {"sentence": "She's waiting __________ the bus stop.",
                        "highlight": "waiting at"},
                    {"sentence": "We met __________ the restaurant.",
                        "highlight": "met at"}
                ]
            },
            {
                "question_text": "They agreed __________ the new plan.",
                "correct_answer": "on",
                "explanation": "The correct preposition is 'on' when reaching an agreement.",
                "options": {
                    "A": "for",
                    "B": "on",
                    "C": "with",
                    "D": "at"
                },
                "examples": [
                    {"sentence": "We need to decide __________ a date.",
                        "highlight": "decide on"},
                    {"sentence": "She insisted __________ a different approach.",
                        "highlight": "insisted on"}
                ]
            },
            {
                "question_text": "He is allergic __________ cats.",
                "correct_answer": "to",
                "explanation": "The correct preposition is 'to' when indicating a sensitivity or reaction.",
                "options": {
                    "A": "at",
                    "B": "to",
                    "C": "with",
                    "D": "for"
                },
                "examples": [
                    {"sentence": "She's not accustomed __________ spicy food.",
                        "highlight": "accustomed to"},
                    {"sentence": "He has a fear __________ heights.",
                        "highlight": "fear of"}
                ]
            },
            {
                "question_text": "The book is __________ the table.",
                "correct_answer": "on",
                "explanation": "The correct preposition is 'on' when indicating position or location.",
                "options": {
                    "A": "at",
                    "B": "on",
                    "C": "in",
                    "D": "by"
                },
                "examples": [
                    {"sentence": "I left my keys __________ the desk.",
                        "highlight": "left on"},
                    {"sentence": "There's a vase __________ the shelf.",
                        "highlight": "on the shelf"}
                ]
            },
            {
                "question_text": "She apologized __________ being late.",
                "correct_answer": "for",
                "explanation": "The correct preposition is 'for' when expressing apologies.",
                "options": {
                    "A": "to",
                    "B": "for",
                    "C": "with",
                    "D": "about"
                },
                "examples": [
                    {"sentence": "He thanked me __________ my help.",
                        "highlight": "thanked me for"},
                    {"sentence": "They congratulated her __________ her success.",
                        "highlight": "congratulated her on"}
                ]
            },
            {
                "question_text": "She's angry __________ her brother.",
                "correct_answer": "with",
                "explanation": "The correct preposition is 'with' when expressing anger towards someone.",
                "options": {
                    "A": "at",
                    "B": "with",
                    "C": "on",
                    "D": "for"
                },
                "examples": [
                    {"sentence": "He's disappointed __________ the result.",
                        "highlight": "disappointed with"},
                    {"sentence": "She's upset __________ the situation.",
                        "highlight": "upset about"}
                ]
            },
        ]

        for data in questions_data:
            # Create the Question object
            question = Question.objects.create(
                question_text=data['question_text'],
                correct_answer=data['correct_answer'],
                explanation=data['explanation'],
                topic=topic
            )

            # Create Options for the Question
            for label, text in data['options'].items():
                Option.objects.create(
                    question=question,
                    option_label=label,
                    option_text=text
                )

            # Create Examples for the Question
            for example_data in data['examples']:
                Example.objects.create(
                    question=question,
                    sentence=example_data['sentence'],
                    highlight=example_data['highlight']
                )

        self.stdout.write(self.style.SUCCESS(
            'Database successfully populated with initial quiz data.'))
