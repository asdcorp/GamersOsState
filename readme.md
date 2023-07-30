GamersOsState
=============
This repository contains GatherOsState.exe patches developed for the Gamers
Against Weed. All the patches are can be applied using provided `patch.py`
script.

Source binary
-------------
Unless stated otherwise in the release readme of the patch, releases are based
on a x86 GatherOsState.exe taken from the Windows 10 ADK Build 14393.

SHA256 of the source GatherOsState.exe:
```
028c8fbe58f14753b946475de9f09a9c7a05fd62e81a1339614c9e138fc2a21d
```

Patch script usage
------------------
Provided patches require applying using the `patch.py` script. The source file
is patched directly.

```
./patch.py file patch
```

Example usage:
```
./patch.py GatherOsState.exe v1.patch
```

License
-------
Copyright (C) 2022 Gamers Against Weed. All rights reserved.
