export RUN_MODE=0
flask --app main.py --debug run
echo
echo "Unsetting RUN_MODE"
echo "Exiting..."
unset RUN_MODE