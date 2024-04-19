import sys, os

# relative paths to shared top level directories with module A and C
relative_paths = []
relative_paths.append('../../') # for module_A
relative_paths.append('') # for module_C

# calculate absolute paths and append to sys.path
for path in relative_paths:
    absolute_path = os.path.realpath(os.path.join(os.path.dirname(__file__), path))
    sys.path.append(absolute_path)

filename = os.path.basename(__file__)
try:
    from my_package.my_modules_A.module_A import foo_module_A
except ImportError as e:
    print(f'{filename}: ', e)
else:
    print(f'{filename}: successfully imported from module_A')

try:
    from module_C import foo_module_C
except ImportError as e:
    print(f'{filename}: ', e)
else:
    print(f'{filename}: successfully imported from module_C')

def foo_module_B():
    pass