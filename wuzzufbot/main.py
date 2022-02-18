import asyncio

import click
from rich.console import Console
from rich.table import Table

from wuzzufbot.parser import parse_jobs, parse_new_jobs
from wuzzufbot.pushover import push_notification

table = Table()
console = Console()

table.add_column("Job Title", style="red", no_wrap=True)
table.add_column("Posted At", style="green")


def async_command(func):

    def wrapper(*args, **kwargs):
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(func(*args, **kwargs))
        asyncio.run(func(*args, **kwargs))
        # pending = asyncio.Task.all_tasks()
        # loop.run_until_complete(asyncio.gather(*pending))
        return

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@click.group()
def cli():
    pass


@cli.command()
def parse():
    """command to parse jobs and print them to console"""
    jobs = parse_jobs()
    for job in jobs:
        table.add_row(job['title'], job['postedAt'])

    console.print(table)


@cli.command()
@click.option('-i',
              '--interval',
              default=15,
              show_default=True,
              help='interval time in minutes to parse')
@click.option('-p',
              '--push',
              default=False,
              show_default=True,
              is_flag=True,
              help='enable pushover notifications')
@async_command
async def listen(interval, push):
    """command to parse new jobs on interval time"""
    with console.status("[bold green]Listening for new jobs...",
                        spinner='clock',
                        refresh_per_second=3) as status:
        timer = 0
        while True:
            if timer <= 0:
                new_jobs = parse_new_jobs()
                if len(new_jobs) > 0:
                    if push:
                        asyncio.create_task(push_notification(new_jobs))

                    for job in new_jobs:
                        console.print('💼 Job: {} || Posted At: {} 💼'.format(
                            job['title'], job['postedAt']),
                                      style='bold blue')
                        await asyncio.sleep(1)

                else:
                    console.print(
                        '😿 No new jobs 😿',
                        style='bold red',
                    )

                timer = interval * 60

            timer -= 1
            status.update(f"[bold green]Retrying again in {timer} seconds..")
            await asyncio.sleep(1)


if __name__ == '__main__':
    cli()
