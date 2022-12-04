from pathlib import Path, PurePath

def resolve_root_path():
    return "." # Path(__file__).parent.resolve().parts[0]

def resolve_path_to_frontend_public():
    cwd = Path(__file__).parent.resolve()
    grandparent = cwd.parent.parent
    return grandparent / "report-frontend" / "public"

