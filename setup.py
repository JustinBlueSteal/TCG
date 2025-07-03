import click
import subprocess
import os
from pathlib import Path

@click.group()
def cli():
    """A CLI for managing the Card Platform application."""
    pass
@cli.command()
def configure():
    """Prompts for credentials and writes to the backend .env file."""
    click.echo("--- Configuring Backend Environment ---")
    
    env_path = Path(__file__).parent / 'backend' / '.env'
    
    if env_path.exists():
        if not click.confirm(f"{env_path} already exists. Do you want to overwrite it?"):
            click.echo("Configuration cancelled.")
            return

    secret_key = click.prompt('Enter a new Flask SECRET_KEY', hide_input=True, confirmation_prompt=True)
    db_user = click.prompt('Enter the DATABASE_USER', default='carduser')
    db_pass = click.prompt('Enter the DATABASE_PASSWORD', hide_input=True, confirmation_prompt=True, default='cardpass')
    db_name = click.prompt('Enter the DATABASE_NAME', default='card_platform_db')
    easypost_api_key = click.prompt('Enter your EASYPOST_API_KEY', default='EASYPOST_API_KEY_HERE')

    database_url = f"postgresql://{db_user}:{db_pass}@db:5432/{db_name}"

    with open(env_path, 'w') as f:
        f.write(f'FLASK_APP=app.py\n')
        f.write(f'FLASK_ENV=development\n')
        f.write(f'SECRET_KEY={secret_key}\n')
        f.write(f'DATABASE_URL={database_url}\n')
        f.write(f'EASYPOST_API_KEY={easypost_api_key}\n')
        f.write(f'POSTGRES_USER={db_user}\n')
        f.write(f'POSTGRES_PASSWORD={db_pass}\n')
        f.write(f'POSTGRES_DB={db_name}\n')

    click.secho(f"Successfully created environment file at {env_path}", fg="green")

@cli.command(name="db-init")
def db_init():
    """Initializes the database by running migrations inside the container."""
    click.echo("--- Initializing Database ---")
    
    # Ensure containers are running
    try:
        subprocess.check_output(['docker-compose', 'ps', '-q', 'backend'], stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.secho("The backend container is not running or docker-compose is not available. Please start it with 'docker-compose up' first.", fg="red")
        return

    commands = [
        "docker-compose exec backend flask db init",
        "docker-compose exec backend flask db migrate -m 'Initial migration.'",
        "docker-compose exec backend flask db upgrade"
    ]
    
    for i, cmd in enumerate(commands):
        click.secho(f"Running: {cmd}", fg="yellow")
        try:
            # For `db init`, we expect it to fail if the migrations dir already exists.
            if i == 0: 
                subprocess.run(cmd, shell=True, check=False, stderr=subprocess.PIPE)
                click.secho("... 'flask db init' completed or directory already exists.", fg="cyan")
            else:
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                click.echo(result.stdout)
        except subprocess.CalledProcessError as e:
            click.secho(f"Error running command: {cmd}", fg="red")
            # Safely print stderr if it exists
            error_output = e.stderr or "No error output."
            click.secho(error_output, fg="red")
            if "Target database is not up to date" in error_output:
                 click.secho("Database may already be initialized. Skipping further steps.", fg="yellow")
                 break
            return

    click.secho("Database initialization complete.", fg="green")


if __name__ == '__main__':
    cli()