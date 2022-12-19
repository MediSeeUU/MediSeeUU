import pathlib


# Scuffed arguments required as set out in this SO post:
# https://stackoverflow.com/questions/29850801/subclass-pathlib-path-fails
class Path(type(pathlib.Path())):
    def rmdir(self, not_exist_ok=False):
        """
        Overwrite for parent class rmdir method. Allows the user to specify whether the method should fail if the
        directory does not exist

        Args:
            not_exist_ok: Boolean value that specifies whether the method should fail if the path does not exist.

        Returns: None

        """
        if not_exist_ok and not self.exists():
            return

        super().rmdir()

    def rmdir_recursive(self, not_exist_ok=False):
        """
        Function to remove all files in a specified directory
        and removing the directory itself as well afterwards

        Args:
            not_exist_ok:

        Returns: None

        """
        if not_exist_ok and not self.exists():
            return

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
