import pathlib


# Scuffed arguments required as set out in this SO post:
# https://stackoverflow.com/questions/29850801/subclass-pathlib-path-fails
class Path(type(pathlib.Path())):
    def rmdir_recursive(self):
        """
        Function to remove all files in a specified directory
        and removing the directory itself as well afterwards

        Returns: None
        """
        for sub in self.iterdir():
            if sub.is_dir():
                sub.rmdir_recursive()
            else:
                sub.unlink()
        self.rmdir()

    def iterdir_files(self):
        """
        Alternative to iterdir method.
        Returns only files, not directories.
        """
        # Makes use of Generators. Documentation can be found here:
        # https://wiki.python.org/moin/Generators
        for path_obj in self.iterdir():
            if path_obj.is_dir():
                continue

            yield path_obj
