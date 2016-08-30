#=========================================================================
# fig-evaluation-eeperf-time
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

aspect_ratio  = 2.13

fig_width     = 4.8                           # width in inches
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
  'sgemm',
  'strsearch',
  'mis',
]

num_bmarks = len( bmarks )

# Configurations

configs = [
  'io',
  'o3',
  '4/2x8/1',
  '4/2x8/2',
  '4/2x8/4',
  '4/2x8/8',
#  '8/2x4/1',
#  '8/2x4/2',
#  '8/2x4/4',
  '8/4x4/1',
  '8/4x4/2',
  '8/4x4/4',
]

num_configs = len( configs )

# Energy results

energy_data = [

  # bilateral

  [
    1321694465.7,
    2506392584.32,
    950920651.04,
    992053233.82,
    1074040986.1,
    1233678459.08,
    883914872.96,
    963933101.94,
    1117538784.76,
  ],

  # sgemm

  [
    4023695428.1,
    7452342218.28,
    2130967050.68,
    2233935054.78,
    2431838032.66,
    2803001272.42,
    2223257058.1,
    2418772149.88,
    2808407040.48,
  ],

  # strsearch

  [
    1073602322.5,
    2092823102.45,
    606284126.52,
    632683505.6,
    687886753.36,
    739122389.56,
    707431514.24,
    727802667.32,
    836639155.24,
  ],

  # mis

  [
    1113349568.7,
    3265106582.35,
    1816066937.26,
    1995956219.84,
    2059938503.42,
    2231117965.58,
    1785899008.24,
    1938007878.14,
    1993698563.3,
  ],

]

# Cycle results

cycle_data = [

  # bilateral

  [
    6.21762e+07,  # io
    2.2038e+07,   # o3
    9.22017e+06,  # LTA-4/2x8/1
    8.63051e+06,  # LTA-4/2x8/2
    8.78448e+06,  # LTA-4/2x8/4
    1.04195e+07,  # LTA-4/2x8/8
#    6.39428e+06,  # LTA-8/2x4/1
#    6.06101e+06,  # LTA-8/2x4/2
#    7.15091e+06,  # LTA-8/2x4/4
    7.41608e+06,  # LTA-8/4x4/1
    7.24986e+06,  # LTA-8/4x4/2
    7.81463e+06,  # LTA-8/4x4/4
  ],

  # sgemm

  [
    1.18787e+08,  # io
    3.58277e+07,  # o3
    1.64291e+07,  # LTA-4/2x8/1
    1.38198e+07,  # LTA-4/2x8/2
    1.51311e+07,  # LTA-4/2x8/4
    2.16114e+07,  # LTA-4/2x8/8
    1.08749e+07,  # LTA-8/4x4/1
    9.85516e+06,  # LTA-8/4x4/2
    1.25951e+07,  # LTA-8/4x4/4
  ],

  # strsearch

  [
    2.99491e+07,  # io
    9.5489e+06,   # o3
    9.2244e+06,   # LTA-4/2x8/1
    6.9701e+06,   # LTA-4/2x8/2
    7.89144e+06,  # LTA-4/2x8/4
    8.63648e+06,  # LTA-4/2x8/8
#    7.79992e+06,  # LTA-8/2x4/1
#    6.27728e+06,  # LTA-8/2x4/2
#    8.01205e+06,  # LTA-8/2x4/4
    6.31471e+06,  # LTA-8/4x4/1
    5.32857e+06,  # LTA-8/4x4/2
    6.90972e+06,  # LTA-8/4x4/4
  ],

  # mis

  [
    1.00801e+08,  # io
    3.83622e+07,  # o3
    3.67955e+07,  # LTA-4/2x8/1
    3.69622e+07,  # LTA-4/2x8/2
    3.65907e+07,  # LTA-4/2x8/4
    3.93823e+07,  # LTA-4/2x8/8
    2.38752e+07,  # LTA-8/4x4/1
    2.38952e+07,  # LTA-8/4x4/2
    2.32631e+07,  # LTA-8/4x4/4
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
  '#FF3333',
  '#CCEBFF',
  '#99D6FF',
  '#66C2FF',
  '#E5FFF2',
  '#B3FFD9',
  '#80FFBF',
]

markers = [
  '.',
  'o',
  '^',
  's',
  'p',
  'h',
  '^',
  's',
  'p',
  '^',
  's',
  'p',
#  's',
#  's',
#  's',
#  's',
#  '^',
#  '^',
#  '^',
#  'p',
#  'p',
#  'p',
]

#-------------------------------------------------------------------------
# Create plot
#-------------------------------------------------------------------------

# Initialize figure

fig, axes = plt.subplots( num_bmarks, 1 )

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

flat_axes = axes #[ ax for dim in axes for ax in dim ]

plots = []
for i, ( ax, perf, eff ) in enumerate( zip( flat_axes, norm_perf, norm_eff ) ):
  for xval, yval, marker, color in zip( perf, eff, markers, colors ):
    sct = ax.scatter( xval, yval, marker=marker, c=color, s=50 )
    if i == 0:
      plots.append( sct )

  ax.plot( perf[2:6], eff[2:6], c=colors[5] )
  ax.plot( perf[6:9], eff[6:9], c=colors[8] )
#  ax.plot( perf[9:12], eff[9:12], c=colors[11] )

# Power curve

#for ax in axes:
#  for i in range( 10 ):
#    ax.plot( [0.0,10.0*i], [0.0,10.0], color = '#cccccc', linestyle = '-', linewidth = 1.0 )

# Legend

legend = full_ax.legend(
  plots, configs, loc='lower center', bbox_to_anchor=(0.45, 1.04),
  ncol=3, borderaxespad=0, prop={'size':10}, frameon=True,
  scatterpoints=1,
  labelspacing=0.5,
  columnspacing=0.5,
  handletextpad=0.5,
  borderpad=0.5
)

# Titles

for ax, bmark in zip( flat_axes, bmarks ):
  ax.set_title( bmark, fontsize=16 )

# Plot formatting

full_ax.set_xlabel( 'Performance', fontsize=16 )
full_ax.set_ylabel( 'Energy Efficiency', fontsize=16 )

#full_ax.yaxis.set_label_coords( -0.1, 0.5 )

# Pretty layout

plt.tight_layout( w_pad=0.1, h_pad=0.1 )

# Axes formatting

for i, ax in enumerate( flat_axes ):
  xmin = 0.88
  xmax = max( norm_perf[i] ) + 0.5
  ymin = 0.45 if i < 3 else 0.30
  ymax = max( norm_eff[i] ) + 0.1
  ax.set_xticks( np.arange( 0.0, xmax, 1.0 ) )
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
