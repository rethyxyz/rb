# rb
A Windows-like recycle bin system for Unix-like systems.

## Flags
- -f, --force

        Invoke a recycle bin bypass. All files listed using this flag are deleted and NOT placed in your recycle bin.

        Example:
            rb.py -f file1 dir1

- -rb, --recycle-bin

        Manually specify a recycle bin path.

        Example:
            rb.py -rb ~/tempbin/
        
        Default:
            ~/rb/

- -h, --help

        Display help information.

- -m, --max-mib

        Specify the max MiB file or directory your recycle bin will hold.

        Default:
            20000000000 (20000 MiB)