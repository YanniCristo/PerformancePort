import importlib
import pkgutil

def register_all_callbacks(app):
    package = __name__

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package}.{module_name}")

        if hasattr(module, "register"):
            module.register(app)
