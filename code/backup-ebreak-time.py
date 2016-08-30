#=========================================================================
# fig-evaluation-ebreak-time
#=========================================================================

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

aspect_ratio  = 2.18

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
# Raw data
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

  # sgemm
  [
    {
        "agen": 12856147.2,
        "alu": 111301182.5,
        "bpred": 0.0,
        "bypass/pipereg": 613691790.0,
        "dcache_rd": 823961322.5,
        "dcache_wr": 55165100.6,
        "fetch/decode": 245476716.0,
        "fpu": 118908518.4,
        "icache_rd": 2471134076.4 / scale_factor,
        "iq": 0.0,
        "l2cache": 49206488.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 9.3,
        "regfile_rd": 83932208.8,
        "regfile_wr": 51753658.4,
        "rename": 0.0,
        "rob": 0.0,
        "tpa-dataq": 0.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 0.0,
        "tpa-rt": 0.0,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 12858251.2,
        "alu": 111316137.5,
        "bpred": 387206641.456,
        "bypass/pipereg": 230409513.291,
        "dcache_rd": 823289273.0,
        "dcache_wr": 55165100.6,
        "fetch/decode": 224308416.0,
        "fpu": 118908518.4,
        "icache_rd": 2258041748.5 / scale_factor,
        "iq": 793564816.32,
        "l2cache": 49207041.6,
        "leak": 0.0,
        "lsq": 374175109.92,
        "memdep": 120405236.4,
        "muldiv": 9.3,
        "regfile_rd": 390482751.36,
        "regfile_wr": 201857563.44,
        "rename": 790666550.96,
        "rob": 740889052.32,
        "tpa-dataq": 0.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 0.0,
        "tpa-rt": 0.0,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 208.0,
        "alu": 204301334.5,
        "bpred": 0.0,
        "bypass/pipereg": 68786970.0,
        "dcache_rd": 937990110.4,
        "dcache_wr": 69126028.4,
        "fetch/decode": 13758453.0,
        "fpu": 185440665.6,
        "icache_rd": 22042227.9,
        "iq": 0.0,
        "l2cache": 80105404.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 90211.3,
        "regfile_rd": 251601187.48,
        "regfile_wr": 146253778.4,
        "rename": 0.0,
        "rob": 108179814.4,
        "tpa-dataq": 22889260.8,
        "tpa-l0": 76402844.1,
        "tpa-pvfb": 779660.0,
        "tpa-rt": 12005789.6,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 208.0,
        "alu": 204301334.5,
        "bpred": 0.0,
        "bypass/pipereg": 142191915.0,
        "dcache_rd": 938366500.4,
        "dcache_wr": 68740341.5,
        "fetch/decode": 28439442.0,
        "fpu": 185440665.6,
        "icache_rd": 25750878.0,
        "iq": 0.0,
        "l2cache": 81345072.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 90211.3,
        "regfile_rd": 248856824.28,
        "regfile_wr": 146253778.4,
        "rename": 0.0,
        "rob": 108179814.4,
        "tpa-dataq": 22889260.8,
        "tpa-l0": 149453578.8,
        "tpa-pvfb": 1555064.0,
        "tpa-rt": 24272008.8,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 208.0,
        "alu": 204301334.5,
        "bpred": 0.0,
        "bypass/pipereg": 285871260.0,
        "dcache_rd": 939298687.9,
        "dcache_wr": 68677583.6,
        "fetch/decode": 57175311.0,
        "fpu": 185440665.6,
        "icache_rd": 29057084.4,
        "iq": 0.0,
        "l2cache": 84611030.4,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 90211.3,
        "regfile_rd": 248389745.56,
        "regfile_wr": 146253778.4,
        "rename": 0.0,
        "rob": 108179808.0,
        "tpa-dataq": 22889260.8,
        "tpa-l0": 285904608.0,
        "tpa-pvfb": 3105872.0,
        "tpa-rt": 48462771.2,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 208.0,
        "alu": 204301334.5,
        "bpred": 0.0,
        "bypass/pipereg": 568823460.0,
        "dcache_rd": 938090097.9,
        "dcache_wr": 68030439.3,
        "fetch/decode": 113765751.0,
        "fpu": 185440665.6,
        "icache_rd": 13769903.3,
        "iq": 0.0,
        "l2cache": 81623708.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 90211.3,
        "regfile_rd": 246519943.6,
        "regfile_wr": 146253760.32,
        "rename": 0.0,
        "rob": 108179795.2,
        "tpa-dataq": 22889260.8,
        "tpa-l0": 571274072.0,
        "tpa-pvfb": 6207488.0,
        "tpa-rt": 96564560.8,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 208.0,
        "alu": 204292262.5,
        "bpred": 0.0,
        "bypass/pipereg": 141841815.0,
        "dcache_rd": 930660914.22,
        "dcache_wr": 60046053.5,
        "fetch/decode": 28369422.0,
        "fpu": 185440665.6,
        "icache_rd": 44049757.8,
        "iq": 0.0,
        "l2cache": 66170083.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 86467.3,
        "regfile_rd": 248749347.72,
        "regfile_wr": 146238808.16,
        "rename": 0.0,
        "rob": 108168294.4,
        "tpa-dataq": 22881916.8,
        "tpa-l0": 152779610.5,
        "tpa-pvfb": 1552796.0,
        "tpa-rt": 23770378.4,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 208.0,
        "alu": 204292262.5,
        "bpred": 0.0,
        "bypass/pipereg": 283661610.0,
        "dcache_rd": 931196286.72,
        "dcache_wr": 59601129.1,
        "fetch/decode": 56733381.0,
        "fpu": 185440665.6,
        "icache_rd": 50031714.4,
        "iq": 0.0,
        "l2cache": 67360681.6,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 86467.3,
        "regfile_rd": 240911505.0,
        "regfile_wr": 146238808.16,
        "rename": 0.0,
        "rob": 108168294.4,
        "tpa-dataq": 22881916.8,
        "tpa-l0": 294928896.5,
        "tpa-pvfb": 3103352.0,
        "tpa-rt": 47796508.8,
        "tpa-tmu": 72.0,
    },
    {
        "agen": 208.0,
        "alu": 204292262.5,
        "bpred": 0.0,
        "bypass/pipereg": 567250215.0,
        "dcache_rd": 930316159.22,
        "dcache_wr": 60843085.6,
        "fetch/decode": 113451102.0,
        "fpu": 185440665.6,
        "icache_rd": 44047009.6,
        "iq": 0.0,
        "l2cache": 66116771.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 86467.3,
        "regfile_rd": 251376909.6,
        "regfile_wr": 146238808.16,
        "rename": 0.0,
        "rob": 108168289.6,
        "tpa-dataq": 22881916.8,
        "tpa-l0": 571185087.7,
        "tpa-pvfb": 6204464.0,
        "tpa-rt": 97757761.6,
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

  # mis
  [
    {
        "agen": 3618565.6,
        "alu": 23148782.5,
        "bpred": 0.0,
        "bypass/pipereg": 119786602.5,
        "dcache_rd": 263247394.0,
        "dcache_wr": 82820889.8,
        "fetch/decode": 47914641.0,
        "fpu": 0.0,
        "icache_rd": 482341079.8 / scale_factor,
        "iq": 0.0,
        "l2cache": 191176630.4,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 0.0,
        "regfile_rd": 11884707.2,
        "regfile_wr": 7196878.4,
        "rename": 0.0,
        "rob": 0.0,
        "tpa-dataq": 0.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 0.0,
        "tpa-rt": 0.0,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 6094308.0,
        "alu": 38789730.0,
        "bpred": 224761177.008,
        "bypass/pipereg": 246709080.636,
        "dcache_rd": 473174114.5,
        "dcache_wr": 80877967.5,
        "fetch/decode": 81235344.0,
        "fpu": 0.0,
        "icache_rd": 817771922.7 / scale_factor,
        "iq": 344775104.8,
        "l2cache": 246931756.8,
        "leak": 0.0,
        "lsq": 177344362.8,
        "memdep": 63904926.24,
        "muldiv": 0.0,
        "regfile_rd": 103336147.2,
        "regfile_wr": 45944205.84,
        "rename": 237257602.32,
        "rob": 322907912.64,
        "tpa-dataq": 0.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 0.0,
        "tpa-rt": 0.0,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 1241.6,
        "alu": 165539937.0,
        "bpred": 0.0,
        "bypass/pipereg": 157806615.0,
        "dcache_rd": 641090336.92,
        "dcache_wr": 237430639.5,
        "fetch/decode": 31566330.0,
        "fpu": 0.0,
        "icache_rd": 84171554.6,
        "iq": 0.0,
        "l2cache": 113634492.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 133982643.02,
        "regfile_wr": 82826432.82,
        "rename": 0.0,
        "rob": 68704464.8,
        "tpa-dataq": 9819042.9,
        "tpa-l0": 202955823.3,
        "tpa-pvfb": 18935224.0,
        "tpa-rt": 25407616.0,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1241.6,
        "alu": 165180625.5,
        "bpred": 0.0,
        "bypass/pipereg": 242162250.0,
        "dcache_rd": 641254034.0,
        "dcache_wr": 237449662.0,
        "fetch/decode": 48437457.0,
        "fpu": 0.0,
        "icache_rd": 141867718.4,
        "iq": 0.0,
        "l2cache": 113519048.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 137090667.34,
        "regfile_wr": 82825513.0,
        "rename": 0.0,
        "rob": 68576860.0,
        "tpa-dataq": 9819456.3,
        "tpa-l0": 286834269.7,
        "tpa-pvfb": 22855413.0,
        "tpa-rt": 40243096.0,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1241.6,
        "alu": 164758750.5,
        "bpred": 0.0,
        "bypass/pipereg": 349779195.0,
        "dcache_rd": 641340404.04,
        "dcache_wr": 237470090.3,
        "fetch/decode": 69960846.0,
        "fpu": 0.0,
        "icache_rd": 80667750.6,
        "iq": 0.0,
        "l2cache": 113614347.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 122001885.82,
        "regfile_wr": 82830634.16,
        "rename": 0.0,
        "rob": 68427456.8,
        "tpa-dataq": 9819868.8,
        "tpa-l0": 383905993.8,
        "tpa-pvfb": 26592027.0,
        "tpa-rt": 58546048.8,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1241.6,
        "alu": 164346172.5,
        "bpred": 0.0,
        "bypass/pipereg": 495836535.0,
        "dcache_rd": 641205032.46,
        "dcache_wr": 237513882.0,
        "fetch/decode": 99172314.0,
        "fpu": 0.0,
        "icache_rd": 46200581.2,
        "iq": 0.0,
        "l2cache": 113557699.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 126256778.78,
        "regfile_wr": 82826109.64,
        "rename": 0.0,
        "rob": 68280063.2,
        "tpa-dataq": 9819958.5,
        "tpa-l0": 526036329.3,
        "tpa-pvfb": 30021054.0,
        "tpa-rt": 85879591.2,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1241.6,
        "alu": 139822104.0,
        "bpred": 0.0,
        "bypass/pipereg": 234584205.0,
        "dcache_rd": 554602190.44,
        "dcache_wr": 200070669.5,
        "fetch/decode": 46921848.0,
        "fpu": 0.0,
        "icache_rd": 128429773.4,
        "iq": 0.0,
        "l2cache": 114405012.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 104874808.04,
        "regfile_wr": 69263718.56,
        "rename": 0.0,
        "rob": 57998244.0,
        "tpa-dataq": 6683280.0,
        "tpa-l0": 305291845.3,
        "tpa-pvfb": 19776029.0,
        "tpa-rt": 37757085.6,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1241.6,
        "alu": 136852743.0,
        "bpred": 0.0,
        "bypass/pipereg": 319550610.0,
        "dcache_rd": 542738666.74,
        "dcache_wr": 195767847.1,
        "fetch/decode": 63915129.0,
        "fpu": 0.0,
        "icache_rd": 200199650.6,
        "iq": 0.0,
        "l2cache": 114606592.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 103744405.76,
        "regfile_wr": 67911307.44,
        "rename": 0.0,
        "rob": 56744960.0,
        "tpa-dataq": 6610008.9,
        "tpa-l0": 373655268.2,
        "tpa-pvfb": 23365699.0,
        "tpa-rt": 51893200.8,
        "tpa-tmu": 216.0,
    },
    {
        "agen": 1241.6,
        "alu": 136436668.5,
        "bpred": 0.0,
        "bypass/pipereg": 436896390.0,
        "dcache_rd": 542926601.2,
        "dcache_wr": 195551910.4,
        "fetch/decode": 87384285.0,
        "fpu": 0.0,
        "icache_rd": 112266884.4,
        "iq": 0.0,
        "l2cache": 114701176.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 99435878.48,
        "regfile_wr": 67905483.42,
        "rename": 0.0,
        "rob": 56596000.8,
        "tpa-dataq": 6610554.0,
        "tpa-l0": 474116066.5,
        "tpa-pvfb": 27905731.0,
        "tpa-rt": 71858924.0,
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

flat_axes = axes #[ ax for dim in axes for ax in dim ]

rects = []
for i, ( ax, energy ) in enumerate( zip( flat_axes, energy_data ) ):
  y_offset = np.array( [ 0.0 ] * num_configs )
  for name, group in zip( group_names, energy ):
    bar = ax.bar(
      ind+width/2.0, group, width, color=colors[name], bottom=y_offset )
    y_offset += group
    if i == 0:
      rects.append( bar[0] )

# Legend

legend = full_ax.legend(
  rects[::-1], group_names[::-1], loc='lower center', bbox_to_anchor=(0.42, 1.04),
  ncol=4, borderaxespad=0, prop={'size':10}, frameon=True,
  scatterpoints=1,
  labelspacing=0.5,
  columnspacing=0.5,
#  handletextpad=0,
  borderpad=0.5
)

# Plot labels

for i, ( ax, bmark ) in enumerate( zip( flat_axes, bmarks ) ):
  ax.set_title( bmark, fontsize=16 )
  xmin = 0.0
  xmax = num_configs
  ymin = 0.0
  ymax = ( sum( energy_dic[i][1].values() ) - energy_dic[i][1]['bypass/pipereg'] ) / 1e9 + 0.01
  ax.set_xticks( ind+width )
  ax.set_xticklabels( configs, rotation=25, fontsize=12 )
  ax.set_yticks( np.arange( 0.0, ymax + 0.5, 0.5 if i != i else 1.0 ) )
  ax.set_xlim( xmin, xmax )
  ax.set_ylim( ymin, ymax )

  ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

# Plot formatting

full_ax.set_ylabel( 'Energy (mJ)', fontsize=16 )

# Pretty layout

plt.tight_layout( w_pad=0.1, h_pad=0.1 )

# Axes formatting

for ax in flat_axes:
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
