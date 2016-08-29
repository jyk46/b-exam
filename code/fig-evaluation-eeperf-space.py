#=========================================================================
# fig-evaluation-eeperf-space
#=========================================================================

import matplotlib.pyplot as plt
import math
import sys
import os.path

import numpy
import numpy as np

#-------------------------------------------------------------------------
# Calculate figure size
#-------------------------------------------------------------------------
# We determine the fig_width_pt by using \showthe\columnwidth in LaTeX
# and copying the result into the script. Change the aspect ratio as
# necessary.

fig_width_pt  = 768.0
inches_per_pt = 1.0/72.27                     # convert pt to inch

aspect_ratio  = 0.5

fig_width     = 7.8                           # width in inches
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
# Get data
#-------------------------------------------------------------------------

# Benchmarks

bmarks = [
  'bilateral',
  'strsearch',
]

num_bmarks = len( bmarks )

# Configurations

configs = [
  'io',
  'o3',
  '4/1x8/1',
  '4/2x8/1',
  '4/4x8/1',
  '8/1x4/1',
  '8/2x4/1',
  '8/4x4/1',
  '8/8x4/1',
]

num_configs = len( configs )

# Energy results

energy_data = [

  # bilateral

  [
    1321694465.7,
    2506392584.32,
    663007605.62 - 12053968.325,
    867145085.24,
    866983138.58,
    659045147.66 - 12134339.744,
    904477482.58,
    883914872.96,
    904486947.86,
  ],

  # strsearch

  [
    1073602322.5,
    2092823102.45,
    614451161.48 - 53424701.663,
    606284126.52,
    696057840.32,
    666632826.36 - 53319701.925,
    632172782.8,
    707431514.24,
    836457421.8,
  ],

]

# Cycle results

cycle_data = [

  # bilateral

  [
    6.21762e+07,  # io
    2.2038e+07,   # o3
    5.46224e+06,  # LTA-4/1x8/1
    9.22017e+06,  # LTA-4/2x8/1
    1.36042e+07,  # LTA-4/4x8/1
    4.01958e+06,  # LTA-8/1x4/1
    6.39428e+06,  # LTA-8/2x4/1
    7.41608e+06,  # LTA-8/4x4/1
    1.34413e+07,  # LTA-8/8x4/1
  ],

  # strsearch

  [
    2.99491e+07,  # io
    9.5489e+06,   # o3
    1.0382e+07,   # LTA-4/1x8/1
    9.2244e+06,   # LTA-4/2x8/1
    6.77705e+06,  # LTA-4/4x8/1
    7.98038e+06,  # LTA-8/1x4/1
    7.79992e+06,  # LTA-8/2x4/1
    6.31471e+06,  # LTA-8/4x4/1
    5.39125e+06,  # LTA-8/8x4/1
  ],

]

#-------------------------------------------------------------------------
# Plot parameters
#-------------------------------------------------------------------------

colors = [
  '#000000',
#  '#F0B3FF',
  '#80FFBF',
  '#FFCCCC',
  '#FF9999',
  '#FF6666',
#  '#E5FFF2',
#  '#B3FFD9',
#  '#80FFBF',
  '#CCEBFF',
  '#99D6FF',
  '#66C2FF',
  '#33ADFF',
]

markers = [
  '.',
  'o',
  '^',
  's',
  'p',
  '^',
  's',
  'p',
  'h',
#  's',
#  's',
#  's',
#  '^',
#  '^',
#  '^',
#  '^',
]

#-------------------------------------------------------------------------
# Create plot
#-------------------------------------------------------------------------

# Initialize figure

fig, axes = plt.subplots( 1, num_bmarks )

# Hack to get pointer to axes for full plot
full_ax = fig.add_subplot( 111 )
full_ax.spines['top'].set_color( 'none' )
full_ax.spines['bottom'].set_color( 'none' )
full_ax.spines['left'].set_color( 'none' )
full_ax.spines['right'].set_color( 'none' )
full_ax.set_axis_bgcolor( 'none' )
full_ax.tick_params(
  labelcolor='none', top='off', bottom='off', left='off', right='off' )

# Convert the python lists into numpy arrays

np_cycles = [ np.array( data ) for data in cycle_data ]
np_energy = [ np.array( data ) for data in energy_data ]

# Calulate our perfomance and energy

task_sec   = [ 1.0 / data for data in np_cycles ]
energy_eff = [ 1.0 / data for data in np_energy ]

# Normalize results to reference design

norm_perf = []
norm_eff  = []

for perf, eff in zip( task_sec, energy_eff ):
  ref_perf = perf[0]
  ref_eff  = eff[0]
  norm_perf.append( perf / ref_perf )
  norm_eff.append( eff / ref_eff )

# Create scatter plots

plots = []
for i, ( ax, perf, eff ) in enumerate( zip( axes, norm_perf, norm_eff ) ):
  for xval, yval, marker, color in zip( perf, eff, markers, colors ):
    sct = ax.scatter( xval, yval, marker=marker, c=color, s=50 )
    if i == 0:
      plots.append( sct )

  ax.plot( perf[2:5], eff[2:5], c=colors[4] )
  ax.plot( perf[5:9], eff[5:9], c=colors[8] )

# Power curve

#for ax in axes:
#  for i in range( 10 ):
#    ax.plot( [0.0,10.0*i], [0.0,10.0], color = '#cccccc', linestyle = '-', linewidth = 1.0 )

# Legend

legend = full_ax.legend(
  plots, configs, loc='center left', bbox_to_anchor=(1.02, 0.5),
  ncol=1, borderaxespad=0, prop={'size':12}, frameon=True,
#  scatterpoints=1, labelspacing=0.2, columnspacing=0.2,
#  handletextpad=0, borderpad=0.2
)

# Titles

for ax, bmark in zip( axes, bmarks ):
  ax.set_title( bmark, fontsize=16 )

# Plot formatting

full_ax.set_xlabel( 'Performance', fontsize=16 )
full_ax.set_ylabel( 'Energy Efficiency', fontsize=16 )

#full_ax.yaxis.set_label_coords( -0.1, 0.5 )

# Pretty layout

plt.tight_layout( w_pad=0.1 )

# Axes formatting

for i, ax in enumerate( axes ):
  xmin = 0.88
  xmax = max( norm_perf[i] ) + 0.5
  ymin = 0.45
  ymax = max( norm_eff[i] ) + 0.1
  ax.set_xticks( np.arange( 0.0, xmax, 2.0 if i == 0 else 1.0 ) )
  ax.set_yticks( np.arange( 0.0, ymax, 0.2 ) )
  ax.set_xlim( xmin, xmax )
  ax.set_ylim( ymin, ymax )

  ax.plot([xmin, xmax], [1.0, 1.0], linestyle='dashed', color='black')
  ax.plot([1.0, 1.0], [ymin, ymax], linestyle='dashed', color='black')

  ax.grid(b=True, which='major')
  ax.grid(b=True, which='minor')
  ax.set_axisbelow(True)
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
