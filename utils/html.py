# Imports
from config.config import html_map, config
from bs4 import BeautifulSoup
from typing import Any
import re


def read_html_file(template: str, **kwargs: Any) -> str:
    """Helper function to return html content"""

    # Insert organization's name to kwargs
    kwargs["org_name"] = config.organization_name

    # Get the content of the file
    with open(html_map[template], "r", encoding="utf-8") as file:
        content = file.read()

    # Iterate over the dictionary and replace the placeholders
    for key, value in kwargs.items():
        content = re.sub(r"\{" + key + r"\}", value, content)

    # Return the contents of the file
    return content


def strip_html(content: str) -> str:
    """Helper function to strip away html tags from string content"""

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(content, "html.parser")

    # Extract text from the parsed HTML
    stripped_text = soup.get_text(separator=" ")

    # Returned the stripped text
    return stripped_text
