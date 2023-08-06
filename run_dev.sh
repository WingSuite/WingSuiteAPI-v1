export RUN_MODE=0
flask --app main.py --debug run --host=0.0.0.0
echo
echo "Unsetting RUN_MODE"
echo "Exiting..."
unset RUN_MODE