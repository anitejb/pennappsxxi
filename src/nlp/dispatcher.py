from .question_identifier import IsQuestion
from db.db import update_result


class Dispatcher:
    def __init__(self):
        self.question_identifier = IsQuestion()

    def update_result(self, record):
        new_question = self.identify_new_question_phrase()
        new_topic = self.identify_new_topic()
        update_result(new_topic, new_question)

    def identify_new_question_phrase(self):
        text, timestamp = record['text'], record['timestamp']
        is_question = self.question_identifier.predict_question()
        if is_question:
            question_type = self.question_identifier.predict_question_type()
            return [{"question": text, "question_type": question_type}]

        return []

    def identify_new_topic(self):
        return []
