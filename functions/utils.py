import os

def try_except(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return f"Error: {e}"

def abs_path(path):
    return try_except(os.path.abspath, path)
 
def merge_paths(absolute_path, relative_path):
    joined = try_except(os.path.join, absolute_path, relative_path)
    return abs_path(joined)

 