import click
import os
from jinja2 import Environment, FileSystemLoader

APP_VERSION = "1.0.0"

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))


# Function to render templates
def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)


# Function to write content to a file
def write_file(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('entity_name')
def generate(entity_name):
    context = {
        'app_version': APP_VERSION,
        'entity_name': entity_name
    }

    # Define file paths and corresponding templates
    files = {
        f'src/domain/model/{entity_name}.py': 'model.py.j2',
        f'src/domain/repository/{entity_name}.py': 'repository.py.j2',
        f'src/infrastructure/repository/sqlalchemy/{entity_name}.py': 'sqlalchemy_repository.py.j2',
        f'src/application/schema/{entity_name}/__init__.py': 'schema_init.py.j2',
        f'src/application/schema/{entity_name}/display.py': 'schema_display.py.j2',
        f'src/application/schema/{entity_name}/short.py': 'schema_short.py.j2',
        f'src/application/schema/{entity_name}/create.py': 'schema_create.py.j2',
        f'src/application/service/{entity_name}.py': 'service.py.j2',
    }

    # Create directories and files
    for filepath, template_name in files.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if os.path.exists(filepath):
            overwrite = click.confirm(f'{filepath} already exists. Do you want to overwrite it?', default=False)
            if not overwrite:
                click.echo(f'Skipped {filepath}')
                continue
        content = render_template(template_name, context)
        write_file(filepath, content)
        click.echo(f'Generated {filepath}')


if __name__ == '__main__':
    cli()
