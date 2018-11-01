import argparse
import functools
import inspect
import json
import logging
import sys
import time

from jsonschema import validate, ValidationError, SchemaError

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


class BaseTask(object):
    name = str()


def parse_user_params(params: str) -> dict:
    """ Convert json-like params structure decoding it to python dict.
        If 'params' is empty str or not a str at all, return empty dict.
    """

    if not isinstance(params, str) or params == "":
        log.error("Incorrect function params. Must be a non-empty string.")
        return dict()

    try:
        args_dict = json.loads(params.replace("'", '"'))
        log.info(type(args_dict), args_dict.__repr__())
    except json.decoder.JSONDecodeError as e:
        log.exception("Incorrect input data structure. Check your params!", e)
        log.info("I will try to run function with its default args, if any")
    else:
        return args_dict


def validate_schema(user_params: dict, schema: str):
    """ validates params data values with supplied json-schema """
    try:
        validate(user_params, schema)
    except ValidationError as e:
        log.error("Incorrect input data values.",
                  "\nValid schema:", schema, "\nError:", e)
        raise
    except SchemaError as e:
        log.error("Incorrect validation schema", e)
        raise


def run_cli():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    func_callables = dict()
    cls_callables = dict()

    # First find and register all the functions that have been decorated and therefore has "name" attr
    all_functions = inspect.getmembers(sys.modules["__main__"], inspect.isfunction)
    # print("all_functions", all_functions)

    for func_name, func_obj in all_functions:
        func_parser = subparser.add_parser(func_name)
        func_parser.add_argument("-p", "--params", dest="params", type=str)

        if hasattr(func_obj, "name"):
            func_callables[func_obj.name] = func_obj
            func_parser = subparser.add_parser(func_obj.name)
            func_parser.add_argument("-p", "--params", dest="params")

    # Then inspect also classes in the module, if they have "name" field, register parsers too
    all_classes = inspect.getmembers(sys.modules["__main__"], inspect.isclass)
    # print("all_classes", all_classes)

    for cls_name, cls_obj in all_classes:
        cls_parser = subparser.add_parser(cls_name)
        cls_parser.add_argument("-p", "--params", dest="params", type=str)

        if hasattr(cls_obj, "name"):
            try:
                getattr(cls_obj, "run")
            except AttributeError as e:
                log.exception("Class " + cls_name + " has no run() method! Skipping.\n Error details:", e)
            else:
                cls_instance = cls_obj()
                cls_callables[cls_obj.name] = cls_instance.run, cls_instance
                cls_parser = subparser.add_parser(cls_obj.name)
                cls_parser.add_argument("-p", "--params", dest="params")

    args = parser.parse_args()
    # print("args.command:", args.command, type(args.command))

    # if desired command is a function - return it, otherwise look in class methods
    func_to_run, cls_inst = (func_callables.get(args.command), None) if (
            args.command in func_callables) else cls_callables.get(args.command)
    if not func_to_run:
        log.error("No any callable found with specified 'name'. Exiting...")
        return None

    # print("args.params:", args.params)
    user_params = parse_user_params(args.params)
    if user_params and cls_inst:
        log.info("validate class method schema", cls_inst.json_schema)
        validate_schema(user_params, cls_inst.json_schema)
    elif user_params and inspect.isfunction(func_to_run):
        log.info("validate function schema", func_to_run.json_schema)
        validate_schema(user_params, func_to_run.json_schema)

    return func_to_run(**user_params)


def task(name, json_schema):
    """ task - wraps decorates function allowing it running from CLI """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.name = name
        wrapper.json_schema = json_schema
        return wrapper

    return decorator


def delayed(attempts, delay_before_retry_sec):
    """ delayed - recover decorated function when it's failed, with specified timeout and number of retries """
    def internal(func):
        def wrapper(*args, **kwargs):
            attempts_counter = int()
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts_counter += 1
                    if attempts_counter >= attempts:
                        raise e
                    time.sleep(delay_before_retry_sec)
                    continue

        return wrapper

    return internal
