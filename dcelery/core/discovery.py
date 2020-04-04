from werkzeug.utils import import_string, find_modules


def auto_discovery():
    for mod in find_modules("modules", recursive=True):
        if str(mod).endswith("tasks"):
            import_string(mod)
        elif str(mod).endswith("models"):
            import_string(mod)
