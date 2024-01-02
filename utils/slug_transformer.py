import re


class SlugTransformer:

    @staticmethod
    def transform(text: str) -> str:
        slug = text.replace(" ", "-").lower()
        slug = re.sub(r'[^a-zA-Z0-9_\-]', '', slug)
        return slug