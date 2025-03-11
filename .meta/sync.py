import os
import json

grp_dirs = []
pkg_dirs = []

print("scanning for directories")
dir_entries = os.scandir(".")

grp_readme_addition = ""
pkg_readme_addition = ""

def comma_seperated_string_from_array(json):
    strings = [str(item) for item in json]
    return ", ".join(strings)


# pkg manifests

for entry in dir_entries:
    if entry.is_file(): continue
    if entry.name.startswith("."): continue

    with open(entry.name+"/manifest.json", "r") as entry_m:
        entry_m_j = json.load(entry_m)
        if entry_m_j['type'] == "group":
            print(f"group {entry_m_j['name']} found")
            grp_readme_addition += f"### {entry_m_j['name']}\n{entry_m_j['desc']}\npackages: {comma_seperated_string_from_array(entry_m_j['pkgs'])}\n\n"
            grp_dirs.append(entry.name)
        if entry_m_j['type'] == "pkg":
            print(f"package {entry_m_j['name']} found")
            pkg_readme_addition += f"### {entry_m_j['name']}\n{entry_m_j['desc']}\n\n"
            pkg_dirs.append(entry.name)

print(f"total of {len(pkg_dirs)} pkgs found")
print(f"total of {len(grp_dirs)} groups found")

# repo manifest

with open("manifest.json", "r+") as repo_m:
    repo_m_j = json.load(repo_m)
    
    print(f"updating {repo_m_j['name']} manifest")
    repo_m_j['groups'] = grp_dirs
    repo_m_j['pkgs'] = pkg_dirs

    repo_m.seek(0)
    json.dump(repo_m_j, repo_m, indent=4)
    repo_m.truncate()

# readme

print("updating readme")

with open("README.base.md", "r") as readme_b:
  readme_d = readme_b.read()

readme_addition = "## groups\n"
readme_addition += grp_readme_addition
readme_addition += "## packages\n"
readme_addition += pkg_readme_addition

readme_d = readme_d.replace("[replace]", readme_addition)

with open("README.md", "w") as readme:
    readme.write(readme_d)