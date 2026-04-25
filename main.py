import sys
from mmu import MMU
from file import File
from constants import NUM_FRAMES

class Tee:
    def __init__(self,file, stdout):
        self.file=file
        self.stdout=stdout
    def write(self,data):
        if not self.file.closed:
            self.file.write(data)
        self.stdout.write(data)
    def flush(self):
        if not self.file.closed:
            self.file.flush()
        self.stdout.flush()

def run():
    with open("output.log", "w",encoding="utf-8") as f:
        sys.stdout =Tee(f,sys.__stdout__)
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
                    print("*** REMOVED ***")
                    for r in removed:
                        print(r)

                print("Page Table:")
                for k, e in mmu.table.entries.items():
                    print(f"{k} | V={e.valid} | Ref={e.reference}")

                print("Frames:")
                for fr in mmu.frames:
                    print(fr)

        print("\nDONE")


if __name__ == "__main__":
    run()