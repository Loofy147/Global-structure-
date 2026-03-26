import inspect
import core
import engine
import domains
import theorems
import frontiers

modules = [core, engine, domains, theorems, frontiers]
with open('signatures.txt', 'w') as f:
    for mod in modules:
        f.write(f"--- {mod.__name__} ---\n")
        for name, obj in inspect.getmembers(mod):
            if inspect.isfunction(obj) or inspect.isclass(obj):
                if obj.__module__ == mod.__name__:
                    try:
                        sig = inspect.signature(obj)
                        f.write(f"{name}{sig}\n")
                    except ValueError:
                        f.write(f"{name}(...)\n")
        f.write("\n")
