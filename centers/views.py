import logging
# pyrefly: ignore [missing-import]
from django.shortcuts import render
# pyrefly: ignore [missing-import]
from django.views.decorators.http import require_GET
from .models import Center

logger = logging.getLogger(__name__)


@require_GET
def center_map_view(request):
    try:
        centers = Center.objects.all()
    except Exception:
        logger.exception("Failed to load centers from the database")
        return render(request, 'centers/map_view.html', {
            'error': 'Error loading centers. Please try again later.',
            'centers': []
        })

    if not centers.exists():
        context = {
            'centers': [],
            'message': 'No recycling centers available at the moment.'
        }
    else:
        context = {'centers': centers}

    return render(request, 'centers/map_view.html', context)