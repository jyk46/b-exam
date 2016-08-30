#=========================================================================
# fig-evaluation-ebreak-space
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

fig_width_pt  = 768.0
inches_per_pt = 1.0/72.27                     # convert pt to inch

aspect_ratio  = 0.35

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
  '4/1x8/1',
  '4/2x8/1',
  '4/4x8/1',
  '8/1x4/1',
  '8/2x4/1',
  '8/4x4/1',
  '8/8x4/1',
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
        "alu": 40448243.0,
        "bpred": 0.0,
        "bypass/pipereg": 26178690.0,
        "dcache_rd": 199652377.2,
        "dcache_wr": 27182628.1,
        "fetch/decode": 2620353.0,
        "fpu": 182710752.0,
        "icache_rd": 27551927.6,
        "iq": 0.0,
        "l2cache": 998137.6,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 79585656.68,
        "regfile_wr": 54741158.84,
        "rename": 0.0,
        "rob": 39068472.0,
        "tpa-dataq": 3574677.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 179256.0,
        "tpa-rt": 2163878.4,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 260.0,
        "alu": 41917043.0,
        "bpred": 0.0,
        "bypass/pipereg": 28295430.0,
        "dcache_rd": 284123637.4,
        "dcache_wr": 69295453.99999999,
        "fetch/decode": 5660742.0,
        "fpu": 182710752.0,
        "icache_rd": 8863655.7,
        "iq": 0.0,
        "l2cache": 1125873.6,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 103277082.99999999,
        "regfile_wr": 57175450.03999999,
        "rename": 0.0,
        "rob": 40818001.6,
        "tpa-dataq": 6737193.9,
        "tpa-l0": 29359956.8,
        "tpa-pvfb": 564452.0,
        "tpa-rt": 4690200.0,
        "tpa-tmu": 72.0
    },
    {
        "agen": 260.0,
        "alu": 41917043.0,
        "bpred": 0.0,
        "bypass/pipereg": 28532197.5,
        "dcache_rd": 269179724.28,
        "dcache_wr": 68232293.2,
        "fetch/decode": 11412879.0,
        "fpu": 182710752.0,
        "icache_rd": 17655358.6,
        "iq": 0.0,
        "l2cache": 1180491.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 103407848.86,
        "regfile_wr": 57175450.04,
        "rename": 0.0,
        "rob": 40818001.6,
        "tpa-dataq": 1723837.8,
        "tpa-l0": 58635534.8,
        "tpa-pvfb": 892164.0,
        "tpa-rt": 9511528.0,
        "tpa-tmu": 144.0,
    },
    {
        "agen": 260.0,
        "alu": 40448243.0,
        "bpred": 0.0,
        "bypass/pipereg": 50528100.0,
        "dcache_rd": 210458984.72,
        "dcache_wr": 27183305.1,
        "fetch/decode": 2529303.0,
        "fpu": 182710752.0,
        "icache_rd": 27735633.7,
        "iq": 0.0,
        "l2cache": 998251.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 65736110.0,
        "regfile_wr": 54741158.84,
        "rename": 0.0,
        "rob": 39068472.0,
        "tpa-dataq": 2574715.5,
        "tpa-l0": 0.0,
        "tpa-pvfb": 179256.0,
        "tpa-rt": 2150874.4,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 260.0,
        "alu": 43391603.0,
        "bpred": 0.0,
        "bypass/pipereg": 57325710.0,
        "dcache_rd": 295606155.02,
        "dcache_wr": 112303189.9,
        "fetch/decode": 5735055.0,
        "fpu": 182710752.0,
        "icache_rd": 9296512.8,
        "iq": 0.0,
        "l2cache": 1084638.4,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 107218574.98,
        "regfile_wr": 59619287.48,
        "rename": 0.0,
        "rob": 42574366.4,
        "tpa-dataq": 5600689.8,
        "tpa-l0": 31122670.4,
        "tpa-pvfb": 779492.0,
        "tpa-rt": 4904371.2,
        "tpa-tmu": 36.0,
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
        "alu": 41179763.0,
        "bpred": 0.0,
        "bypass/pipereg": 55321725.0,
        "dcache_rd": 243872722.84,
        "dcache_wr": 46821817.4,
        "fetch/decode": 22128690.0,
        "fpu": 182710752.0,
        "icache_rd": 34371969.0,
        "iq": 0.0,
        "l2cache": 1197137.6,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 2529828.2,
        "regfile_rd": 98662807.1,
        "regfile_wr": 55953531.32,
        "rename": 0.0,
        "rob": 39939819.2,
        "tpa-dataq": 1492823.4,
        "tpa-l0": 113661263.6,
        "tpa-pvfb": 1461572.0,
        "tpa-rt": 18502047.2,
        "tpa-tmu": 144.0,
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
        "alu": 204287222.5,
        "bpred": 0.0,
        "bypass/pipereg": 70753485.0,
        "dcache_rd": 813575993.56,
        "dcache_wr": 72808889.4,
        "fetch/decode": 7076937.0,
        "fpu": 185440665.6,
        "icache_rd": 76414698.0,
        "iq": 0.0,
        "l2cache": 68026537.6,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 84387.3,
        "regfile_rd": 235666619.04,
        "regfile_wr": 146230491.36,
        "rename": 0.0,
        "rob": 108161868.8,
        "tpa-dataq": 12790752.0,
        "tpa-l0": 0.0,
        "tpa-pvfb": 388724.0,
        "tpa-rt": 5819108.0,
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
        "alu": 204292262.5,
        "bpred": 0.0,
        "bypass/pipereg": 69042315.0,
        "dcache_rd": 899766448.1,
        "dcache_wr": 61863730.8,
        "fetch/decode": 27616926.0,
        "fpu": 185440665.6,
        "icache_rd": 44049757.8,
        "iq": 0.0,
        "l2cache": 65222652.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 86467.3,
        "regfile_rd": 253999924.36,
        "regfile_wr": 146238808.16,
        "rename": 0.0,
        "rob": 108168294.4,
        "tpa-dataq": 4828896.0,
        "tpa-l0": 152779610.5,
        "tpa-pvfb": 1552796.0,
        "tpa-rt": 24232996.0,
        "tpa-tmu": 144.0,
    },
    {
        "agen": 208.0,
        "alu": 204287222.5,
        "bpred": 0.0,
        "bypass/pipereg": 145268655.0,
        "dcache_rd": 854872528.44,
        "dcache_wr": 72800900.8,
        "fetch/decode": 7265286.0,
        "fpu": 185440665.6,
        "icache_rd": 76414698.0,
        "iq": 0.0,
        "l2cache": 67745833.6,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 84387.3,
        "regfile_rd": 225944135.2,
        "regfile_wr": 146230491.36,
        "rename": 0.0,
        "rob": 108161894.4,
        "tpa-dataq": 7747209.6,
        "tpa-l0": 0.0,
        "tpa-pvfb": 388724.0,
        "tpa-rt": 5781604.8,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 208.0,
        "alu": 204301334.5,
        "bpred": 0.0,
        "bypass/pipereg": 143569335.0,
        "dcache_rd": 817911085.48,
        "dcache_wr": 69077216.7,
        "fetch/decode": 14358522.0,
        "fpu": 185440665.6,
        "icache_rd": 22042318.0,
        "iq": 0.0,
        "l2cache": 82379107.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 90211.3,
        "regfile_rd": 245266285.44,
        "regfile_wr": 146253778.4,
        "rename": 0.0,
        "rob": 108179814.4,
        "tpa-dataq": 12798345.6,
        "tpa-l0": 76402844.1,
        "tpa-pvfb": 779660.0,
        "tpa-rt": 11880388.8,
        "tpa-tmu": 36.0,
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
        "alu": 204287726.5,
        "bpred": 0.0,
        "bypass/pipereg": 144649837.5,
        "dcache_rd": 878219447.22,
        "dcache_wr": 55529862.6,
        "fetch/decode": 57859935.0,
        "fpu": 185440665.6,
        "icache_rd": 88063376.0,
        "iq": 0.0,
        "l2cache": 21147772.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 84595.3,
        "regfile_rd": 253859266.48,
        "regfile_wr": 146231323.04,
        "rename": 0.0,
        "rob": 108162534.4,
        "tpa-dataq": 4827427.2,
        "tpa-l0": 305533113.1,
        "tpa-pvfb": 3102092.0,
        "tpa-rt": 47544466.4,
        "tpa-tmu": 144.0,
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
        "alu": 74414320.5,
        "bpred": 0.0,
        "bypass/pipereg": 90238095.0,
        "dcache_rd": 259666557.82,
        "dcache_wr": 3589994.0,
        "fetch/decode": 9029781.0,
        "fpu": 0.0,
        "icache_rd": 122113603.8,
        "iq": 0.0,
        "l2cache": 379388.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 68539938.8,
        "regfile_wr": 34868444.36,
        "rename": 0.0,
        "rob": 29550299.2,
        "tpa-dataq": 1438207.2,
        "tpa-l0": 0.0,
        "tpa-pvfb": 3417638.0,
        "tpa-rt": 7440909.6,
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
        "alu": 74414046.0,
        "bpred": 0.0,
        "bypass/pipereg": 58346670.0,
        "dcache_rd": 217280360.64,
        "dcache_wr": 3659318.8,
        "fetch/decode": 23338668.0,
        "fpu": 0.0,
        "icache_rd": 57902554.7,
        "iq": 0.0,
        "l2cache": 396252.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 66325550.12,
        "regfile_wr": 34868444.36,
        "rename": 0.0,
        "rob": 29550227.2,
        "tpa-dataq": 1159811.4,
        "tpa-l0": 158523408.9,
        "tpa-pvfb": 9487471.0,
        "tpa-rt": 19149216.0,
        "tpa-tmu": 432.0,
    },
    {
        "agen": 1099.2,
        "alu": 74414320.5,
        "bpred": 0.0,
        "bypass/pipereg": 176916165.0,
        "dcache_rd": 313672547.78,
        "dcache_wr": 3590603.3,
        "fetch/decode": 8852775.0,
        "fpu": 0.0,
        "icache_rd": 121873604.4,
        "iq": 0.0,
        "l2cache": 379280.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 66794692.22,
        "regfile_wr": 34868444.36,
        "rename": 0.0,
        "rob": 29550324.8,
        "tpa-dataq": 1747490.4,
        "tpa-l0": 0.0,
        "tpa-pvfb": 3417638.0,
        "tpa-rt": 7469027.2,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 1099.2,
        "alu": 74416030.5,
        "bpred": 0.0,
        "bypass/pipereg": 142594995.0,
        "dcache_rd": 259690811.12,
        "dcache_wr": 3613264.2,
        "fetch/decode": 14265471.0,
        "fpu": 0.0,
        "icache_rd": 34306077.0,
        "iq": 0.0,
        "l2cache": 382652.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 66472712.28,
        "regfile_wr": 34869990.2,
        "rename": 0.0,
        "rob": 29551379.2,
        "tpa-dataq": 1438628.7,
        "tpa-l0": 95751032.8,
        "tpa-pvfb": 5631325.0,
        "tpa-rt": 11781221.6,
        "tpa-tmu": 108.0,
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
        "alu": 74413470.0,
        "bpred": 0.0,
        "bypass/pipereg": 89458882.5,
        "dcache_rd": 217278491.6,
        "dcache_wr": 3709690.7,
        "fetch/decode": 35783553.0,
        "fpu": 0.0,
        "icache_rd": 92499578.3,
        "iq": 0.0,
        "l2cache": 421820.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 979.2,
        "regfile_rd": 63691092.98,
        "regfile_wr": 34868186.72,
        "rename": 0.0,
        "rob": 29549948.0,
        "tpa-dataq": 1159783.5,
        "tpa-l0": 238913861.0,
        "tpa-pvfb": 14799778.0,
        "tpa-rt": 29365656.8,
        "tpa-tmu": 432.0,
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
        "alu": 109967511.0,
        "bpred": 0.0,
        "bypass/pipereg": 181908495.0,
        "dcache_rd": 489359157.58,
        "dcache_wr": 166205198.5,
        "fetch/decode": 18198360.0,
        "fpu": 0.0,
        "icache_rd": 244691435.7,
        "iq": 0.0,
        "l2cache": 112604148.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 82084597.4,
        "regfile_wr": 53014067.7,
        "rename": 0.0,
        "rob": 45427924.8,
        "tpa-dataq": 3554696.1,
        "tpa-l0": 0.0,
        "tpa-pvfb": 7386540.0,
        "tpa-rt": 13486764.8,
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
        "alu": 139948302.0,
        "bpred": 0.0,
        "bypass/pipereg": 117738082.5,
        "dcache_rd": 523554544.86,
        "dcache_wr": 200234794.3,
        "fetch/decode": 47095233.0,
        "fpu": 0.0,
        "icache_rd": 128709818.0,
        "iq": 0.0,
        "l2cache": 114361584.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 107439808.6,
        "regfile_wr": 69331407.82,
        "rename": 0.0,
        "rob": 58053079.2,
        "tpa-dataq": 3110606.1,
        "tpa-l0": 306327056.0,
        "tpa-pvfb": 19809818.0,
        "tpa-rt": 37839331.2,
        "tpa-tmu": 432.0,
    },
    {
        "agen": 1241.6,
        "alu": 109967511.0,
        "bpred": 0.0,
        "bypass/pipereg": 346320435.0,
        "dcache_rd": 575837449.36,
        "dcache_wr": 166205266.2,
        "fetch/decode": 17324784.0,
        "fpu": 0.0,
        "icache_rd": 244691435.7,
        "iq": 0.0,
        "l2cache": 112604148.8,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 79802666.36,
        "regfile_wr": 53014067.7,
        "rename": 0.0,
        "rob": 45427924.8,
        "tpa-dataq": 4664977.5,
        "tpa-l0": 0.0,
        "tpa-pvfb": 7386540.0,
        "tpa-rt": 13488910.4,
        "tpa-tmu": 0.0,
    },
    {
        "agen": 1241.6,
        "alu": 165541989.0,
        "bpred": 0.0,
        "bypass/pipereg": 311421465.0,
        "dcache_rd": 648554918.68,
        "dcache_wr": 237438241.9,
        "fetch/decode": 31149657.0,
        "fpu": 0.0,
        "icache_rd": 84171917.0,
        "iq": 0.0,
        "l2cache": 113670819.2,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 130408050.74,
        "regfile_wr": 82827650.96,
        "rename": 0.0,
        "rob": 68705388.8,
        "tpa-dataq": 7122983.1,
        "tpa-l0": 202710267.1,
        "tpa-pvfb": 18935035.0,
        "tpa-rt": 25439366.4,
        "tpa-tmu": 108.0,
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
        "alu": 122928478.5,
        "bpred": 0.0,
        "bypass/pipereg": 150273427.5,
        "dcache_rd": 463276603.02,
        "dcache_wr": 158787656.3,
        "fetch/decode": 60109371.0,
        "fpu": 0.0,
        "icache_rd": 170900965.6,
        "iq": 0.0,
        "l2cache": 115745152.0,
        "leak": 0.0,
        "lsq": 0.0,
        "memdep": 0.0,
        "muldiv": 942.0,
        "regfile_rd": 86973013.56,
        "regfile_wr": 60465606.36,
        "rename": 0.0,
        "rob": 50915884.0,
        "tpa-dataq": 2703467.7,
        "tpa-l0": 398412231.6,
        "tpa-pvfb": 21906745.0,
        "tpa-rt": 48241381.6,
        "tpa-tmu": 432.0,
    },
  ],

]

# NOTE: The single lane group configurations (TC in space)
# were not simulated with a PIB, so the corresponding I$ energy numbers
# are a slightly inflated. One way to adjust this is to scale the total
# I$ energy by 1/8 (8 words per cache line), and assume the remaining 7/8
# of the energy would be spent on the PIB. Since the PIB is modeled to
# take half as much energy per hit as the I$, we need to further scale
# the 7/8 by 1/2.

for bmark_dic in energy_dic:
  for dic in [ bmark_dic[2], bmark_dic[5] ]: # 4/1 x 8/1, 8/1 x 4/1
    dic['tpa-l0']     = dic['icache_rd']
    dic['icache_rd'] *= 0.125       # scale I$ energy by 1/8
    dic['tpa-l0']    *= 0.5 * 0.875 # remaining I$ energy is PIB

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
  rects[::-1], group_names[::-1], loc='center left', bbox_to_anchor=(1.02, 0.5),
  ncol=1, borderaxespad=0, prop={'size':10}, frameon=True,
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
  ax.set_xticklabels( configs, rotation=90, fontsize=12 )
  ax.set_yticks( np.arange( 0.0, ymax + 0.5, 0.5 if i != 1 else 1.0 ) )
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
