# imports
import click

@click.command()
def does_it_work():
    print("Hello there! -- This is docker-one kenobi")

if __name__ == '__main__':
    does_it_work()