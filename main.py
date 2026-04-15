import random
from page_table import PageTable
from constants import TOTAL_REQUESTS,PAGE_RANGE,OUTPUT_FILE

def generate_sequence():
    return [random.randint(1,PAGE_RANGE) for _ in range(TOTAL_REQUESTS)]

def run():
    pt=PageTable()
    sequence=generate_sequence()
    hits=0
    faults = 0

    with open(OUTPUT_FILE, "w") as f:
        f.write(" Page Table\n")
        f.write(f"Sequence:{sequence}\n\n")
        for page in sequence:
            file,status=pt.access_page(page)
            if status == "HIT":
                hits+= 1
            else:
                faults+= 1
            # displat pages in memeory
            frame_view=[entry[0] for entry in pt.frames]
            f.write(f"Page {page} | {status} | File {file} | Frames {frame_view}\n")
        f.write("\n")
        f.write(f"Total Hits: {hits}\n")
        f.write(f"Total Faults: {faults}\n")
if __name__ == "__main__":
    run()