import re


class SlugTransformer:
    """
    Utility class for transforming text into slugs.

    Methods:
    - transform(text: str) -> str: Transforms the input text into a slug format.
    """

    @staticmethod
    def transform(text: str) -> str:
        """
        Transforms the input text into a slug format.

        Parameters:
        - text (str): The input text to be transformed.

        Returns:
        - str: The transformed text in slug format.
        """
        slug = text.replace(" ", "-").lower()
        slug = re.sub(r'[^a-zA-Z0-9_\-]', '', slug)
        return slug
