import os
import json

pkg_dirs = []

print("scanning for directories")
dir_entries = os.scandir(".")

readme_addition = ""

# pkg manifests

for entry in dir_entries:
    if entry.is_file(): continue
    if entry.name.startswith("."): continue

    with open(entry.name+"/manifest.json", "r") as pkg_m:
        pkg_m_j = json.load(pkg_m)
        if pkg_m_j['type'] != "pkg": continue
        print(f"package {pkg_m_j['name']} found")
        
        readme_addition += f"### {pkg_m_j['name']}\n{pkg_m_j['desc']}\n\n"

    pkg_dirs.append(entry.name)

print(f"total of {len(pkg_dirs)} pkgs found")

# repo manifest

with open("manifest.json", "r+") as repo_m:
    repo_m_j = json.load(repo_m)
    
    print(f"updating {repo_m_j['name']} manifest")
    repo_m_j['pkgs'] = pkg_dirs

    repo_m.seek(0)
    json.dump(repo_m_j, repo_m, indent=4)
    repo_m.truncate()

# readme

print("updating readme")

with open("README.base.md", "r") as readme_b:
  readme_d = readme_b.read()

readme_d = readme_d.replace("[replace]", readme_addition)

with open("README.md", "w") as readme:
    readme.write(readme_d)