import random
import time
from mmu import MMU
from file import File
from constants import NUM_FRAMES, TOTAL_REQUESTS, OUTPUT_FILE

def generate_files():
    return [
        File("file1",12),  # 3 pages
        File("file2", 8),   # 2 pages
        File("file3", 4),   # 1 page
    ]
def generate_sequence(files):
    file_ids = [f.file_id for f in files]
    weights = [0.5, 0.3, 0.2]  # file1 more frequent
    sequence = []

    for _ in range(TOTAL_REQUESTS):
        chosen_file_id = random.choices(file_ids, weights=weights, k=1)[0]
        chosen_file = next(f for f in files if f.file_id == chosen_file_id)
        page = random.choice(chosen_file.pages)
        sequence.append((chosen_file_id, page))

    return sequence
def run():
    mmu=MMU(NUM_FRAMES)
    files=generate_files()
    sequence=generate_sequence(files)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        def write(line):
            print(line)
            f.write(line + "\n")
        write("   PAGE TABLE SIMULATION         ")
        write("Sequence:")
        write(str([file_id for file_id, _ in sequence]))

        for file_id,page in sequence:
            status =mmu.access_page(page)
            write(f"\nAccess: {file_id} ({page}) ---- {status}")
            write("Page Table:")
            for p, entry in mmu.page_table.entries.items():
                frame_id = entry.frame.frame_id if entry.frame else "-"
                if entry.last_access:
                    time_str = time.strftime("%H:%M:%S", time.localtime(entry.last_access))
                else:
                    time_str = "-"
                write(f"{p} -> Frame {frame_id} | Valid: {entry.valid} | Time: {time_str}")
            write("Frames:")
            for fr in mmu.frames:
                write(str(fr))
if __name__ == "__main__":
    run()