import time
import sys
from mmu import MMU
from file import File
from constants import NUM_FRAMES

def format_time(dt):
    return dt.strftime("%H:%M:%S.%f")
def run():
    with open("output.log", "w") as log_file:
        sys.stdout = log_file
        mmu = MMU(NUM_FRAMES)
        files = [File("f1", 8), File("f2", 8), File("f3", 16)]
        print(f"{'TIMESTAMP':<18} | {'PAGE':<8} | {'STATUS':<6} | {'PHYSICAL RAM SLOTS (0-3)'}")
        print("-" * 85)

        for fobj in files:
            print(f"--- Accessing File: {fobj.file_id} ---")
            for p in fobj.pages:
                time.sleep(0.001) 
                status, removed = mmu.access(p)
                entry = mmu.table.get(p)
                ts = format_time(entry.last_access)          
                frame_view = " ".join([f"[{f.page if f.page else '   -   ':^9}]" for f in mmu.frames])
                print(f"{ts:<18} | {p:<8} | {status:<6} | {frame_view}")
                
                if removed:
                    print(f"{' ':>18} | [CLEANUP] Table Purged: {removed}")
            print()

    sys.stdout = sys.__stdout__
    print("'output.log'.")

if __name__ == "__main__":
    run()