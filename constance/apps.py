from django.db.models import signals
from django.apps import AppConfig
from django.conf import settings

class ConstanceConfig(AppConfig):
    name = 'constance'
    verbose_name = 'Constance'

    def ready(self):
        super(ConstanceConfig, self).ready()
        signals.post_migrate.connect(self.create_perm,
                                     dispatch_uid='constance.create_perm')

    def create_perm(self, using=None, *args, **kwargs):
        """
        Creates a fake content type and permission
        to be able to check for permissions
        """
        from django.contrib.contenttypes.models import ContentType

        if ContentType._meta.installed:
            content_type, created = ContentType.objects.using(using).get_or_create(
                app_label='constance',
                model='config',
            )

        if 'auth' not in settings.INSTALLED_APPS:
            return

        from django.contrib.auth.models import Permission

        if Permission._meta.installed:
            permission, created = Permission.objects.using(using).get_or_create(
                name='Can change config',
                content_type=content_type,
                codename='change_config')

