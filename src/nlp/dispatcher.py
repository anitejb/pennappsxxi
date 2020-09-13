from .question_identifier import IsQuestion
from .lda import LDA
from .wolfram import Wolfram
from db.db import update_result

class Dispatcher:
    def __init__(self):
        self.question_identifier = IsQuestion()
        self.lda = LDA()
        self.wolfram = Wolfram()

    def update_result(self, record):
        # print(record)
        new_question = self.identify_new_question_phrase(record)
        new_topic = self.identify_new_topic(record)
        wolfram_question = self.identify_wolfram_question(record)
        update_result(new_topic, new_question, wolfram_question)

    def identify_new_question_phrase(self, record):
        text, timestamp = record['text'], record['timestamp']
        is_question = bool(self.question_identifier.predict_question(text))
        if is_question:
            question_type = self.question_identifier.predict_question_type(text)
            return [{"question": text, "question_type": question_type}]

        return []

    def identify_new_topic(self, record):
        text, timestamp = record['text'], record['timestamp']
        if text:
            return self.lda.load_model(text)
        return []

    def identify_wolfram_question(self, record):
        text, timestamp = record['text'], record['timestamp']
        text = text.lower()
        if self.wolfram.STOP_WORD in text:
            question = text[text.index(self.wolfram.STOP_WORD) + len(self.wolfram.STOP_WORD):]
            return [self.wolfram.get_query_url(question)]
        return []
q