# Python Module Import: Handling Relative Imports

## Table of Contents

1. [Abstract](#abstract)
2. [Issue #1](#issue-1)
3. [Issue #2](#issue-2)
4. [Solution](#solution)
5. [Example](#example)

## Abstract

### Issue overview

This repository addresses two common issues encountered in Python programming related to the import mechanism of modules. Specifically, it discusses the challenges faced when importing a module (module A) into another module (module B) using relative paths.

An issue occurs when:
- the execution context shifts outside the project directory
- performing a relative import using dot notation while running the script as standalone.

The first issue arises due to the relative import path in module B becoming invalid when the execution context changes to a directory outside the project, such as when importing module B from a main file located elsewhere.

The second issue arises when a module - in this case module B - is run as a script and attempts to import another module, module A, that resides outside of its parent directory (or any of its subdirectories) by traversing up the directory hierarchy using dot notation.

###  Summarized solution
The proposed solution involves appending the absolute path of the shared top-level directory of module A and B to the system path (`sys.path`).

This approach ensures the successful import of module A irrespective of the execution context, thereby resolving the first issue of relative import failures.

Furthermore, it eliminates the need for relative imports using dot notation. Consequently, the second issue associated with relative import failures when the script is run directly, is effectively resolved.



## Issue #1

The issue at hand pertains to the scope of Python's module import mechanism. When importing module A into module B using a relative path, the import operation is successful as long as the execution context remains within the directory where module B is located, referred to here as the project directory. However, difficulties arise when attempting to import module B from a main file located outside this project directory.

The relative import path in module B, which is valid in the context of the project directory, becomes invalid when the execution context changes to the directory of the main file. This is because Python's import function searches for modules in the directories listed in `sys.path`. By default, `sys.path` includes the directory of the script that was used to invoke the Python interpreter, which would be the directory of the main file in this case. If module B is not in the same directory as the main file, or in a directory that has been added to `sys.path`, Python will not be able to find the relative path used in module_B, resulting in an import error.

One could adjust the relative import path in module B to be valid in the context of the main file, but this would then break the ability to execute module B as a standalone script within the project directory.


## Issue #2

In Python, the dot notation in import statements is used for relative imports. A single dot represents the current package or directory, two dots represent the parent directory, and so on. Therefore, if module B wants to import module A that resides in the directory above its own, it would use two dots in the import statement.

However, this approach has a limitation. Python's relative imports are designed to work within a package. When Python encounters a dot in an import statement, it tries to resolve it relative to the current module's directory. If the current module is not part of a package (which is the case when the module is run as a standalone script), or if the import statement tries to navigate above the top-level package, Python raises an ImportError.

The reason for this behavior lies in the way Python handles imports. When a script is run directly, Python sets `__name__` to `"__main__"` and does not consider the script to be part of a package, even if it physically resides within a package's directory structure. As a result, relative imports, which rely on the script being part of a package, fail. On the other hand, when the script is imported as a module, Python recognizes the package structure, and relative imports work as expected.


## Solution

A viable, and probably the only simple solution to the issues of relative imports in Python is to append the absolute path of the shared top-level directory to the system path (`sys.path`). This shared top-level directory represents the first directory that is common between the current module (module B in this example) and the module being imported (module A). By appending the path of this shared top-level directory to `sys.path`, Python is instructed to also search in this directory when attempting to import modules and it eliminates the need for relative imports using dot notation.

This appending is done in the module where the import of module A is needed, by leveraging the `__file__` attribute. This attribute consistently provides the path to the file in which it is used - in this example module B - regardless of the execution context.

The `os.path.realpath()`, `os.path.join()` and `os.path.dirname()` functions are used to calculate the absolute path to the shared top-level directory from the current file. This absolute path is then added to `sys.path`, allowing Python to successfully import module A even when the execution context changes or module A resides outside of module B's parent directory.

Alternatively, directly appending module A's absolute path to `sys.path` would also work. In this case, module A would be imported without any prefixes, as `import module_A`. However, this method triggers an unresolved import warning from Pylance, despite successful runtime import, impacting code readability.



## Example

`main.py` imports from `module_B.py`, which in turn imports from `module_A.py` and `module_C.py`. To ensure the successful import from `module_A.py` and `module_C.py` regardless of whether the execution context is `main.py` or `module_B.py`, it is necessary to append the absolute path of their shared top-level directory to `sys.path` and import relative to it.

```
my_project
├───main.py
└───my_package
    ├───my_modules_A
    │   └───module_A.py
    └───my_modules_BC
        ├───module_B.py
        └───module_C.py
```

[`module_B.py`](my_package/my_modules_BC/module_B.py) could look like this:
```python
import sys, os

# relative paths to shared top level directories with module A and C
relative_paths = []
relative_paths.append('../../') # for module_A
relative_paths.append('') # for module_C

# calculate absolute paths and append to sys.path
for path in relative_paths:
    absolute_path = os.path.realpath(os.path.join(os.path.dirname(__file__), path))
    sys.path.append(absolute_path)

from my_package.my_modules_A.module_A import foo_module_A
from module_C import foo_module_C
```

The following code is from [`main.py`](main.py):
```python
from my_package.my_modules_BC.module_B import foo_module_B
```



### Try it out
This repository contains all the necessary files to reproduce the scenario described above. Feel free to experiment with alternatives to manage relative imports, and see how they most likely will fail in one way or the other ;)