import m5
from m5.objects import *
from caches import *

import argparse

# parser.add_argument("binary", default="tests/test-progs/hello/bin/x86/linux/hello", nargs="?", type=str,
parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')
parser.add_argument("binary", default="gapbs/a.out", nargs="?", type=str,
                        help="Path to the binary to execute.")
parser.add_argument("extra_args", default="-h", nargs="?", type=str,
                        help="Extra arguments for the binary.")
parser.add_argument("--l1i_size",
                        help=f"L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size",
                        help="L1 data cache size. Default: Default: 64kB.")
parser.add_argument("--l2_size",
                        help="L2 cache size. Default: 256kB.")
parser.add_argument("--l1i_assoc",
                        help=f"L1I n-way set associative. Default: 2.")
parser.add_argument("--l1d_assoc",
                        help="L1D n-way set associative. Default: Default: 2.")
parser.add_argument("--l2_assoc",
                        help="L2 n-way set associative. Default: 8.")

options = parser.parse_args()

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = DerivO3CPU()

system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

system.membus = SystemXBar()

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# binary = 'tests/test-progs/hello/bin/x86/linux/hello'
binary = options.binary
extra_args = options.extra_args
print("extra_args=", extra_args)

# for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)

process = Process()
# process.cmd = [binary]
# process.cmd += options.extra_args

process.cmd = [binary] + extra_args.split()
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
