#!/usr/bin/python3
import click
from data.dos import DOS
from data.cohp import COHP
from data.coop import COOP
from data.cobi import COBI
from data.population_analysis import PopulationAnalysis

@click.group()
def super():
    pass

@click.group()
@click.pass_context
def charges(ctx):
    ctx.obj = PopulationAnalysis()

@click.group()
@click.pass_context
def cobi(ctx):
    ctx.obj = COBI()

@click.group()
@click.pass_context
def coop(ctx):
    ctx.obj = COOP()

@click.group()
@click.pass_context
def cohp(ctx):
    ctx.obj = COHP()

@click.group()
@click.pass_context
def dos(ctx):
    ctx.obj = DOS('DOSCAR.lobster')


@click.command()
@click.pass_context
def get(ctx):
    print(ctx.obj.charges)


@click.command()
@click.pass_context
def get_states(ctx):
    states = ctx.obj.get_states()
    for state in states:
        print(state)

@click.command()
@click.option('--states', help='Plot DOS states.')
@click.option('--e_range', help='Energy range to plot.')
@click.pass_context
def plot(ctx, states, e_range):
    ctx.obj.print_plot(states, e_range)


dos.add_command(get_states)
dos.add_command(plot)
cobi.add_command(get_states)
cobi.add_command(plot)
coop.add_command(get_states)
coop.add_command(plot)
cohp.add_command(get_states)
cohp.add_command(plot)

charges.add_command(get)

super.add_command(charges)
super.add_command(dos)
super.add_command(cobi)
super.add_command(cohp)
super.add_command(coop)

if __name__ == '__main__':
    super()
