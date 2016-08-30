#=========================================================================
# fig-evaluation-case-uthreads.py
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

aspect_ratio  = 0.75

fig_width     = 8.0                           # width in inches
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
  y2 = [ y1[0] - 0.2, y1[1] - 0.2 ]

  plt.plot( x1, y1, color = 'w', linestyle = '-', linewidth = 1.5 )
  plt.plot( x1, y2, color = 'w', linestyle = '-', linewidth = 1.5 )

  return ax.annotate(
    label, xy = ( init_x + 0.05 + x_tweak, init_y + 0.15 + y_tweak ),
    horizontalalignment='center',
    verticalalignment='bottom',
    fontsize = 12.0 )

#-------------------------------------------------------------------------
# Raw data
#-------------------------------------------------------------------------

# Configurations

configs = [
  'IO',
  'O3',
  '8/4x4/1',
  '8/4x4/2',
  '8/4x4/4',
  '8/4x8/1',
  '8/4x8/2',
  '8/4x8/4',
  '8/4x8/8',
  '8/4x12/1',
  '8/4x12/2',
  '8/4x12/4',
  '8/4x12/6',
  '8/4x12/12',
  '8/4x16/1',
  '8/4x16/2',
  '8/4x16/4',
  '8/4x16/8',
  '8/4x16/16',
]

num_configs = len( configs )

groups = [
  'IO',
  'O3',
  '32-uthread LTA',
  '64-uthread LTA',
  '96-uthread LTA',
  '128-uthread LTA',
]

# Results (execution time in seconds)

cycle_data = [
  [
    2.99491e+07,  #  io
  ],
  [
    9.5489e+06,   #  o3
  ],
  [
    6.31471e+06,  #  8/4x4/1
    5.32857e+06,  #  8/4x4/2
    6.90972e+06,  #  8/4x4/4
  ],
  [
    6.31905e+06,  #  8/4x8/1
    6.07488e+06,  #  8/4x8/2
    5.00186e+06,  #  8/4x8/4
    4.69305e+06,  #  8/4x8/8
  ],
  [
    6.31945e+06,  #  8/4x12/1
    6.24585e+06,  #  8/4x12/2
    5.30066e+06,  #  8/4x12/4
    4.41921e+06,  #  8/4x12/6
    6.8211e+06,   #  8/4x12/12
  ],
  [
    6.31904e+06,  #  8/4x16/1
    6.28074e+06,  #  8/4x16/2
    5.67829e+06,  #  8/4x16/4
    4.10374e+06,  #  8/4x16/8
    4.68646e+06,  #  8/4x16/16
  ],
]

io_data = cycle_data[0][0]
perf_data = [ io_data / np.array( data ) for data in cycle_data ]

#-------------------------------------------------------------------------
# Plot parameters
#-------------------------------------------------------------------------

# Setup x-axis

spacing = 1.5

idx = 0
indices = []
for i, data in enumerate( cycle_data ):
  indices.append( np.arange( len( data ) ) + idx )
  idx += len( data ) + ( spacing if i > 0 else 0.0 )

# Bar widths

width = 0.05

for i in range( len( indices ) ):
  indices[i] = ( indices[i] + 1 ) * width

# Colors

colors = [
  '#000000',
  '#80FFBF',
  '#CCEBFF',
  '#99D6FF',
  '#66C2FF',
  '#33ADFF',
]

#-------------------------------------------------------------------------
# Create plot
#-------------------------------------------------------------------------

# Initialize figure

fig = plt.figure()
ax  = fig.add_subplot(111)

# Plot formatting

flat_ind = np.array( [ tick for ind in indices for tick in ind ] )

ax.set_xticks( flat_ind+width/2.0 )
ax.set_xticklabels( configs, rotation=90, fontsize=13 )

ax.set_ylabel( 'Speedup', fontsize=16 )
ax.yaxis.set_label_coords( -0.04, 0.5 )
#ax.set_yticks( np.arange( 0, 13, 2 ) )

ax.grid(True)
ax.set_axisbelow(True)

# Set axis limits

plt.axis( xmax=flat_ind[-1]+2*width, ymax=7.5 )

# Add bars for each configuration

rects = []
for i, ( ind, perf ) in enumerate( zip( indices, perf_data ) ):
  rects.append( ax.bar( ind, perf, width, color=colors[i] ) )

# Set tick positions

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Add horizontal line for baseline

plt.axhline( y=1, color='k', linewidth=1.5 )

# Cut-off lines

labels = []
#labels.append( draw_cutoffs( 0.22, 11.8, '13', -0.1 ) )

# Legend

legend = ax.legend(
  rects, groups, loc='lower center', bbox_to_anchor=(0.475, 1.05),
  ncol=3, borderaxespad=0, prop={'size':10}, frameon=True )

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
plt.savefig( output_filename, bbox_extra_artists=(legend,), bbox_inches='tight' )
