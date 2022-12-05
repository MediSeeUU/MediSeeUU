import pathlib


class Path(pathlib.Path):
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
