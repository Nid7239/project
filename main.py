import random
import time
from mmu import MMU
from constants import TOTAL_REQUESTS, PAGE_RANGE, NUM_FRAMES, OUTPUT_FILE


def generate_sequence():
    return [random.randint(1, PAGE_RANGE) for _ in range(TOTAL_REQUESTS)]


def run():
    mmu =MMU(NUM_FRAMES)
    sequence=generate_sequence()
    hits=0
    faults=0
    header= "LRU PAGE TABLE SIMULATION"
    separator= "=" * 70
    print("\n" + header)
    print(separator)
    print(f"Sequence | {sequence}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        f.write(f"Sequence | {sequence}\n")

        for page in sequence:
            frame, status=mmu.access_page(page)
            if status == "HIT":
                hits +=1
            else:
                faults +=1

            frame_view=[fr.page if fr.page is not None else "-" for fr in mmu.frames]
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            line = f"Time | {timestamp} | Page | {page} | Status | {status} | Frames | {frame_view}"
            print(line)
            f.write(line + "\n")
        print(separator)
        print(f"Total hits | {hits}")
        print(f"Total faults | {faults}")

        f.write(separator + "\n")
        f.write(f"Total hits | {hits}\n")
        f.write(f"Total faults | {faults}\n")
if __name__=="__main__":
    run()