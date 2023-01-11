import json
import joblib
import os
import os.path as path
import multiprocessing
import datetime
import scraping.utilities.xml.xml_file_compare as xml_compare
import logging
from tqdm import tqdm

log = logging.getLogger("db_communicator")

def filter_and_sort_annex_files(annex_files: list[str]) -> list[str]:
    """
    Takes a list of filenames ending with "_[number]" and then returns a list 
    where all pre-initial files are filtered out and sorted in ascending order based 
    on the value of [number].
    
    Example:
        input: [EU-1-00-160_h_anx_-1, EU-1-00-160_h_anx_1, EU-1-00-160_h_anx_0]
        Output: [EU-1-00-160_h_anx_0, EU-1-00-160_h_anx_1]

    Args:
        annex_files (list[str]): List of filenames, all ending in "_[number]"

    Returns:
        list[str]: List of filenames where the [number] suffix is in range(0, max int) sorted in ascending order.
    """
    annex_files = [file for file in annex_files if int(file.split(".")[-2].split("_")[-1]) >= 0]
    annex_files.sort(key=lambda annex_name: int(annex_name.split(".")[-2].split("_")[-1]))
    return annex_files
    

def folder_changelog_up_to_date(folder: str, filepath: str) -> bool:
    """
    Returns a bool indicating whether the folder given contains an up-to-date changelog.json.
    If the given filepath is an invalid json file, then the file will be deleted before returning False.

    Args:
        folder (str): Directory of the folder to be checked.
        filepath (str): Filepath to the changelog in folder.

    Returns:
        bool: Boolean indicating whether to write a new changelog in given folder.
    """
    annex_files = [path.join(folder, file) for file in os.listdir(folder) if ".xml" in file and "anx_" in file]
    annex_files = filter_and_sort_annex_files(annex_files)

    try:
        with open(filepath) as comparison_file:
            comparison_dict = json.load(comparison_file)
            changelogs = comparison_dict["changelogs"]
    except FileNotFoundError:
        return len(annex_files) == 0
    except json.JSONDecodeError as e:
        log.warning("ANNEX COMPARER: invalid json file:", filepath, ", file will be deleted | error:", e)
        os.remove(filepath)
        return len(annex_files) == 0
    except Exception as e:
        log.warning("ANNEX COMPARER: cannot determine whether changelog is up to date:", filepath, "file will be updated | error:", e)
        return False
        
    if (len(annex_files) == 0) and len(changelogs) == 0:
        return True

    return (len(annex_files) - 1) == len(changelogs)


def annex_changelog_json_folder(folder: str, replace_all=False, filename_suffix: str = "_annex_changelog.json"):
    """
    Recursively creates a changelog.json for all annex files starting at initial annex within folder and all of its
    subfolders.\n
    Folders containing existing up-to-date changelog.json will be skipped unless replace_all is set to True.\n
    changelog.json files created will be named at directory path.join(folder, path.basename(folder) + filename_suffix).

    Args:
        folder (str): Folder to start recursively create changelog.json files in.
        replace_all (bool, optional): Forces replacing all existing changelog.json files. Defaults to False.
        filename_suffix (str, optional): suffix of changelog.json filename. Defaults to "_annex_changelog.json".
    Returns:
        None
    """    
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
            with open(filename, "w") as comparison_json:
                json.dump(comparisons, comparison_json, default=str)
            log.info("ANNEX COMPARER: created", filename)
        except Exception as e:
            log.warning("ANNEX COMPARER: cannot create", filename, "| error:", e)


def clean_section_text(dict_key: str, change_dict: dict[str, str]) -> str:
    """
    Returns the stripped string in change[dict_key] where all \\n's are replaced with \\n\\t\\t.

    Args:
        dict_key (str): Dictionary key for accessing a string within change.
        change_dict (dict[str, str]): Dictionary containing information on a section single change in an xml file.
            {
                "change": denotes change type: ["added section"|"removed section"|"changed section content"]
                "header": header content of the section changed. e.g. "1 | pharmaceutical form and contents"
                "section_text": Paragraph content of section. Only present for "added section" and "removed section"
                "old_content": Old section content. Only present for "changed section content".
                "new_content": New section content. Only present for "changed section content".
            }

    Returns:
        str: change_dict[dict_key] string with all and \\n's replaced with \\n\\t\\t and unnecessary whitespace removed.
    """    
    enter_seperator = "\n\t\t"
    return enter_seperator.join(list(map(str.strip, change_dict[dict_key].split("\n"))))


def change_dict_to_string(change_dict: dict[str, str]) -> str:
    """
    Returns a change note string for given change_dict using its contents.

    Example:
        input change_dict:
            {
                "change": "changed section content",
                "header": "3 | luxembourg/luxemburg",
                "old_content": "rue de stalle 73 b-1180 bruxelles/br\u00fcssel",
                "new_content": "rue de stalle 73 be-1180 bruxelles/br\u00fcssel"
            }
        output changenote:
            "changed section content: 3 | luxembourg/luxemburg\n

                 new_content:\n
                 rue de stalle 73 b-1180 bruxelles/brüssel\n
            
                 old_content:\n
                 rue de stalle 73 be-1180 bruxelles/brüssel\n
            "
    Args:
        change_dict (dict[str, str]): Dictionary containing information on a section single change in an xml file.
            {
                "change": denotes change type: ["added section"|"removed section"|"changed section content"]
                "header": header content of the section changed. e.g. "1 | pharmaceutical form and contents"
                "section_text": Paragraph content of section. Only present for "added section" and "removed section"
                "old_content": Old section content. Only present for "changed section content".
                "new_content": New section content. Only present for "changed section content".
            }

    Returns:
        str: Changenote string generated from change_dict.  
    """
    text = "\t" + change_dict["change"].strip() + ": " + change_dict["header"].replace("\n", "").strip() + "\n\n"
    keys = change_dict.keys()

    if "section_text" in keys:
        text += "\t\t" + "section_text:\n"
        section_text = clean_section_text("section_text", change_dict)
        text += "\t\t" + section_text + "\n"
    if "new_content" in keys:
        text += "\t\t" + "new_content:\n"
        section_text = clean_section_text("new_content", change_dict)
        text += "\t\t" + section_text + "\n"
    if "old_content" in keys:
        text += "\t\t" + "old_content:\n"
        section_text = clean_section_text("old_content", change_dict)
        text += "\t\t" + section_text + "\n"
        
        text += "\n"

    return text


def changelog_json_to_text(changelog_filepath: str) -> str:
    """
    Returns a formatted changenotes string using the content of the changelog.json at changelog_filepath.

    Example:\n
    input changelog.json:
        {
            "eu_number": "EU-1-00-160",
            "last_updated": "2023-01-09 16:45:15.390951",
            "changelogs": [
                "old_file": "EU-1-00-160_h_anx_0.xml",
                "new_file": "EU-1-00-160_h_anx_1.xml",
                "changes": [
                    {
                        "change": "removed section",
                        "header": "1 | expiry date",
                        "section_text": exp. mm/yyyy"
                    }
                ]
            ]
        }
        
    output changelog text:
        "Medicine: EU-1-00-160\n
         Last updated on 2023-01-09 16:45:15.390951\n
         EU-1-00-160_h_anx_1.xml:\n

         removed section: 1 | expiry date

             section_text:\n
             exp. mm/yyyy\n
        "

    Args:
        changelog_filepath (str): Filepath to a changelog.json file.

    Returns:
        str: String containing the full changenotes for a given changelog.json file.
    """    
    try:
        with open(changelog_filepath, "r") as changelog_json:
            changelog_dict = json.load(changelog_json)
    except Exception as e:
        log.warning("ANNEX COMPARER: could not read:", changelog_filepath, "| error:", e)
        return ""
    
    text = "Medicine" + changelog_dict["eu_number"] + "\nLast updated on " + changelog_dict["last_updated"] + "\n"
    for changelog in changelog_dict["changelogs"]:
        text += changelog["new_file"] + ":\n\n"

        for change_dict in changelog["changes"]:
            text += change_dict_to_string(change_dict)

    return text


def changelog_json_to_text_file(changelog_filepath: str, save_filepath: str):
    """
    Creates a txt file containing a formatted changelog based on given changelog.json.
    If a txt file already exists at save_filepath with a last modified date more recent
    than the changelog.json at changelog_filepath, the function will immediately return.

    Args:
        changelog_filepath (str): Filepath to a changelog.json
        save_filepath (str): Filepath to write the changelog txt file.

    Returns:
        None
    """    
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
        log.warning("ANNEX COMPARER: could not read:", changelog_filepath, "| error:", e)
        return
        
    try:
        changelog_text_file = open(save_filepath, "w", encoding="utf-8")
    except Exception as e:
        log.warning("ANNEX COMPARER: cannot create", save_filepath, "| error:", e)
        return

    for changelog_dict in changelog_dict["changelogs"]:
        try:
            changelog_text_file.write(changelog_dict["new_file"] + ":\n\n")
        except Exception as e:
            log.warning("ANNEX COMPARER: could not write to", changelog_text_file, "| error:", e)
            return
        for change_dict in changelog_dict["changes"]:
            text = change_dict_to_string(change_dict)
            try:
                changelog_text_file.write(text)
            except Exception as e:
                log.warning("ANNEX COMPARER: could not write to", changelog_text_file, "| error:", e)

    changelog_text_file.close()


def annex_changelog_text_folder(folder: str):
    """
    Creates a txt changelog for every changelog.json in the given folder and its subfolders recusively.

    Args:
        folder (str): Directory to search for changelog.jsons within.

    Returns:
        None
    """    
    changelog_jsons = [path.join(folder, file) for file in os.listdir(folder) if "json" in file and "changelog" in file]
    subdirs = [path.join(folder, subdir) for subdir in os.listdir(folder) if path.isdir(path.join(folder, subdir))]

    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(annex_changelog_text_folder)(subdir) for subdir in
        tqdm(subdirs))

    for changelog_json in changelog_jsons:
        changelog_json_to_text_file(changelog_json, changelog_json.replace("json", "txt"))


def main(directory: str):
    """
    Main function of the Annex Comparer Module, creates changelog.json and changelog.txt files
    for all folders and subfolders in given directory.

    Args:
        directory (str): Directory to recursively create annex changelogs in.

    Returns:
        None
    """    
    annex_changelog_json_folder(directory)
    annex_changelog_text_folder(directory)
