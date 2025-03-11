import os

pkg_dirs = []

dir_entries = os.scandir(".")

for entry in dir_entries:
    if entry.is_file(): continue
    if entry.name.startswith("."): continue

    print("FOUND pkg " + entry.name)
    pkg_dirs.append(entry.name)

print(f"END total of {len(pkg_dirs)} pkgs found")