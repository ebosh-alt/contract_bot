from jinja2 import Environment, PackageLoader, select_autoescape


def get_tmp(path: str, *args):
    env = Environment(
        loader=PackageLoader(package_name="bot", package_path="admin_panel/src/templates", encoding="utf-8"),
        autoescape=select_autoescape(['html', 'xml'])
    )
    tmpl = env.get_template(path)
    return tmpl.render(args[0])
