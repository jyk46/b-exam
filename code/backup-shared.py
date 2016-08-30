#=========================================================================
# fig-evaluation-case-shared.py
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

fig_width     = 10.0                          # width in inches
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

# Benchmarks

bmarks = [
  'bilateral',
  'dct8x8m',
  'mriq',
  'bfs-d',
  'bfs-nd',
  'dict',
  'radix-1',
  'radix-2',
  'knn',
  'mis',
  'maxmatch',
  'nbody',
  'rdups',
  'rgb2cmyk',
  'sarray',
  'sgemm',
  'strsearch',
  'avg',
  'avg/area',
]

ordered_bmarks = [
  'nbody',
  'bilateral',
  'mriq',
  'sgemm',
  'rgb2cmyk',
  'dct8x8m',
  'knn',
  'bfs-nd',
  'radix-2',
  'radix-1',
  'rdups',
  'sarray',
  'strsearch',
  'bfs-d',
  'dict',
  'mis',
  'maxmatch',
  'avg',
  'avg/area',
]

num_bmarks = len( bmarks )

# Configurations

configs = [
  'IO',
  'O3',
  'LTA-8/1x4/1',
  'LTA-8/2x4/1',
  'LTA-8/4x4/1',
  'LTA-8/8x4/1',
]

num_configs = len( configs )

# Area estimates (um^2)

cache_area = [ # 32KB I$ + 32KB D$ (direct-mapped)
  2 * 262005.78 + 8495.39,   # 1-port crossbar network
  2 * 262005.78 + 24272.54,  # 2-port crossbar network
  2 * 262005.78 + 69350.12,  # 4-port crossbar network
  2 * 262005.78 + 198143.19, # 8-port crossbar network
]

core_area = [
  75981.95,     # io
  75981.95 * 3, # o3
  1019622.7,    # LTA-8/1x4/1
  1044871.28,   # LTA-8/2x4/1
  1047000.08,   # LTA-8/4x4/1
  1051257.68,   # LTA-8/8x4/1
]

area_data = [
  core_area[0] + cache_area[0],
  core_area[1] + cache_area[0],
  core_area[2] + cache_area[1],
  core_area[3] + cache_area[1],
  core_area[4] + cache_area[1],
  core_area[5] + cache_area[1],
]

# Results (execution time in seconds)

cycle_data = [

  # io

  [
    6.21762e+07,  #  bilateral-scalar
    9.6853e+07,   #  dct8x8m-scalar
    1.38979e+07,  #  mriq-scalar
    1.11999e+08,  #  pbbs-bfs-serialBFS-parc-small
    1.11999e+08,  #  pbbs-bfs-serialBFS-parc-small
    1.00005e+08,  #  pbbs-dict-serialHash-parc-small
    2.14937e+08,  #  pbbs-isort-serialRadixSort-parc-small
    1.23254e+08,  #  pbbs-isort-serialRadixSort-parc-small-1
    5.73002e+07,  #  pbbs-knn-serialNeighbors-parc-small
    1.00801e+08,  #  pbbs-mis-serialMIS-parc-small
    2.20669e+08,  #  pbbs-mm-serialMatching-parc-small
    2.39507e+08,  #  pbbs-nbody-serialBarnesHut-parc-small
    1.06215e+08,  #  pbbs-rdups-serialHash-parc-small
    6.24962e+07,  #  rgb2cmyk-scalar
    2.33191e+08,  #  pbbs-sa-serialKS-parc-small
    1.18787e+08,  #  sgemm-scalar
    2.99491e+07,  #  strsearch-scalar
  ],

  # o3

  [
    2.2038e+07,   #  bilateral-scalar
    6.60528e+07,  #  dct8x8m-scalar
    5.23304e+06,  #  mriq-scalar
    4.9687e+07,   #  pbbs-bfs-serialBFS-parc-small
    4.9687e+07,   #  pbbs-bfs-serialBFS-parc-small
    5.78961e+07,  #  pbbs-dict-serialHash-parc-small
    1.21024e+08,  #  pbbs-isort-serialRadixSort-parc-small
    7.01812e+07,  #  pbbs-isort-serialRadixSort-parc-small-1
    2.59591e+07,  #  pbbs-knn-serialNeighbors-parc-small
    3.83622e+07,  #  pbbs-mis-serialMIS-parc-small
    7.16346e+07,  #  pbbs-mm-serialMatching-parc-small
    1.27389e+08,  #  pbbs-nbody-serialBarnesHut-parc-small
    6.28899e+07,  #  pbbs-rdups-serialHash-parc-small
    4.70559e+07,  #  rgb2cmyk-scalar
    1.00265e+08,  #  pbbs-sa-serialKS-parc-small
    3.58277e+07,  #  sgemm-scalar
    9.5489e+06,   #  strsearch-scalar
  ],

  # LTA-8/1x4/1

  [
    4.01958e+06,  #  bilateral-xpc
    2.08595e+07,  #  dct8x8m-xpc
    1.16403e+06,  #  mriq-xpc
    4.00252e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    6.67766e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    1.88071e+07,  #  pbbs-dict-deterministicHash-parc-xpc-small
    7.71387e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    7.03166e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    4.94318e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    4.1237e+07,   #  pbbs-mis-ndMIS-parc-xpc-small
    4.18723e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    1.57719e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    4.2636e+07,   #  pbbs-rdups-deterministicHash-parc-xpc-small
    9.60028e+06,  #  rgb2cmyk-xpc
    7.96016e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    1.27497e+07,  #  sgemm-xpc
    7.98038e+06,  #  strsearch-xpc
  ],

  # LTA-8/2x4/1

  [
    4.42022e+06,  #  bilateral-xpc
    1.53853e+07,  #  dct8x8m-xpc
    1.1985e+06,   #  mriq-xpc
    3.28052e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    5.81189e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    2.03942e+07,  #  pbbs-dict-deterministicHash-parc-xpc-small
    6.80056e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    6.73469e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    4.62468e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    3.25577e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    3.73233e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    1.73807e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    3.35713e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    9.15442e+06,  #  rgb2cmyk-xpc
    7.2427e+07,   #  pbbs-sa-parallelRange-parc-xpc-small
    1.14256e+07,  #  sgemm-xpc
    7.64605e+06,  #  strsearch-xpc
  ],

  # LTA-8/4x4/1

  [
    4.34132e+06,  #  bilateral-xpc
    1.43362e+07,  #  dct8x8m-xpc
    1.19844e+06,  #  mriq-xpc
    2.55355e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    5.15988e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    1.6484e+07,   #  pbbs-dict-deterministicHash-parc-xpc-small
    5.92055e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    6.39264e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    4.34632e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    2.38752e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    3.34442e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    1.74269e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    2.73786e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    8.55022e+06,  #  rgb2cmyk-xpc
    6.77677e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    9.20226e+06,  #  sgemm-xpc
    6.31471e+06,  #  strsearch-xpc
  ],

  # LTA-8/8x4/1

  [
    3.93616e+06,  #  bilateral-xpc
    1.14717e+07,  #  dct8x8m-xpc
    1.15704e+06,  #  mriq-xpc
    1.93972e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    4.6336e+07,   #  pbbs-bfs-ndBFS-parc-xpc-small
    1.24771e+07,  #  pbbs-dict-deterministicHash-parc-xpc-small
    5.29709e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    5.91414e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    4.16698e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    1.50062e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    2.65977e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    1.69848e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    1.84192e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    8.91107e+06,  #  rgb2cmyk-xpc
    6.20964e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    9.43012e+06,  #  sgemm-xpc
    5.39125e+06,  #  strsearch-xpc
  ],

]

perf_data = [ np.array( [ float(i) for i in cycle_data[0] ] ) / np.array( data )
              for data in cycle_data ]

perf_area_data = [ perf * ( area_data[0] / float( area ) )
                   for perf, area in zip( perf_data, area_data ) ]

for i, ( perf, perf_area ) in enumerate( zip( perf_data, perf_area_data ) ):
  perf_avg = sum( perf ) / ( num_bmarks - 2 )
  perf_area_avg = sum( perf_area ) / ( num_bmarks - 2 )
  perf_data[i] = np.append( perf, [ perf_avg, perf_area_avg ] )

# Reorder bmarks

for i, data in enumerate( perf_data ):
  tmp_data = []
  for bmark in ordered_bmarks:
    tmp_data.append( data[bmarks.index( bmark )] )
  perf_data[i] = tmp_data

#-------------------------------------------------------------------------
# Plot parameters
#-------------------------------------------------------------------------

# Setup x-axis

ind = np.arange( num_bmarks )
mid = num_configs / 2.0

# Bar widths

width = 0.10

# Colors

colors = [
  '#000000',
#  '#F0B3FF',
  '#80FFBF',
#  '#FFCCCC',
#  '#FF9999',
#  '#FF6666',
#  '#E5FFF2',
#  '#B3FFD9',
#  '#80FFBF',
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

ax.set_xticks( ind+mid*width+width )
ax.set_xticklabels( ordered_bmarks, rotation=45, fontsize=14 )
#ax.set_yticks( np.arange( 0.0, 9.2, 1.0 ) )

#ax.set_xlabel( 'Benchmarks', fontsize=16 )
ax.set_ylabel( 'Speedup', fontsize=16 )
ax.yaxis.set_label_coords( -0.035, 0.5 )
ax.set_yticks( np.arange( 0, 16, 2 ) )

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
plt.axvline( x=num_bmarks-2, color='k', linewidth=1.5, linestyle='dashed' )

# Cut-off lines

labels = []
#labels.append( draw_cutoffs( 0.22, 11.8, '13', -0.1 ) )
#labels.append( draw_cutoffs( 0.46, 11.8, '15', 0.15 ) )
#labels.append( draw_cutoffs( 1.46, 11.8, '16' ) )

# Legend

legend = ax.legend(
  rects, configs, loc='lower center', bbox_to_anchor=(0.475,1.05),
  ncol=6, borderaxespad=0, prop={'size':10}, frameon=True,
  labelspacing=0.75,
  columnspacing=0.75,
  handletextpad=0.75,
  borderpad=0.75
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
plt.savefig( output_filename, bbox_extra_artists=(legend,), bbox_inches='tight' )
