#!/usr/bin/env python

import argparse


cli = argparse.ArgumentParser()
subparsers = cli.add_subparsers(dest="subcommand")


def argument(*name_or_flags, **kwargs):
    """Convenience function to properly format arguments to pass to the
    subcommand decorator.
    """
    return (list(name_or_flags), kwargs)


def subcommand(args=[], extend_args_func=None, parent=subparsers):
    """Decorator to define a new subcommand in a sanity-preserving way.
    The function will be stored in the ``func`` variable when the parser
    parses arguments so that it can be called directly like so::
        args = cli.parse_args()
        args.func(args)
    Usage example::
        @subcommand([argument("-d", help="Debug mode", action="store_true")])
        def subcommand(args):
            print(args)
    Then on the command line::
        $ python cli.py subcommand -d
    """
    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        if extend_args_func:
            extend_args_func(parser)
        parser.set_defaults(func=func)
        # return parser for multi-level subcommand, see test2
        return parser
    return decorator


@subcommand([argument("name", help="hello, name!")])
def hello(name):
    print("Hello, " + name + '!')


def conflict_group(parser):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--foo", action="store_true")
    group.add_argument("--bar", type=str)


@subcommand(extend_args_func=conflict_group)
def test(foo, bar):
    """
    This is test command for extend args function.
    """
    print(foo, bar)


# multi-level subcommand
@subcommand()
def test2():
    pass


test2_subparser = test2.add_subparsers(dest='subcommand')


@subcommand([argument('--foo')], parent=test2_subparser)
def test2sub(foo):
    print("this is subcommand for test2.")
    print(foo)


def main():
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        kwargs = {}
        for k, v in args._get_kwargs():
            if k not in ['func', 'subcommand']:
                kwargs[k] = v
        args.func(**kwargs)


if __name__ == "__main__":
    main()
