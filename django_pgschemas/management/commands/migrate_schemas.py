from django.core import management
from django.core.management.base import BaseCommand

from . import WrappedSchemaOption
from .runschema import Command as RunSchemaCommand


class NonInteractiveRunSchemaCommand(RunSchemaCommand):
    interactive = False


class MigrateSchemasCommand(WrappedSchemaOption, BaseCommand):
    interactive = False

    def handle(self, *args, **options):
        runschema = NonInteractiveRunSchemaCommand()
        management.call_command(runschema, "django.core.migrate", *args, **options)


Command = MigrateSchemasCommand
