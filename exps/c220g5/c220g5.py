
# Copyright (c) Meta Platforms, Inc. and affiliates.

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import sys

from dram_model import Fab_DRAM
from hdd_model  import Fab_HDD
from ssd_model  import Fab_SSD
from logic_model  import Fab_Logic

debug = False

##############################
# Cisco UCS C220 M4
##############################

##############################
# Main Dell R740 integrated circuits
##############################
c220_ssd       = 480 # GB (1x 480 GB 6G SAS SSD)
c220_dram      = 192 # GB (8x 32 GB DDR4 2133 MHz PC4-17000 dual rank RDIMMs) 
ic_yield           = 0.875

# https://www.x86-guide.net/en/cpu/Intel-Xeon-Silver-4114-cpu-no6241.html
cpu_area = 3.25 #cm^2

##############################
# Estimated process technology node to mimic fairphone LCA process node
##############################
CPU_Logic = Fab_Logic(gpa  = "95",
                      carbon_intensity = "src_coal",
                      process_node = 14,
                      fab_yield=ic_yield)

SSD_main           = Fab_SSD(config  = "nand_30nm", fab_yield = ic_yield)
DRAM               = Fab_DRAM(config = "ddr4_10nm", fab_yield = ic_yield)

##############################
# Computing carbon footprint of IC's
##############################
CPU_Logic.set_area(cpu_area)
DRAM.set_capacity(c220_dram)
SSD_main.set_capacity(c220_ssd)


'''
Memory
Storage
Processor
Platform
4 Years
EU & USA
x12 32GB DIMM’s
x1 400GB SSD
x8 3.4TB SSD’s
x2 Intel Xeon 140W CPU’s
2U, 2-socket platform
'''

##################################
# Computing the packaging footprint
##################################
# number of packages
ssd_main_nr         = 1 + 1
dram_nr             = 6 + 1
cpu_nr              = 2
packaging_intensity = 150 # gram CO2

SSD_main_packaging      = packaging_intensity * ssd_main_nr
DRAM_packging           = packaging_intensity * dram_nr
CPU_packaging           = packaging_intensity * cpu_nr

total_packaging = SSD_main_packaging +  \
                  DRAM_packging + \
                  CPU_packaging
total_packaging = total_packaging / 1000.

##################################
# Compute end-to-end carbon footprints
##################################
SSD_main_count = 1
SSD_main_co2 = (SSD_main.get_carbon() + SSD_main_packaging) / 1000.
SSD_main_co2 = round(SSD_main_co2 * SSD_main_count, 2)


DRAM_count = 8
DRAM_co2 = round((DRAM.get_carbon() + DRAM_packging) / 1000. * DRAM_count, 2)

CPU_count = 2
CPU_co2   = round((CPU_Logic.get_carbon() + CPU_packaging) * CPU_count / 1000., 2)

print("--------------------------------")
print("ACT SSD main", SSD_main_co2, "kg CO2")
print("ACT DRAM", DRAM_co2, "kg CO2")
print("ACT CPU", CPU_co2, "kg CO2")
print(f"Embodied {round(SSD_main_co2 + DRAM_co2 + CPU_co2, 2)} kg CO2") 
