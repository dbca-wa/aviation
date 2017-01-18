from django.conf import settings


def template_context(request):
    """Pass extra context variables to every template.
    """
    context = {
        'sitetitle': 'Aviation System',
        'application_version_no': '15.10',
        'application_custodian': 'Fire Management Services',
        'production_site': not settings.DEBUG
    }
    context.update(settings.STATIC_CONTEXT_VARS)
    return context
