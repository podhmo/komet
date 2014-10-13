# -*- coding:utf-8 -*-
import sys
from pyramid.paster import bootstrap

def main():
    config = sys.argv[1]
    env = bootstrap(config)

    registry = env["registry"]
    introspector = registry.introspector

    print("{path:^25} {method:^6} {view_name:^20}".format(
        path="Path",
        method="Method",
        view_name="View"))
    print(u"--------------------------------------------------")

    for d in (introspector.get_category("views")):
        view = d["introspectable"]
        route = None
        for s, category_name, discriminator in view._relations:
            if s and category_name == "routes":
                route = introspector.get(category_name, discriminator)
                break

        if route:
            print("{path:<25} {method:<6} {view_name:<20}".format(
                path=route["pattern"],
                method=view["request_methods"] or "-",
                view_name=view_name(view["callable"], view["attr"])
            ))


def view_name(callable, attr):
    if hasattr(callable, "__name__"):
        name = callable.__name__
    else:
        name = callable.__class__.__name__
    if attr:
        name = name + "#" + attr
    return "{module}:{name}".format(
        module=callable.__module__,
        name=name)
