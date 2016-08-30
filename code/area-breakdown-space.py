#=========================================================================
# area-breakdown-space
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

fig_width_pt  = 244.0
inches_per_pt = 1.0/72.27                     # convert pt to inch

aspect_ratio  = 0.80

fig_width     = 9.0                           # width in inches
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
# Raw data
#-------------------------------------------------------------------------

# Configurations

configs = [
  'IO',
  '4/1x8/1',
  '4/2x8/1',
  '4/4x8/1',
  '8/1x4/1',
  '8/2x4/1',
  '8/4x4/1',
  '8/8x4/1',
]

num_configs = len( configs )

# Component groups

groups = [
  'pib',
  'tmu',
  'rf',
  'slfu',
  'llfu',
  'lsu',
  'wq',
  'dcache',
  'icache',
  'gpp',
]

groups.reverse()

# Results

total_area = [
  0.61,
  1.34 + 0.076,
  1.23 + 0.076,
  1.17 + 0.076,
  1.74 + 0.076,
  1.46 + 0.076,
  1.32 + 0.076,
  1.27 + 0.076,
]

area_data = [

  # IO

  [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.44,
    0.43,
    0.13,
  ],

  # 4/1x8/1

  [
    0.95 * 0.00075,
    0.95 * 0.0,
    0.95 * 0.18,
    0.95 * 0.06,
    0.95 * 0.14,
    0.95 * 0.02,
    0.95 * 0.14,
    0.95 * 0.25,
    0.95 * 0.20,
    0.05,
  ],

  # 4/2x8/1

  [
    0.94 * 0.0016,
    0.94 * 0.02,
    0.94 * 0.22,
    0.94 * 0.07,
    0.94 * 0.07,
    0.94 * 0.02,
    0.94 * 0.15,
    0.94 * 0.23,
    0.94 * 0.21,
    0.06,
  ],

  # 4/4x8/1

  [
    0.94 * 0.0034,
    0.94 * 0.02,
    0.94 * 0.22,
    0.94 * 0.07,
    0.94 * 0.04,
    0.94 * 0.03,
    0.94 * 0.16,
    0.94 * 0.23,
    0.94 * 0.22,
    0.06,
  ],

  # 8/1x4/1

  [
    0.96 * 0.00059,
    0.96 * 0.0,
    0.96 * 0.16,
    0.96 * 0.09,
    0.96 * 0.20,
    0.96 * 0.02,
    0.96 * 0.11,
    0.96 * 0.26,
    0.96 * 0.15,
    0.04,
  ],

  # 8/2x4/1

  [
    0.95 * 0.0014,
    0.95 * 0.02,
    0.95 * 0.17,
    0.95 * 0.10,
    0.95 * 0.12,
    0.95 * 0.02,
    0.95 * 0.13,
    0.95 * 0.25,
    0.95 * 0.18,
    0.05,
  ],

  # 8/4x4/1

  [
    0.95 * 0.003,
    0.95 * 0.02,
    0.95 * 0.19,
    0.95 * 0.12,
    0.95 * 0.07,
    0.95 * 0.02,
    0.95 * 0.14,
    0.95 * 0.23,
    0.95 * 0.20,
    0.05,
  ],

  # 8/8x4/1

  [
    0.94 * 0.0063,
    0.94 * 0.02,
    0.94 * 0.21,
    0.94 * 0.13,
    0.94 * 0.04,
    0.94 * 0.02,
    0.94 * 0.15,
    0.94 * 0.21,
    0.94 * 0.21,
    0.06,
  ],

]

# Calculate absolute group area

results = []
for area, total in zip( area_data, total_area ):
  results.append( np.array( area ) * total )

area_data = zip( *results )[::-1]

#-------------------------------------------------------------------------
# Plot parameters
#-------------------------------------------------------------------------

# Setup x-axis

ind = np.arange( num_configs )

# Bar widths

width = 0.35

# Colors

colors = {
  'gpp'     : '#000000',
  'icache'  : '#f2e6ff',
  'dcache'  : '#0073e6',
  'pib'     : '#bd80ff',
  'tmu'     : '#00b359',
  'rf'      : '#ff3333',
  'slfu'    : '#ffff99',
  'llfu'    : '#ffcc66',
  'lsu'     : '#99ccff',
  'wq'      : '#cc0000',
}

#-------------------------------------------------------------------------
# Create plot
#-------------------------------------------------------------------------

# Initialize figure

fig = plt.figure()
ax  = fig.add_subplot(111)

# Create stacked bar plots

rects = []
y_offset = np.array( [ 0.0 ] * num_configs )
for group, area in zip( groups, area_data ):
  bar = ax.bar(
    ind+width/2.0, area, width, color=colors[group], bottom=y_offset )
  y_offset += area
  rects.append( bar[0] )

# Legend

legend = ax.legend(
  rects[::-1], groups[::-1], loc='center left', bbox_to_anchor=(1.02, 0.5),
  ncol=1, borderaxespad=0, prop={'size':14}, frameon=True
)

# Plot labels

xmin = 0.0
xmax = num_configs
ymin = 0.0
ymax = 1.85
ax.set_xticks( ind+width )
ax.set_xticklabels( configs, rotation=0, fontsize=14 )
ax.set_yticks( np.arange( 0.0, ymax, 0.2 ) )
ax.set_xlim( xmin, xmax )
ax.set_ylim( ymin, ymax )

# Plot formatting

ax.set_ylabel( 'Area (mm^2)', fontsize=16 )

# Pretty layout

plt.tight_layout()

# Axes formatting

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
