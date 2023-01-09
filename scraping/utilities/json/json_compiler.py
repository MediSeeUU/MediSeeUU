import json
import os.path as path
from os import listdir


def compile_json_dict(compile_dir: str, incl_substr: list[str], excl_substr: list[str] = [],
                      subdirectories: bool = True) -> dict[str, dict]:
    """
    Returns a dict containing the following key-value pairs:
    "directory": a string indicating which folder data was compiled from.
    "files": a list of dictionaries containing { "json_file_name": json_file_content } dictionaries
    "subdirectories": a list containing dictionaries with same key-value pairs representing data found in subdirectories.

    Args:
        compile_dir (str): directory where to start looking for json files.
        incl_substr (list[str]): list of substrings which filenames must contain at least one of.
        excl_substr (list[str], optional): list of substrings which filenames must contain none of. Defaults to [].
        subdirectories (bool, optional): indicates whether to compile jsons from subdirectories. Defaults to True.
    Returns:
        dict[str, dict]: dictionary containing a compilation of all json files found in compile_dir \
                         and optionally in subdirectories
    """
    dir_content = [path.join(compile_dir, content) for content in listdir(compile_dir)]

    files = [file for file in dir_content if path.isfile(file)]
    subdirs = [subdir for subdir in dir_content if path.isdir(subdir)]
    compiled_dict = {}
    file_dicts = []
    subdir_dicts = []

    if subdirectories:
        for subdir in subdirs:
            subdir_dicts.append(compile_json_dict(subdir, incl_substr, excl_substr, subdirectories))

    for file in files:
        contains_included = any(substring in path.basename(file) for substring in incl_substr)
        contains_excluded = any(substring in path.basename(file) for substring in excl_substr)
        is_json_file = ".json" in path.basename(file)

        if is_json_file and contains_included and not contains_excluded:
            try:
                with open(file) as json_file:
                    json_dict = json.load(json_file)
                    file_dicts.append({path.basename(file): json_dict})
            except Exception:
                print("failed to open or load \"", file + "\"", "in compile_json_dict")

    compiled_dict[path.basename(compile_dir)] = {"directory": compile_dir, "files": file_dicts,
                                                 "subdirectories": subdir_dicts}
    return {"directory": compile_dir, "files": file_dicts, "subdirectories": subdir_dicts}


def compile_json_file(compile_dir: str, save_dir: str, incl_substr: list[str], excl_substr: list[str] = [],
                      subdirectories: bool = True):
    """
    Saves a compiled.json file at save_dir which contains an compilation of all json files which contain 
    at least one item from incl_substr in their filename and none from excl_substr. With optional subdirectories
    traversal within compile_dir.
    

    Args:
        compile_dir (str): directory where to start looking for json files.
        save_dir (str): directory where compiled.json will be saved.
        incl_substr (list[str]): list of substrings which filenames must contain at least one of.
        excl_substr (list[str], optional): list of substrings which filenames must contain none of. Defaults to [].
        subdirectories (bool, optional): indicates whether to compile jsons from subdirectories. Defaults to True.
    """
    compiled_dict = compile_json_dict(compile_dir, incl_substr, excl_substr, subdirectories)

    with open(path.join(save_dir, "compiled.json"), "w") as compiled_json:
        json.dump(compiled_dict, compiled_json, indent = 4)


def compile_json_files(directory: str, save_dir: str, add_webdata: bool = True, add_pdfdata: bool = True):
    """
    Combines JSONs from PDF scraper and/or web scraper

    Args:
        directory (str): Data folder containing the categories of medicines:
        save_dir (str): Folder where all_json_results.json will be saved
        add_webdata (bool): Whether to add web data json files
        add_pdfdata (bool): Whether to add pdf data json files
    """
    meds_dir = f"{directory}/active_withdrawn"

    subdirectories = [subdirectory for subdirectory in listdir(meds_dir) if
                      path.isdir(path.join(meds_dir, subdirectory))]

    medicine_json_list = []

    for subdirectory in subdirectories:
        get_medicine_json(path.join(meds_dir, subdirectory), medicine_json_list, add_webdata, add_pdfdata)

    all_json_results = open(path.join(save_dir, "all_json_results.json"), "w")
    json.dump(medicine_json_list, all_json_results, indent = 4)
    all_json_results.close()


def get_medicine_json(medicine_path: str, json_list: list[dict], add_webdata: bool, add_pdfdata: bool):
    """

    Args:
        medicine_path (str): Path to medicine folder containing json files
        json_list (list[dict]): List of dictionaries from all json files
        add_webdata (bool): Whether to add web data json files
        add_pdfdata (bool): Whether to add pdf data json files
    """
    medicine_jsons = [file for file in listdir(medicine_path) if path.isfile(path.join(medicine_path, file))]
    if add_webdata and add_pdfdata:
        medicine_jsons = [file for file in medicine_jsons if "webdata.json" in file or "pdf_parser.json" in file]
    elif add_webdata:
        medicine_jsons = [file for file in medicine_jsons if "webdata.json" in file]
    elif add_pdfdata:
        medicine_jsons = [file for file in medicine_jsons if "pdf_parser.json" in file]

    for medicine_json in medicine_jsons:
        with open(path.join(medicine_path, medicine_json)) as json_file:
            try:
                medicine_json_dir = json.load(json_file)
                json_list.append(medicine_json_dir)
            # TODO: Add specific exception handling
            except:
                return
