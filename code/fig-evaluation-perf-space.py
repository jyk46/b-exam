#=========================================================================
# fig-evaluation-perf-space.py
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
  'LTA-4/1x8/1',
  'LTA-4/2x8/1',
  'LTA-4/4x8/1',
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
  746055.46, #970949.54,    # LTA-4/1x8/1
  680345.62, #905239.70,    # LTA-4/2x8/1
  636995.21, #861889.29,    # LTA-4/4x8/1
  1019622.7, #1244516.78,   # LTA-8/1x4/1
  862954.44, #1087848.52,   # LTA-8/2x4/1
  774124.82, #999018.90,    # LTA-8/4x4/1
  732903.21, #957797.29,    # LTA-8/8x4/1
]

area_data = [
  core_area[0] + cache_area[0],
  core_area[1] + cache_area[0],
  core_area[2] + cache_area[2],
  core_area[3] + cache_area[1],
  core_area[4] + cache_area[0],
  core_area[5] + cache_area[3],
  core_area[6] + cache_area[2],
  core_area[7] + cache_area[1],
  core_area[8] + cache_area[0],
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

  # LTA-4/1x8/1

  [
    5.46224e+06,  #  bilateral-xpc
    2.52045e+07,  #  dct8x8m-xpc
    1.67079e+06,  #  mriq-xpc
    4.15598e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    6.89339e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    2.12606e+07,  #  pbbs-dict-deterministicHash-parc-xpc-small
    7.85329e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    7.08254e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    5.01518e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    4.33168e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    4.4625e+07,   #  pbbs-mm-ndMatching-parc-xpc-small
    1.91717e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    4.54065e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    1.08412e+07,  #  rgb2cmyk-xpc
    8.08117e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    1.57291e+07,  #  sgemm-xpc
    1.0382e+07,   #  strsearch-xpc
  ],

  # LTA-4/2x8/1

  [
    9.22017e+06,  #  bilateral-xpc
    2.33754e+07,  #  dct8x8m-xpc
    1.93217e+06,  #  mriq-xpc
    3.56515e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    6.0832e+07,   #  pbbs-bfs-ndBFS-parc-xpc-small
    2.85791e+07,  #  pbbs-dict-deterministicHash-parc-xpc-small
    6.90154e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    6.75429e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    4.90623e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    3.67955e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    4.40686e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    2.6983e+07,   #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    4.16018e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    1.01901e+07,  #  rgb2cmyk-xpc
    7.7595e+07,   #  pbbs-sa-parallelRange-parc-xpc-small
    1.64291e+07,  #  sgemm-xpc
    9.2244e+06,   #  strsearch-xpc
  ],

  # LTA-4/4x8/1

  [
    1.36042e+07,  #  bilateral-xpc
    3.58641e+07,  #  dct8x8m-xpc
    2.28518e+06,  #  mriq-xpc
    2.65584e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    5.34201e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    2.00578e+07,  #  pbbs-dict-deterministicHash-parc-xpc-small
    6.01588e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    6.44666e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    4.59117e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    2.49205e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    3.68213e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    4.38329e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    3.02481e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    9.62343e+06,  #  rgb2cmyk-xpc
    7.00787e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    1.65616e+07,  #  sgemm-xpc
    6.77705e+06,  #  strsearch-xpc
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
    6.39428e+06,  #  bilateral-xpc
    1.72825e+07,  #  dct8x8m-xpc
    1.37428e+06,  #  mriq-xpc
    3.37439e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    5.88742e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    2.37387e+07,  #  pbbs-dict-deterministicHash-parc-xpc-small
    6.79575e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    6.71529e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    4.80171e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    3.46944e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    3.90664e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    2.03096e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    3.7668e+07,   #  pbbs-rdups-deterministicHash-parc-xpc-small
    9.08387e+06,  #  rgb2cmyk-xpc
    7.45908e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    1.26451e+07,  #  sgemm-xpc
    7.79992e+06,  #  strsearch-xpc
  ],

  # LTA-8/4x4/1

  [
    7.41608e+06,  #  bilateral-xpc
    2.00253e+07,  #  dct8x8m-xpc
    1.5038e+06,   #  mriq-xpc
    2.55355e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    5.15988e+07,  #  pbbs-bfs-ndBFS-parc-xpc-small
    1.6484e+07,   #  pbbs-dict-deterministicHash-parc-xpc-small
    5.92133e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    6.39264e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    4.49455e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    2.38752e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    3.34442e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    2.61732e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    2.73786e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    8.55007e+06,  #  rgb2cmyk-xpc
    6.77677e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    1.08749e+07,  #  sgemm-xpc
    6.31471e+06,  #  strsearch-xpc
  ],

  # LTA-8/8x4/1

  [
    1.34413e+07,  #  bilateral-xpc
    3.52445e+07,  #  dct8x8m-xpc
    2.10226e+06,  #  mriq-xpc
    1.93972e+07,  #  pbbs-bfs-deterministicBFS-parc-xpc-small
    4.6336e+07,   #  pbbs-bfs-ndBFS-parc-xpc-small
    1.24771e+07,  #  pbbs-dict-deterministicHash-parc-xpc-small
    5.29688e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small
    5.91383e+07,  #  pbbs-isort-blockRadixSort-parc-xpc-small-1
    4.31125e+07,  #  pbbs-knn-octTree2Neighbors-parc-xpc-small
    1.50062e+07,  #  pbbs-mis-ndMIS-parc-xpc-small
    2.65977e+07,  #  pbbs-mm-ndMatching-parc-xpc-small
    4.08803e+07,  #  pbbs-nbody-parallelBarnesHut-parc-xpc-small
    1.84192e+07,  #  pbbs-rdups-deterministicHash-parc-xpc-small
    8.9109e+06,   #  rgb2cmyk-xpc
    6.20944e+07,  #  pbbs-sa-parallelRange-parc-xpc-small
    1.4835e+07,   #  sgemm-xpc
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

width = 0.08

# Colors

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
ax.set_ylabel( 'Speedup', fontsize=14 )
ax.yaxis.set_label_coords( -0.02, 0.5 )
ax.set_yticks( np.arange( 0, 13, 2 ) )

ax.grid(True)
ax.set_axisbelow(True)

# Set axis limits

plt.axis( xmax=num_bmarks-1+(num_configs+2)*width, ymax=12.0 )

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
labels.append( draw_cutoffs( 0.22, 11.8, '12.5', -0.05 ) )
labels.append( draw_cutoffs( 0.46, 11.8, '15.2', 0.3 ) )
labels.append( draw_cutoffs( 1.46, 11.8, '15.5' ) )

# Legend

#legend = ax.legend(
#  rects, configs, loc='upper center', bbox_to_anchor=(0.55,1.05),
#  ncol=5, borderaxespad=0, prop={'size':11}, frameon=True
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
plt.savefig( output_filename, bbox_extra_artists=(labels[0],), bbox_inches='tight' )
