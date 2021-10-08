from cpuinfo import get_cpu_info
from os import cpu_count

cpuCount = 0
cpuInfo = None

#--------------------------------------------------
# Get number of available threads
#--------------------------------------------------



def CPUcount():
    global cpuCount
    if cpuCount: return cpuCount
    else: return cpu_count()



#--------------------------------------------------
# End program messages
#--------------------------------------------------



def endProgram(reason="interrupted"):
    if reason == "noGrain": print("\n[Error] No grain found. You can generate a grain by running the following command: python grain.py")
    else:print("\nProgram interrupted.")
    exit()


#--------------------------------------------------
# Get CPU infos
#--------------------------------------------------



def CPUinfo():
    global cpuInfo
    if cpuInfo is not None: return cpuInfo
    else:
        print("\nGetting CPU info...")
        cpuInfo = get_cpu_info()["brand_raw"]
        print("-> ",cpuInfo)
        return cpuInfo.replace(" ","_")



