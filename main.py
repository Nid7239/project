import sys
import time
from mmu import MMU
from file import File
from constants import NUM_FRAMES


def fmt(t):
    us = int((t % 1) * 1000000)
    return time.strftime("%H:%M:%S", time.localtime(t)) + f".{us:06d}"


def run():
    with open("output.log", "w") as f:
        sys.stdout = f

        mmu = MMU(NUM_FRAMES)

        files = [
            File("file1", 8),
            File("file2", 8),
            File("file3", 16),
            File("file4", 8),
        ]

        print("===== PAGE TABLE SIMULATION =====")

        for fobj in files:
            print(f"\n=== Accessing {fobj.file_id} ===")

            for p in fobj.pages:
                status, removed = mmu.access(p)

                print(f"{p} -> {status}")

                if removed:
                    print("*** CLEANUP ***")
                    for r in removed:
                        print(r)

                print("Page Table:")
                for k, e in mmu.table.entries.items():
                    print(f"{k} | V={e.valid} | Ref={e.reference} | Time={fmt(e.last_access)}")

                print("Frames:")
                for fr in mmu.frames:
                    print(fr)

        print("\nDONE")


if __name__ == "__main__":
    run()