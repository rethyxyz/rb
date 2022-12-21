# <img src="rb.png">

## Summary
`rb` is a python program that provides a "recycle bin" functionality, allowing the user to move files and directories to a designated recycle bin folder, rather than permanently deleting them. `rb` takes in a list of arguments, including file and directory paths, and options such as `--help`, `--force`, and `--max-mib`. It processes these arguments and then performs actions on the specified files and directories, such as moving them to the recycle bin, renaming them if necessary to avoid conflicts, and deleting them if the `--force` option is provided. `rb` also has the ability to handle large files, and will prompt the user to confirm the deletion of files that exceed a specified maximum size (in mebibytes) if the `--force` option is not provided.

## Features
- Allows you to move files and directories to a recycle bin
- Provides command-line arguments for various options and actions
- Prevents the recycle bin from exceeding a specified maximum size in MiB
- Handles conflicts when moving items with the same name to the recycle bin

## Usage
To use `rb`, simply run it from the command line with the desired options and the paths of the items to be recycled.

Here is an example of how to move a file to the recycle bin:

    python rb.py file.txt

You can also specify multiple items to be recycled at once:

    python rb.py file1.txt file2.txt directory/

## Options
`rb` supports the following command-line options:

- `--help`: Displays usage information and a list of options
- `--force`: Forces the removal of items without prompting for confirmation
- `--max-mib`: Sets the maximum size of the recycle bin in MiB
- `--recycle-bin`: Sets the path of the recycle bin directory

## Recovery
To recover an item from the recycle bin, simply navigate to the recycle bin directory and move the item back to its original location.

## Deletion
To permanently delete an item from the recycle bin, you can use the --force option:

    python rb.py --force file.txt

Alternatively, you can manually delete the item from the recycle bin using your system's file management tools.