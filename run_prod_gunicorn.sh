export RUN_MODE=1
gunicorn --bind "0.0.0.0:5000" wsgi:app
echo
echo "Unsetting RUN_MODE"
echo "Exiting..."
unset RUN_MODE