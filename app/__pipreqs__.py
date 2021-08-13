"""
using pipreqs --force in the parent directory to auto-generate
our requirements.txt - however no code ever uses gunicorn.  only
the dockerfile uses it so this will force pipreqs to include
gunicorn
"""

import gunicorn