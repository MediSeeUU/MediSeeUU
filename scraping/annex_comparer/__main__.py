import json
import joblib
import os
import os.path as path
import multiprocessing
import datetime
import scraping.utilities.xml.xml_file_compare as xml_compare
import scraping.utilities.log as log
from tqdm import tqdm


def filter_and_sort_annex_files(annex_files: list[str]) -> list[str]:
    annex_files = [file for file in annex_files if int(file.split(".")[-2].split("_")[-1]) >= 0]
    annex_files.sort(key=lambda annex_name: int(annex_name.split(".")[-2].split("_")[-1]))
    return annex_files
    

def folder_changelog_up_to_date(folder: str, filepath: str) -> bool:
    annex_files = [path.join(folder, file) for file in os.listdir(folder) if ".xml" in file and "anx_" in file]
    annex_files = filter_and_sort_annex_files(annex_files)

    try:
        with open(filepath) as comparison_file:
            comparison_dict = json.load(comparison_file)
            changelogs = comparison_dict["changelogs"]
    except FileNotFoundError:
        return len(annex_files) == 0
    except json.JSONDecodeError as e:
        print("ANNEX COMPARER:", e, "| invalid json file:", filepath, ", file will be deleted")
        os.remove(filepath)
        return len(annex_files) == 0
    except Exception as e:
        print("ANNEX COMPARER:", e, "| cannot determine whether changelog is up to date:", filepath)
        return False
        
    if (len(annex_files) == 0) and len(changelogs) == 0:
        return True

    return (len(annex_files) - 1) == len(changelogs)


def annex_changelog_json_folder(folder: str, replace_all=False, filename_suffix: str = "_annex_changelog.json"):
    annex_files = [path.join(folder, file) for file in os.listdir(folder) if ".xml" in file and "anx_" in file]
    annex_files = filter_and_sort_annex_files(annex_files)
    annex_files.sort(key=lambda annex_name: int(annex_name.split(".")[-2].split("_")[-1]))
    subdirs = [path.join(folder, subdir) for subdir in os.listdir(folder) if path.isdir(path.join(folder, subdir))]
    comparisons = {"eu_number": path.basename(folder),
                   "last_updated": datetime.datetime.now(),
                   "changelogs": []}
    filename = path.join(folder, path.basename(folder) + filename_suffix)

    if folder_changelog_up_to_date(folder, filename) and not replace_all:
        annex_files = []

    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(annex_changelog_json_folder)(subdir) for subdir in
        tqdm(subdirs))

    comparisons["changelogs"] = joblib.Parallel(
        n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(xml_compare.compare_xml_files_dict)(annex_files[i], annex_files[i - 1]) for i in
        range(1, len(annex_files)))

    # single threaded version for debugging
    # for subfolder in subfolders:
    #     compare_annexes_folder(subfolder)

    # for i in range(1, len(annex_files)):
    #     comparisons["changelogs"].append(compare_xml_files_dict(annex_files[i], annex_files[i - 1]))

    if len(annex_files) > 0:
        try:
            print("writing to file", str(filename))
            with open(filename, "w") as comparison_json:
                json.dump(comparisons, comparison_json, default=str)
        except Exception as e:
            print("ANNEX COMPARER: cannot write", filename)
            print(e)


def clean_section_text(change_key: str, change: dict[str, str]) -> str:
    enter_seperator = "\n\t\t"
    return enter_seperator.join(list(map(str.strip, change[change_key].split("\n"))))


def change_dict_to_string(change: dict[str, str]) -> str:
    text = "\t" + change["change"].strip() + ": " + change["header"].replace("\n", "").strip() + "\n\n"
    keys = change.keys()

    if "section_text" in keys:
        text += "\t\t" + "section_text:\n"
        section_text = clean_section_text("section_text", change)
        text += "\t\t" + section_text + "\n"
    if "new_content" in keys:
        text += "\t\t" + "new_content:\n"
        section_text = clean_section_text("new_content", change)
        text += "\t\t" + section_text + "\n"
    if "old_content" in keys:
        text += "\t\t" + "old_content:\n"
        section_text = clean_section_text("old_content", change)
        text += "\t\t" + section_text + "\n"
        
        text += "\n"

    return text


def changelog_json_to_text(changelog_filepath: str) -> str:
    try:
        with open(changelog_filepath, "r") as changelog_json:
            changelog_dict = json.load(changelog_json)
    except Exception:
        print("ANNEX COMPARER:", changelog_filepath, "does not exist")
        return ""
    
    text = ""
    for changelog in changelog_dict["changelogs"]:
        text += changelog["new_file"] + ":\n\n"

        for change_dict in changelog["changes"]:
            text += change_dict_to_string(change_dict)

    return text


def changelog_json_to_text_file(changelog_filepath: str, save_filepath: str):
    # skip making new annex_changelog.txt if the existing one is up-to-date
    try:
        json_modify_date = path.getmtime(changelog_filepath)
        txt_modify_date = path.getmtime(changelog_filepath.replace(".json", ".txt"))
        if json_modify_date < txt_modify_date:
            return
    except Exception:
        pass  # should try to make a new annex_changelog.txt if failed
    
    try:
        with open(changelog_filepath, "r") as changelog_json:
            changelog_dict = json.load(changelog_json)
    except Exception as e:
        print("ANNEX COMPARER:", e, "| file does not exist:", changelog_filepath)
        return
        
    try:
        changelog_text_file = open(save_filepath, "w", encoding="utf-8")
    except Exception as e:
        print("ANNEX COMPARER:", e, "| cannot create", save_filepath)
        return

    for changelog_dict in changelog_dict["changelogs"]:
        try:
            changelog_text_file.write(changelog_dict["new_file"] + ":\n\n")
        except Exception as e:
            print(e)
            return
        for change_dict in changelog_dict["changes"]:
            text = change_dict_to_string(change_dict)
            try:
                changelog_text_file.write(text)
            except Exception as e:
                print("ANNEX COMPARER:", e, "| cannot write line: ", text)

    changelog_text_file.close()


def annex_changelog_text_folder(folder: str):
    changelog_jsons = [path.join(folder, file) for file in os.listdir(folder) if "json" in file and "changelog" in file]
    subdirs = [path.join(folder, subdir) for subdir in os.listdir(folder) if path.isdir(path.join(folder, subdir))]

    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(annex_changelog_text_folder)(subdir) for subdir in
        tqdm(subdirs))

    for changelog_json in changelog_jsons:
        changelog_json_to_text_file(changelog_json, changelog_json.replace("json", "txt"))


def main(directory: str):
    annex_changelog_json_folder(directory)
    annex_changelog_text_folder(directory)
