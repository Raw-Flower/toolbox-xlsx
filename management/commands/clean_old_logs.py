from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from xlsx.models import FileLogs
from datetime import timedelta

class Command(BaseCommand):
    help = 'Clean old records(More than one month) available on FileLogs model'
    
    def handle(self, *args, **options):
        limit = now() - timedelta(days=30)
        logs = FileLogs.objects.filter(createtime__lt=limit)
        if len(logs)>0:
            for log in logs:
                log.delete()
            self.stdout.write(
                self.style.SUCCESS('Total logs deleted("%s")' % len(logs))
            )
        else:
            self.stdout.write(
                self.style.ERROR('No logs available')
            )
            
            
        