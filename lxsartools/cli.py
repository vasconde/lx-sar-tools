"""
lx-sar-tools

Usage:
  lx-sar-tools hello
  lx-sar-tools plot_band input <in_name> output <out_name>
  lx-sar-tools band2mat input <in_name> output <out_name>
  lx-sar-tools filter2d input <in_name> output <out_name> wsize <wsize>
  lx-sar-tools filter2d_complex inputi <in_name_i> inputq <in_name_q> output <out_name> wsize <wsize>
  lx-sar-tools filter2d_complex_mask inputi <in_name_i> inputq <in_name_q> mask <in_mask_name> wsize <wsize> outputi <out_name_i> outputq <out_name_q>
  lx-sar-tools coherence inputi1 <in_name_i_1> inputq1 <in_name_q_1> inputi2 <in_name_i_2> inputq2 <in_name_q_2> wsize <wsize> output <out_name>
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

import pdb

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

            # VC
            aux_con = getmembers(module, isclass)
            for elem in aux_con:
                if (elem[0].lower() == k.lower()):
                    #print(elem)
                    lxsartools.tools[0] = elem
            
            # VC
            
            command = [command[1] for command in lxsartools.tools if command[0] != 'Base'][0]
            #pdb.set_trace()
            command = command(options)
			
            command.run()
