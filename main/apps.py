import os
import sys
from django.apps import AppConfig
from django.core.management import get_commands

class RAGConfig(AppConfig):
    name = 'core'

    def ready(self):
        from core import initialize_qa_engines, setup_index

        setup_index()
        initialize_qa_engines()