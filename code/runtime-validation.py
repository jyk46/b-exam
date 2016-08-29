#=========================================================================
# runtime-validation.py
#=========================================================================

import matplotlib.pyplot as plt
import math
import sys
import os.path
import numpy as np

#-------------------------------------------------------------------------
# Calculate figure size
#-------------------------------------------------------------------------
# We determine the fig_width_pt by using \showthe\columnwidth in LaTeX
# and copying the result into the script. Change the aspect ratio as
# necessary.

fig_width_pt  = 768.0
inches_per_pt = 1.0/72.27                     # convert pt to inch

aspect_ratio  = 0.52

fig_width     = 8.0                          # width in inches
fig_height    = fig_width * aspect_ratio      # height in inches
fig_size      = [ fig_width, fig_height ]

#-------------------------------------------------------------------------
# Configure matplotlib
#-------------------------------------------------------------------------

plt.rcParams['pdf.use14corefonts'] = True
plt.rcParams['font.size']          = 14
plt.rcParams['font.family']        = 'serif'
plt.rcParams['font.serif']         = ['Times']
plt.rcParams['figure.figsize']     = fig_size

#-------------------------------------------------------------------------
# Helper functions
#-------------------------------------------------------------------------

def draw_cutoffs( init_x, init_y, label, x_tweak=0.0, y_tweak=0.0 ):
  x1 = [ init_x, init_x + 0.1 ]
  y1 = [ init_y, init_y + 0.2 ]
  y2 = [ y1[0] - 0.2, y1[1] - 0.2 ]

  plt.plot( x1, y1, color = 'w', linestyle = '-', linewidth = 1.5 )
  plt.plot( x1, y2, color = 'w', linestyle = '-', linewidth = 1.5 )

  return ax.annotate(
    label, xy = ( init_x + 0.05 + x_tweak, init_y + 0.15 + y_tweak ),
    horizontalalignment='center',
    verticalalignment='bottom',
    fontsize = 11.0 )

#-------------------------------------------------------------------------
# Raw data
#-------------------------------------------------------------------------

# Benchmarks

bmarks = [
  'sgemm',
  'dct8x8m',
  'mriq',
  'bfs-nd',
  'maxmatch',
  'strsearch',
]

num_bmarks = len( bmarks )

# Configurations

configs = [
  'scalar',
  'cilk++',
  'tbb',
  'lta',
]

num_configs = len( configs )

# Results (execution time in seconds)

cycle_data = [

  # scalar

  [
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
  ],

  # cilk++

  [
    10.42,
    3.32,
    7.53,
    2.29,
    1.61,
    11.18,
  ],

  # tbb

  [
    11.76,
    3.33,
    8.83,
    1.77,
    1.73,
    9.97,
  ],

  # lta

  [
    10.32,
    3.38,
    9.54,
    1.77,
    2.05,
    11.22,
  ],

]

perf_data = [ np.array( data ) / np.array( cycle_data[0] ) for data in cycle_data ]

#-------------------------------------------------------------------------
# Plot parameters
#-------------------------------------------------------------------------

# Setup x-axis

ind = np.arange( num_bmarks )
mid = num_configs / 2.0

# Bar widths

width = 0.12

# Colors

colors = [
  '#000000',
  '#FF6666',
  '#66C2FF',
  '#80FFBF',
]

#-------------------------------------------------------------------------
# Create plot
#-------------------------------------------------------------------------

# Initialize figure

fig = plt.figure()
ax  = fig.add_subplot(111)

# Plot formatting

ax.set_xticks( ind+mid*width+width )
ax.set_xticklabels( bmarks, rotation=0, fontsize=12 )

ax.set_ylabel( 'Speedup', fontsize=14 )
ax.yaxis.set_label_coords( -0.04, 0.5 )
ax.set_yticks( np.arange( 0, 13, 1 ) )

ax.grid(True)
ax.set_axisbelow(True)

# Set axis limits

plt.axis( xmax=num_bmarks-1+(num_configs+2)*width )

# Add bars for each configuration

rects = []

for i, perf in enumerate( perf_data ):
  rects.append( ax.bar( ind+width*i+width, perf, width, color=colors[i] ) )

# Set tick positions

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Add horizontal line for baseline

plt.axhline( y=1, color='k', linewidth=1.5 )

# Cut-off lines

labels = []
#labels.append( draw_cutoffs( 0.22, 11.8, '12.5', -0.05 ) )
#labels.append( draw_cutoffs( 0.46, 11.8, '15.2', 0.3 ) )
#labels.append( draw_cutoffs( 1.46, 11.8, '15.5' ) )

# Legend

legend = ax.legend(
  rects, configs, loc='lower center', bbox_to_anchor=(0.5,1.02),
  ncol=4, borderaxespad=0, prop={'size':11}, frameon=True
)

# Pretty layout

plt.tight_layout()

# Turn off top and right border

ax.xaxis.grid(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

#-------------------------------------------------------------------------
# Generate PDF
#-------------------------------------------------------------------------

input_basename = os.path.splitext( os.path.basename(sys.argv[0]) )[0]
output_filename = input_basename + '.py.pdf'
plt.savefig( output_filename, bbox_inches='tight' )
