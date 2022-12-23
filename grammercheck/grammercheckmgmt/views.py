import nltk
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .serializers import TextSerializer
from nltk.corpus import wordnet
from rest_framework.views import APIView
from nltk import CFG
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from spellchecker import SpellChecker
from language_tool_python import LanguageTool


class TextView(viewsets.ModelViewSet):
    serializer_class = TextSerializer

    @action(methods=['post'], detail=False)
    def check_grammar(self, request):
        text = request.data['text']

        # Use NLTK to check grammar
        grammar_errors = nltk.pos_tag(nltk.word_tokenize(text))

        correct_grammar = []
        for word, tag in grammar_errors:
            if tag == 'NNP' or tag == 'NN':
                correct_grammar.append(word)
            else:
                correct_grammar.append(nltk.pos_tag([word])[0][0])

        # Correct spelling errors using pyspellchecker
        spell_checker = SpellChecker()
        misspelled_words = spell_checker.unknown(text.split())
        corrected_spelling = []
        for word in text.split(' '):
            if word in misspelled_words:
                corrected_spelling.append(spell_checker.correction(word))
            else:
                corrected_spelling.append(word)

        # Correct punctuation errors using language_tool_python
        tool = LanguageTool('en-US')
        corrected_text = tool.correct(text)

        return HttpResponse(f'Correct grammar: {correct_grammar}\nCorrect spelling: {corrected_spelling}\nCorrect punctuation: {corrected_text}')
