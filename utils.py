from aws_cdk import Tags


def add_tags(source, tag_value: str, env: str, custom_tags: dict = None):
    Tags.of(source).add('Name', tag_value)
    Tags.of(source).add('Environment', env)

    [Tags.of(source).add(key, value) for key, value in custom_tags.items()] if custom_tags else None
