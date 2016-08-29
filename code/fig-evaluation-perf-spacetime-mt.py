#=========================================================================
# fig-evaluation-perf-spacetime-mt.py
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

aspect_ratio  = 0.5

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
  x1 = [ init_x, init_x + 0.15 ]
  y1 = [ init_y, init_y + 0.2 ]
  y2 = [ y1[0] - 0.4, y1[1] - 0.4 ]

  plt.plot( x1, y1, color = 'w', linestyle = '-', linewidth = 1 )
  plt.plot( x1, y2, color = 'w', linestyle = '-', linewidth = 1 )

  return ax.annotate(
    label, xy = ( init_x + 0.05 + x_tweak, init_y + 0.3 + y_tweak ),
    horizontalalignment='center',
    verticalalignment='bottom',
    fontsize = 11.0 )

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
#  'avg/area',
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
#  'avg/area',
]

num_bmarks = len( bmarks )

# Configurations

configs = [
  'IO',
  'MC-IO',
  'MC-O3',
#  'MC-LTA-4/2x8/1',
#  'MC-LTA-8/2x4/1',
#  'MC-LTA-8/4x4/1',
  'MC-LTA-4/2x8/2',
#  'MC-LTA-8/2x4/2',
  'MC-LTA-8/4x4/2',
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
#  680345.62, #905239.70,    # LTA-4/2x8/1
#  862954.44, #1087848.52,   # LTA-8/2x4/1
#  774124.82, #999018.90,    # LTA-8/4x4/1
  680345.62, #905239.70,    # LTA-4/2x8/2
#  862954.44, #1087848.52,   # LTA-8/2x4/2
  774124.82, #999018.90,    # LTA-8/4x4/2
]

area_data = [
  core_area[0] + cache_area[0],
  4 * ( core_area[0] + cache_area[0] ),
  4 * ( core_area[1] + cache_area[0] ),
#  4 * ( core_area[2] + cache_area[1] ),
#  4 * ( core_area[3] + cache_area[2] ),
#  4 * ( core_area[3] + cache_area[1] ),
  4 * ( core_area[2] + cache_area[1] ),
#  4 * ( core_area[6] + cache_area[2] ),
  4 * ( core_area[3] + cache_area[1] ),
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

  # io

  [
    1.50793e+07,  #  bilateral-xpc
    2.47686e+07,  #  dct8x8m-xpc
    3.44848e+06,  #  mriq-xpc
    4.65342e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    7.85213e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    2.8046e+07,   #  pbbs-dict-deterministicHash-parc-xpc-small
    7.64268e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    9.51608e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    3.85318e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    2.81444e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    5.72897e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    6.14704e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    3.53858e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    1.80856e+07,  #  rgb2cmyk-xpc
    9.67182e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    3.1286e+07,   #  sgemm-xpc
    8.95889e+06,  #  strsearch-xpc
  ],

  # o3

  [
    5.97651e+06,  #  bilateral-xpc
    1.69157e+07,  #  dct8x8m-xpc
    1.28594e+06,  #  mriq-xpc
    3.24513e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    4.9139e+07,   #  pbbs-bfs-ndBFS-parc-xpc-small
    3.14912e+07,  #  pbbs-dict-deterministicHash-parc-xpc-small
    4.63606e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    6.15649e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    1.93765e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    2.39772e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    5.00547e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    3.27255e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    3.08482e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    1.58093e+07,  #  rgb2cmyk-xpc
    6.87773e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    9.06889e+06,  #  sgemm-xpc
    2.74351e+06,  #  strsearch-xpc
  ],

#  # LTA-4/2x8/1
#
#  [
#    2.32852e+06,  #  bilateral-xpc
#    9.05556e+06,  #  dct8x8m-xpc
#    508209,       #  mriq-xpc
#    1.42276e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
#    4.12393e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
#    7.33219e+06,  #  pbbs-dict-deterministicHash-parc-xpc-small
#    3.28034e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
#    3.71016e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
#    3.31183e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
#    9.50541e+06,  #  pbbs-mis-ndMIS-parc-xpc-small
#    1.87973e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
#    7.09842e+06,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
#    1.08459e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
#    2.98764e+06,  #  rgb2cmyk-xpc
#    4.63514e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
#    4.60057e+06,  #  sgemm-xpc
#    2.59037e+06,  #  strsearch-xpc
#  ],

#  # LTA-8/2x4/1
#
#  [
#    1.629e+06,    #  bilateral-xpc
#    9.31351e+06,  #  dct8x8m-xpc
#    367742,       #  mriq-xpc
#    1.38455e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
#    4.053e+07,    #  pbbs-bfs-ndBFS-parc-xpc-small
#    6.16491e+06,  #  pbbs-dict-deterministicHash-parc-xpc-small
#    3.24905e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
#    3.66004e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
#    3.29419e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
#    8.99955e+06,  #  pbbs-mis-ndMIS-parc-xpc-small
#    1.81732e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
#    5.37236e+06,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
#    9.88249e+06,  #  pbbs-rdups-deterministicHash-parc-xpc-small
#    2.72612e+06,  #  rgb2cmyk-xpc
#    4.59826e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
#    3.53215e+06,  #  sgemm-xpc
#    2.19888e+06,  #  strsearch-xpc
#  ],

#  # LTA-8/4x4/1
#
#  [
#    1.88273e+06,  #  bilateral-xpc
#    8.95337e+06,  #  dct8x8m-xpc
#    391560,       #  mriq-xpc
#    1.22403e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
#    3.88563e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
#    4.45534e+06,  #  pbbs-dict-deterministicHash-parc-xpc-small
#    2.9263e+07,   #  pbbs-isort-blockRadixSort-parc-xpc-small
#    3.38851e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
#    3.19888e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
#    6.34192e+06,  #  pbbs-mis-ndMIS-parc-xpc-small
#    1.78053e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
#    6.47302e+06,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
#    7.28524e+06,  #  pbbs-rdups-deterministicHash-parc-xpc-small
#    2.47459e+06,  #  rgb2cmyk-xpc
#    4.32064e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
#    3.1392e+06,   #  sgemm-xpc
#    1.86561e+06,  #  strsearch-xpc
#  ],

  # LTA-4/2x8/2

  [
    2.17043e+06,  #  bilateral-xpc
    8.9177e+06,   #  dct8x8m-xpc
    457001,       #  mriq-xpc
    1.42737e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    4.07234e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    8.15319e+06,  #  pbbs-dict-deterministicHash-parc-xpc-small
    3.18858e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    3.69758e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    3.3123e+07,   #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    9.51958e+06,  #  pbbs-mis-ndMIS-parc-xpc-small
    1.85928e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    1.16084e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    1.12712e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    3.33391e+06,  #  rgb2cmyk-xpc
    4.85895e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    3.94018e+06,  #  sgemm-xpc
    1.9732e+06,   #  strsearch-xpc
  ],

#  # LTA-8/2x4/2
#
#  [
#    1.54287e+06,  #  bilateral-xpc
#    9.32881e+06,  #  dct8x8m-xpc
#    360999,       #  mriq-xpc
#    1.39413e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
#    4.04172e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
#    6.37968e+06,  #  pbbs-dict-deterministicHash-parc-xpc-small
#    3.25449e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
#    4.03811e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
#    3.29563e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
#    9.1596e+06,   #  pbbs-mis-ndMIS-parc-xpc-small
#    1.81572e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
#    7.07094e+06,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
#    1.03598e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
#    3.29111e+06,  #  rgb2cmyk-xpc
#    4.54463e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
#    3.22693e+06,  #  sgemm-xpc
#    1.78001e+06,  #  strsearch-xpc
#  ],

  # LTA-8/4x4/2

  [
    1.84654e+06,  #  bilateral-xpc
    8.86548e+06,  #  dct8x8m-xpc
    377628,       #  mriq-xpc
    1.22012e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    3.88795e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    4.77974e+06,  #  pbbs-dict-deterministicHash-parc-xpc-small
    3.02327e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    3.59192e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    3.19622e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    6.40907e+06,  #  pbbs-mis-ndMIS-parc-xpc-small
    1.77926e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    7.72569e+06,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    7.74767e+06,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    3.19688e+06,  #  rgb2cmyk-xpc
    4.52065e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    2.78036e+06,  #  sgemm-xpc
    1.54934e+06,  #  strsearch-xpc
  ],

]

perf_data = [ np.array( [ float(i) for i in cycle_data[0] ] ) / np.array( data )
              for data in cycle_data ]

perf_area_data = [ perf * ( area_data[0] / float( area ) )
                   for perf, area in zip( perf_data, area_data ) ]

for i, ( perf, perf_area ) in enumerate( zip( perf_data, perf_area_data ) ):
  perf_avg = sum( perf ) / ( num_bmarks - 1 )
  perf_area_avg = sum( perf_area ) / ( num_bmarks - 1 )
  perf_data[i] = np.append( perf, [ perf_avg ] ) #, perf_area_avg ] )

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

width = 0.15

# Colors

colors = [
  '#000000',
  '#ffc34d',
  '#80FFBF',

#  '#FFCCCC',
  '#FF9999',
#  '#FF6666',

#  '#CCEBFF',
  '#99D6FF',
#  '#66C2FF',

#  '#E5FFF2',
#  '#B3FFD9',
#  '#80FFBF',
]

#-------------------------------------------------------------------------
# Create plot
#-------------------------------------------------------------------------

# Initialize figure

fig = plt.figure()
ax  = fig.add_subplot(111)

# Plot formatting

ax.set_xticks( ind+mid*width+width )
ax.set_xticklabels( ordered_bmarks, rotation=45, fontsize=12 )
#ax.set_yticks( np.arange( 0.0, 9.2, 1.0 ) )

#ax.set_xlabel( 'Benchmarks', fontsize=16 )
ax.set_ylabel( 'Speedup', fontsize=16 )
ax.yaxis.set_label_coords( -0.04, 0.5 )
ax.set_yticks( np.arange( 0, 36, 4 ) )

ax.grid(True)
ax.set_axisbelow(True)

# Set axis limits

plt.axis( xmax=num_bmarks-1+(num_configs+2)*width, ymax=32.0 )

# Add bars for each configuration

rects = []

for i, perf in enumerate( perf_data ):
  rects.append( ax.bar( ind+width*i+width, perf, width, color=colors[i] ) )

# Set tick positions

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Add horizontal line for baseline

plt.axhline( y=1, color='k', linewidth=1.5 )
plt.axvline( x=num_bmarks-0.975, color='k', linewidth=1.5, linestyle='dashed' )

# Cut-off lines

labels = []
#labels.append( draw_cutoffs( 0.15 + 0.44, 27.6, '34', -0.2 ) )
#labels.append( draw_cutoffs( 0.15 + 0.60, 27.6, '37', 0.2 ) )
labels.append( draw_cutoffs( 0.15 + 1.60, 31.6, '34' ) )
labels.append( draw_cutoffs( 0.15 + 2.60, 31.6, '37' ) )
labels.append( draw_cutoffs( 0.15 + 3.60, 31.6, '42' ) )

# Legend

#legend = ax.legend(
#  rects, configs, loc='upper center', bbox_to_anchor=(0.54,1.13),
#  ncol=2, borderaxespad=0, prop={'size':12}, frameon=True,
#  columnspacing=0.5,
#)

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
