#=========================================================================
# fig-evaluation-ebreak-time
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
# Raw data
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
  '4/2x8/1',
  '4/2x8/2',
  '4/2x8/4',
  '4/2x8/8',
  '8/2x4/1',
  '8/2x4/2',
  '8/2x4/4',
]

num_configs = len( configs )

# Components

comps = [
  'alu',
  'muldiv',
  'fpu',

  'regfile_rd',
  'regfile_wr',

  'fetch/decode',
  'rename',
  'rob',
  'iq',
  'lsq',
  'bpred',
  'agen',
  'memdep',
#  'bypass/pipereg',

  'icache_rd',
  'dcache_rd',
  'dcache_wr',
  'l2cache',

  'tpa-dataq',
  'tpa-l0',
  'tpa-pvfb',
  'tpa-rt',
  'tpa-tmu',

  'leak',
]

comps.reverse()

num_comps = len( comps )

# Component groups

group_names = [
  'icache',
  'pib',
  'tmu',
  'front',
  'rf',
  'rt/rob',
  'slfu',
  'llfu',
  'lsu',
  'dcache',
#  'l2cache',
#  'pipereg',
]

group_names.reverse()

groups = {
  'icache'  : [ 'icache_rd' ],
  'pib'     : [ 'tpa-l0' ],
  'tmu'     : [ 'tpa-tmu' ],
  'front'   : [ 'fetch/decode', 'iq', 'bpred', 'tpa-pvfb' ],
  'rf'      : [ 'regfile_rd', 'regfile_wr' ],
  'rt/rob'  : [ 'rename', 'tpa-rt', 'rob' ],
  'slfu'    : [ 'alu' ],
  'llfu'    : [ 'muldiv', 'fpu' ],
  'lsu'     : [ 'lsq', 'agen', 'memdep', 'tpa-dataq' ],
  'dcache'  : [ 'dcache_rd', 'dcache_wr' ],
#  'l2cache' : [ 'l2cache' ],
#  'pipereg' : [ 'bypass/pipereg' ],
}

# Results

scale_factor = 1.0 # rough estimate of savings with L0 on io/o3

energy_dic = [

  # bilateral
  [
    {
        "agen": 3207382.4,
        "alu": 21156272.5,
        "bpred": 0.0,
        "bypass/pipereg": 200966265.0,
        "dcache_rd": 195638491.5,
        "dcache_wr": 27628937.4,
        "fetch/decode": 80386506.0,
        "fpu": 123865749.2,
        "icache_rd": 809230647.6 / scale_factor,
        "iq": 0.0,
        "l2cache": 8905564.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 600138.3,
        "regfile_rd": 32070776.0,
        "regfile_wr": 19004000.0,
        "rename": 0.0,
        "rob": 0.0,
        "tpa-dataq": 0.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 0.0,
        "tpa-rt": 0.0,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 3207648.0,
        "alu": 21156690.0,
        "bpred": 71216656.4,
        "bypass/pipereg": 141726950.83,
        "dcache_rd": 181909890.5,
        "dcache_wr": 27635368.9,
        "fetch/decode": 78068799.0,
        "fpu": 123865759.4,
        "icache_rd": 785898343.0 / scale_factor,
        "iq": 307416883.6,
        "l2cache": 8906014.4,
        "leak": 0.0,
        "lsq": 93342556.8,
        "memdep": 30839214.96,
        "muldiv": 600147.6,
        "regfile_rd": 137978015.76,
        "regfile_wr": 74116030.56,
        "rename": 281287569.92,
        "rob": 278946995.52,
        "tpa-dataq": 0.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 0.0,
        "tpa-rt": 0.0,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 260.0,
        "alu": 43391603.0,
        "bpred": 0.0,
        "bypass/pipereg": 27626580.0,
        "dcache_rd": 337580067.56,
        "dcache_wr": 112156619.4,
        "fetch/decode": 5526972.0,
        "fpu": 182710752.0,
        "icache_rd": 9296512.8,
        "iq": 0.0,
        "l2cache": 1070929.6,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 109139398.7,
        "regfile_wr": 59619287.48,
        "rename": 0.0,
        "rob": 42574366.4,
        "tpa-dataq": 8452598.7,
        "tpa-l0": 31122670.4,
        "tpa-pvfb": 779492.0,
        "tpa-rt": 4969220.8,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 260.0,
        "alu": 43391603.0,
        "bpred": 0.0,
        "bypass/pipereg": 56856165.0,
        "dcache_rd": 337131050.06,
        "dcache_wr": 111476437.5,
        "fetch/decode": 11372889.0,
        "fpu": 182710752.0,
        "icache_rd": 10802406.1,
        "iq": 0.0,
        "l2cache": 1094752.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 109205838.18,
        "regfile_wr": 59619287.48,
        "rename": 0.0,
        "rob": 42574366.4,
        "tpa-dataq": 8452598.7,
        "tpa-l0": 60412382.0,
        "tpa-pvfb": 1092868.0,
        "tpa-rt": 10185843.2,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 260.0,
        "alu": 43391603.0,
        "bpred": 0.0,
        "bypass/pipereg": 115790820.0,
        "dcache_rd": 337218830.06,
        "dcache_wr": 111744664.9,
        "fetch/decode": 23159820.0,
        "fpu": 182710752.0,
        "icache_rd": 11795955.9,
        "iq": 0.0,
        "l2cache": 1099539.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 110114037.26,
        "regfile_wr": 59619287.48,
        "rename": 0.0,
        "rob": 42574366.4,
        "tpa-dataq": 8452598.7,
        "tpa-l0": 117219880.6,
        "tpa-pvfb": 1719620.0,
        "tpa-rt": 20689870.4,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 260.0,
        "alu": 43391603.0,
        "bpred": 0.0,
        "bypass/pipereg": 230973735.0,
        "dcache_rd": 337241297.56,
        "dcache_wr": 112107063.0,
        "fetch/decode": 46196403.0,
        "fpu": 182710752.0,
        "icache_rd": 8845053.5,
        "iq": 0.0,
        "l2cache": 1109004.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 112135162.04,
        "regfile_wr": 59619264.88,
        "rename": 0.0,
        "rob": 42574356.8,
        "tpa-dataq": 8452598.7,
        "tpa-l0": 232289279.6,
        "tpa-pvfb": 2973124.0,
        "tpa-rt": 41503336.0,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 260.0,
        "alu": 41917043.0,
        "bpred": 0.0,
        "bypass/pipereg": 53244255.0,
        "dcache_rd": 283458732.4,
        "dcache_wr": 68267091.0,
        "fetch/decode": 10650507.0,
        "fpu": 182710752.0,
        "icache_rd": 17655178.4,
        "iq": 0.0,
        "l2cache": 1171569.6,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 101882068.62,
        "regfile_wr": 57175450.04,
        "rename": 0.0,
        "rob": 40818001.6,
        "tpa-dataq": 6737193.9,
        "tpa-l0": 58635534.8,
        "tpa-pvfb": 892164.0,
        "tpa-rt": 9413426.4,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 260.0,
        "alu": 41917043.0,
        "bpred": 0.0,
        "bypass/pipereg": 108402000.0,
        "dcache_rd": 283394702.4,
        "dcache_wr": 68238115.4,
        "fetch/decode": 21682056.0,
        "fpu": 182710752.0,
        "icache_rd": 22276895.8,
        "iq": 0.0,
        "l2cache": 1176896.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 101331030.9,
        "regfile_wr": 57175450.04,
        "rename": 0.0,
        "rob": 40818001.6,
        "tpa-dataq": 6737193.9,
        "tpa-l0": 113168716.7,
        "tpa-pvfb": 1547588.0,
        "tpa-rt": 19228500.0,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 260.0,
        "alu": 41917043.0,
        "bpred": 0.0,
        "bypass/pipereg": 216282765.0,
        "dcache_rd": 283344637.4,
        "dcache_wr": 67858047.6,
        "fetch/decode": 43258209.0,
        "fpu": 182710752.0,
        "icache_rd": 25601766.8,
        "iq": 0.0,
        "l2cache": 1178201.6,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 103364639.92,
        "regfile_wr": 57175450.04,
        "rename": 0.0,
        "rob": 40818001.6,
        "tpa-dataq": 6737193.9,
        "tpa-l0": 219097964.9,
        "tpa-pvfb": 2858436.0,
        "tpa-rt": 39088280.8,
        "tpa-tmu": 72.0,
    },
  ],

  # strsearch
  [
    {
        "agen": 3052980.0,
        "alu": 41105387.5,
        "bpred": 0.0,
        "bypass/pipereg": 179115510.0,
        "dcache_rd": 199933079.0,
        "dcache_wr": 3062391.7,
        "fetch/decode": 71646204.0,
        "fpu": 0.0,
        "icache_rd": 721240525.9 / scale_factor,
        "iq": 0.0,
        "l2cache": 112822.4,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 0.0,
        "regfile_rd": 21218283.2,
        "regfile_wr": 12230648.8,
        "rename": 0.0,
        "rob": 0.0,
        "tpa-dataq": 0.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 0.0,
        "tpa-rt": 0.0,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 3178386.4,
        "alu": 41950267.5,
        "bpred": 215003161.568,
        "bypass/pipereg": 61409344.9939,
        "dcache_rd": 208248291.0,
        "dcache_wr": 3073426.8,
        "fetch/decode": 64648917.0,
        "fpu": 0.0,
        "icache_rd": 650803332.5 / scale_factor,
        "iq": 219760574.32,
        "l2cache": 114715.2,
        "leak": 0.0,
        "lsq": 92491044.24,
        "memdep": 28838471.76,
        "muldiv": 0.0,
        "regfile_rd": 100691719.44,
        "regfile_wr": 48641555.04,
        "rename": 207449351.04,
        "rob": 207929888.64,
        "tpa-dataq": 0.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 0.0,
        "tpa-rt": 0.0,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 1099.2,
        "alu": 74416030.5,
        "bpred": 0.0,
        "bypass/pipereg": 71090790.0,
        "dcache_rd": 231720778.84,
        "dcache_wr": 3613873.5,
        "fetch/decode": 14222139.0,
        "fpu": 0.0,
        "icache_rd": 34306077.0,
        "iq": 0.0,
        "l2cache": 386243.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 67983352.78,
        "regfile_wr": 34869990.2,
        "rename": 0.0,
        "rob": 29551379.2,
        "tpa-dataq": 1282287.0,
        "tpa-l0": 96504960.7,
        "tpa-pvfb": 5631325.0,
        "tpa-rt": 11793395.2,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1099.2,
        "alu": 74415841.5,
        "bpred": 0.0,
        "bypass/pipereg": 80809980.0,
        "dcache_rd": 231662753.5,
        "dcache_wr": 3616852.3,
        "fetch/decode": 16165977.0,
        "fpu": 0.0,
        "icache_rd": 54105891.1,
        "iq": 0.0,
        "l2cache": 382108.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 70589046.9,
        "regfile_wr": 34869990.2,
        "rename": 0.0,
        "rob": 29551312.0,
        "tpa-dataq": 1328640.9,
        "tpa-l0": 96027936.6,
        "tpa-pvfb": 6342854.0,
        "tpa-rt": 13622006.4,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1099.2,
        "alu": 74415567.0,
        "bpred": 0.0,
        "bypass/pipereg": 125007315.0,
        "dcache_rd": 231655743.34,
        "dcache_wr": 3603312.3,
        "fetch/decode": 25005444.0,
        "fpu": 0.0,
        "icache_rd": 54243452.6,
        "iq": 0.0,
        "l2cache": 381020.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 72720491.32,
        "regfile_wr": 34869990.2,
        "rename": 0.0,
        "rob": 29551214.4,
        "tpa-dataq": 1341829.5,
        "tpa-l0": 129055487.1,
        "tpa-pvfb": 10052532.0,
        "tpa-rt": 20988374.4,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1099.2,
        "alu": 74415085.5,
        "bpred": 0.0,
        "bypass/pipereg": 197689110.0,
        "dcache_rd": 231663844.06,
        "dcache_wr": 3596948.5,
        "fetch/decode": 39541803.0,
        "fpu": 0.0,
        "icache_rd": 366592.2,
        "iq": 0.0,
        "l2cache": 381020.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 73437776.9,
        "regfile_wr": 34869990.2,
        "rename": 0.0,
        "rob": 29551043.2,
        "tpa-dataq": 1333480.8,
        "tpa-l0": 200645266.6,
        "tpa-pvfb": 16264073.0,
        "tpa-rt": 33053170.4,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1099.2,
        "alu": 74414046.0,
        "bpred": 0.0,
        "bypass/pipereg": 116155260.0,
        "dcache_rd": 231690298.84,
        "dcache_wr": 3657355.5,
        "fetch/decode": 23235033.0,
        "fpu": 0.0,
        "icache_rd": 57902554.7,
        "iq": 0.0,
        "l2cache": 396252.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 65195113.94,
        "regfile_wr": 34868444.36,
        "rename": 0.0,
        "rob": 29550227.2,
        "tpa-dataq": 1279273.8,
        "tpa-l0": 156609483.9,
        "tpa-pvfb": 9487471.0,
        "tpa-rt": 19143664.8,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1099.2,
        "alu": 74413776.0,
        "bpred": 0.0,
        "bypass/pipereg": 129165660.0,
        "dcache_rd": 231621967.68,
        "dcache_wr": 3672520.3,
        "fetch/decode": 25837113.0,
        "fpu": 0.0,
        "icache_rd": 74008427.6,
        "iq": 0.0,
        "l2cache": 400931.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 68991629.18,
        "regfile_wr": 34868444.36,
        "rename": 0.0,
        "rob": 29550131.2,
        "tpa-dataq": 1335047.4,
        "tpa-l0": 151106062.4,
        "tpa-pvfb": 10468269.0,
        "tpa-rt": 21526053.6,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1099.2,
        "alu": 74413294.5,
        "bpred": 0.0,
        "bypass/pipereg": 199880340.0,
        "dcache_rd": 231630378.9,
        "dcache_wr": 3680373.5,
        "fetch/decode": 39980049.0,
        "fpu": 0.0,
        "icache_rd": 92660342.2,
        "iq": 0.0,
        "l2cache": 405392.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 71679571.48,
        "regfile_wr": 34868444.36,
        "rename": 0.0,
        "rob": 29549960.0,
        "tpa-dataq": 1336006.2,
        "tpa-l0": 206376698.1,
        "tpa-pvfb": 16521393.0,
        "tpa-rt": 33534957.6,
        "tpa-tmu": 216.0,
    },
  ],

]

#-------------------------------------------------------------------------
# Plot parameters
#-------------------------------------------------------------------------

# Setup x-axis

ind = np.arange( num_configs )

# Bar widths

width = 0.35

# Colors

colors = {
  'icache'  : '#f2e6ff',
  'pib'     : '#bd80ff',
  'tmu'     : '#00b359',
  'front'   : '#99ff99',
  'rf'      : '#ff3333',
  'rt/rob'  : '#cc0000',
  'slfu'    : '#ffff99',
  'llfu'    : '#ffcc66',
  'lsu'     : '#99ccff',
  'dcache'  : '#0073e6',
#  'l2cache' : '#000000',
  'pipereg' : '#7575a3',
#  'alu'        : '#80ffff',
#  'muldiv'     : '#99ccff',
#  'fpu'        : '#0073e6',
#
#  'regfile_rd' : '#4dff4d',
#  'regfile_wr' : '#99ff99',
#
#  'fetch/decode'   : '#ffddcc',
#  'rename'         : '#ffbb99',
#  'rob'            : '#ff9966',
#  'iq'             : '#ff7733',
#  'lsq'            : '#ff5500',
#  'bpred'          : '#cc4400',
#  'agen'           : '#993300',
#  'memdep'         : '#662200',
#  'bypass/pipereg' : '#999966',
#
#  'icache_rd'  : '#f2e6ff',
#  'dcache_rd'  : '#9933ff',
#  'dcache_wr'  : '#8000ff',
#  'l2cache'    : '#400080',
#
#  'tpa-dataq'  : '#cc0000',
#  'tpa-l0'     : '#ff0000',
#  'tpa-pvfb'   : '#ff3333',
#  'tpa-rt'     : '#ff6666',
#  'tpa-tmu'    : '#ff9999',
#
#  'leak'       : '#000000',
}


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

# Generate stackable bars from energy dictionary

energy_data = []
for bmark_dic in energy_dic:
  bmark_data = []
  for group in group_names:
    group_data = []
    for config in bmark_dic:
      value = 0.0
      for comp in groups[group]:
        if comp in config:
          value += config[comp]
      group_data.append( value / 1e9 )
    bmark_data.append( group_data )
  energy_data.append( bmark_data )

# Create stacked bar plots

rects = []
for i, ( ax, energy ) in enumerate( zip( axes, energy_data ) ):
  y_offset = np.array( [ 0.0 ] * num_configs )
  for name, group in zip( group_names, energy ):
    bar = ax.bar(
      ind+width/2.0, group, width, color=colors[name], bottom=y_offset )
    y_offset += group
    if i == 0:
      rects.append( bar[0] )

# Legend

legend = full_ax.legend(
  rects[::-1], group_names[::-1], loc='center left', bbox_to_anchor=(1.02, 0.5),
  ncol=1, borderaxespad=0, prop={'size':12}, frameon=True
)

# Plot labels

for i, ( ax, bmark ) in enumerate( zip( axes, bmarks ) ):
  ax.set_title( bmark, fontsize=16 )
  xmin = 0.0
  xmax = num_configs
  ymin = 0.0
  ymax = ( sum( energy_dic[i][1].values() ) - energy_dic[i][1]['bypass/pipereg'] ) / 1e9 + 0.01
  ax.set_xticks( ind+width )
  ax.set_xticklabels( configs, rotation=90, fontsize=14 )
  ax.set_yticks( np.arange( 0.0, ymax + 0.4, 0.4 ) )
  ax.set_xlim( xmin, xmax )
  ax.set_ylim( ymin, ymax )

# Plot formatting

full_ax.set_ylabel( 'Energy (mJ)', fontsize=16 )

# Pretty layout

plt.tight_layout()

# Axes formatting

for ax in axes:
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
