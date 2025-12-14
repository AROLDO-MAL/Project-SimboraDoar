
import os
import django
from django.conf import settings
from django.template.loader import render_to_string

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simboradoar.settings')
django.setup()

try:
    # Try to render the template. 
    # We might need a request context, but strict syntax checks happen on loading usually.
    # rendering will check tag execution.
    print("Attempting to load donate_options.html...")
    render_to_string('core/donate_options.html')
    print("donate_options.html rendered successfully!")

    print("Attempting to load donate_custom.html...")
    render_to_string('core/donate_custom.html', {'items': []}) # Need items context to avoid loop error if strict
    print("donate_custom.html rendered successfully!")
except Exception as e:
    print(f"Error rendering template: {e}")
