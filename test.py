import psutil
import cpuinfo
import platform

architecture = platform.architecture()
device_name = platform.node()
operating_system = platform.platform()

cpu_model = cpuinfo.get_cpu_info()['brand_raw']

