"""Views and tools for debugging Django."""


def splode(request):
    """View to cause an exception, usually to view Django's settings."""
    raise Exception("This exception raised deliberately to view debug info.")
