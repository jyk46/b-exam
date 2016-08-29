#=========================================================================
# fig-motivation-native.py
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

aspect_ratio  = 0.95

fig_width     = 5.0                           # width in inches
fig_height    = fig_width * aspect_ratio      # height in inches
fig_size      = [ fig_width, fig_height ]

#-------------------------------------------------------------------------
# Configure matplotlib
#-------------------------------------------------------------------------

plt.rcParams['pdf.use14corefonts'] = True
plt.rcParams['font.size']          = 16
plt.rcParams['font.family']        = 'serif'
plt.rcParams['font.serif']         = ['Times']
plt.rcParams['figure.figsize']     = fig_size

#-------------------------------------------------------------------------
# Helper functions
#-------------------------------------------------------------------------

def draw_cutoffs( init_x, init_y, label, x_tweak=0.0, y_tweak=0.0 ):
  x1 = [ init_x, init_x + 0.1 ]
  y1 = [ init_y, init_y + 0.2 ]
  y2 = [ y1[0] - 0.4, y1[1] - 0.4 ]

  plt.plot( x1, y1, color = 'w', linestyle = '-', linewidth = 1.5 )
  plt.plot( x1, y2, color = 'w', linestyle = '-', linewidth = 1.5 )

  return ax.annotate(
    label, xy = ( init_x + 0.05 + x_tweak, init_y + 0.4 + y_tweak ),
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
  'rgb2cmyk',
  'bfs-nd',
  'maxmatch',
  'strsearch',
]

num_bmarks = len( bmarks )

# Configurations

configs = [
  'cmp-scalar',
  'cmp-avx',
  'cmp-tbb',
  'cmp-tbb-avx',
#  'mic-avx',
  'mic-tbb-avx',
  'gpgpu-cuda',
]

num_configs = len( configs )

# Results (execution time in seconds)

cycle_data = [

  # cmp-scalar

  [
    244.484,
    49.467,
    126.191,
    25.8277,
    18.2,
    5.95,
    105.561,
  ],

  # cmp-avx

  [
    34.914,
    19.569,
    52.283,
    4.5209,
    17.1,
    5.91,
    85.785,
  ],

  # cmp-tbb (nthreads=12)

  [
    22.564,
    14.623,
    15.460,
    4.18735,
    8.64,
    1.75,
    15.935,
  ],

  # cmp-tbb+avx (nthreads=12)

  [
    3.871,
    16.834,
    22.944,
    5.35787,
    8.6,
    1.77,
    13.357,
  ],

  # mic-avx

#  [
#    325.11,
#    283.97,
#    87.82,
#    45.7,
#    19.8,
#    531.19,
#  ],

  # mic-tbb-avx (nthreads=240)

  [
    1.48,
    5.04,
    6.93,
    1.89,
    3.479,
    1.34,
    7.16,
  ],

  # gpu-cuda

  [
    0.512,
    0.845,
    0.959,
    0.812,
    4.720, #8.085,
    13.703,
    17.405,
  ],

]

perf_data = [ np.array( [ float(i) for i in cycle_data[0] ] ) /
              np.array( data ) for data in cycle_data ]

#-------------------------------------------------------------------------
# Plot parameters
#-------------------------------------------------------------------------

# Setup x-axis

ind = np.arange( num_bmarks )
mid = num_configs / 2.0

# Bar widths

width = 0.09

# Colors

colors = [
  '#000000',
  '#CCEBFF',
  '#66c2ff',
  '#0099ff',
#  '#cc99ff',
#  '#ffcccc',
  '#ff6666',
  '#33ffad',
]


#-------------------------------------------------------------------------
# Create plot
#-------------------------------------------------------------------------

# Initialize figure

fig = plt.figure()
ax  = fig.add_subplot(111)

# Plot formatting

#ax.set_title( 'Speedup over Optimized Scalar Implementation' )
ax.set_xticks( ind+mid*width+width )
ax.set_xticklabels( bmarks, fontsize=14, rotation=45 )

#ax.set_xlabel( 'Benchmarks', fontsize=12 )
ax.set_ylabel( 'Speedup', fontsize=14 )

ax.grid(True)
ax.set_axisbelow(True)

# Set axis limits

plt.axis( xmax=num_bmarks-1+(num_configs+2)*width, ymax=21.0 )

# Add bars for each configuration

rects = []

for i, perf in enumerate( perf_data ):
  if i == 4:
    break
  rects.append( ax.bar( ind+width*i+width, perf, width, color=colors[i] ) )

# Set tick positions

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Add horizontal line for baseline

plt.axhline( y=1, color='k', linewidth=1.5 )

# Cut-off lines

labels = []
labels.append( draw_cutoffs( 0.42 - 0.09, 20.6, '63', -0.2, -1.5 ) )
#labels.append( draw_cutoffs( 0.53 - 0.09, 20.6, '165' ) )
#labels.append( draw_cutoffs( 0.64 - 0.09, 20.6, '478', 0.25, -1.5 ) )
#labels.append( draw_cutoffs( 1.63 - 0.09, 20.6, '59' ) )
#labels.append( draw_cutoffs( 2.63 - 0.09, 20.6, '132' ) )
#labels.append( draw_cutoffs( 3.63 - 0.09, 20.6, '32' ) )

# Legend

#legend = ax.legend(
#  rects, configs, loc='lower center', bbox_to_anchor=(0.5,1.10),
#  ncol=3, borderaxespad=0, prop={'size':12}, frameon=True )

#legend = ax.legend(
#  rects, configs, loc='upper right', bbox_to_anchor=(0.85,1.05),
#  ncol=1, borderaxespad=0, prop={'size':12}, frameon=True )

# Pretty layout

plt.tight_layout( )

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
plt.savefig( output_filename, #bbox_extra_artists=(legend,), #labels[1],),
             bbox_inches='tight' )

