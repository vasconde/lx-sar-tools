"""
lx-sar-tools

Usage:
  lx-sar-tools hello
  lx-sar-tools plot_snap_band input <in_name> output <out_name>
  lx-sar-tools -h | --help
  lx-sar-tools --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  lx-sar-tools hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/vasconde/lx-sar-tools
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import lxsartools.tools
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(lxsartools.tools, k) and v:
            module = getattr(lxsartools.tools, k)
            lxsartools.tools = getmembers(module, isclass)
            command = [command[1] for command in lxsartools.tools if command[0] != 'Base'][0]
            command = command(options)
			
            command.run()
