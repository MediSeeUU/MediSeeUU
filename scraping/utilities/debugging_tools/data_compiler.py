import scraping.utilities.json.json_compiler as jc


# def main():
#     pass

def compile():
    print("starting data compilation")
    compile_dir = "D:\Git_repos\MediSeeUU\data"
    save_dir = "D:\Git_repos\MediSeeUU\data"
    jc.compile_json_file(compile_dir, save_dir, ["combine"], [], True)
    print("data compiled")