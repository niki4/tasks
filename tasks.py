import argparse
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
    """ convert json-like params structure decoding it to python dict """

    if not isinstance(params, str):
        log.error("Incorrect function param. Must be a string.")
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
        raise e
    except SchemaError as e:
        log.error("Incorrect validation schema", e)
        raise e


def run_cli():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    func_callables = dict()
    cls_callables = dict()

    # First find and register all the functions that have been decorated and therefore has "name" attr
    all_functions = inspect.getmembers(sys.modules["__main__"], inspect.isfunction)
    print("all_functions", all_functions)

    for func_name, func_obj in all_functions:
        print(vars(func_obj))
        # print(dir(inspect.unwrap(func_obj)))
        # print(getattr(func_obj, "name", None))
        # print(func_obj.__name__, inspect.getfullargspec(func_obj))

        func_parser = subparser.add_parser(func_name)
        func_parser.add_argument("-p", "--params", dest="params", type=str)
        # if hasattr(func_obj, "name"):
        func_callables[func_name] = func_name             # TODO: Collect only those where 'name' arg set in decorator
        #     func_parser = subparser.add_parser(func_name)
        #     func_parser.add_argument("-p", "--params", dest="params")

    # Then inspect also classes in the module, if they have "name" field, register parsers too
    all_classes = inspect.getmembers(sys.modules["__main__"], inspect.isclass)
    print("all_classes", all_classes)

    for cls_name, cls_obj in all_classes:
            cls_parser = subparser.add_parser(cls_name)
            cls_parser.add_argument("-p", "--params", dest="params", type=str)

            if hasattr(cls_obj, "name"):
                print(cls_name, "cls_obj.name:", getattr(cls_obj, "name"), type(cls_obj.name))
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
    print("args.command", args.command, type(args.command))

    # if desired command is a function - return it, otherwise look in class methods
    func_to_run, cls_inst = (getattr(sys.modules["__main__"], func_callables.get(args.command), None), ) if (
            args.command in func_callables) else cls_callables.get(args.command)
    if not func_to_run:
        log.error("No any callable found with specified 'name'. Exiting...")
        return None

    print("args:", args)
    print("args.params:", args.params)

    # args_dict = dict()
    user_params = parse_user_params(args.params)
    if user_params and cls_inst:
            log.info("cls_inst.json_schema", cls_inst.json_schema)
            validate_schema(user_params, cls_inst.json_schema)

    # if args.params:
    #     # validate json-like params structure with decoding it to python dict
    #     try:
    #         args_dict = json.loads(args.params.replace("'", '"'))
    #         log.info(type(args_dict), args_dict.__repr__())
    #     except json.decoder.JSONDecodeError as e:
    #         log.exception("Incorrect input data structure. Check your params!\nError:", e)
    #         log.info("I will try to run function with its default args, if any")
    #
    #     # validate params data values with supplied json-schema
    #     try:
    #         schema = getattr(func_to_run, "json_schema")
    #         validate(args_dict, schema)
    #     except AttributeError as e:
    #         log.exception("No attribute 'json_schema' in specified function.", e)
    #     except ValidationError as e:
    #         log.error("Incorrect input data values.", "\nValid schema:",
    #                   func_to_run.schema, "\nError:", e)

    return func_to_run(**user_params)


# task - wraps decorated function allowing it running from CLI
def task(name, json_schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(name, "-" * 5)
            print(json_schema)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# delayed - Recover decorated function when it's failed, with specified timeout and number of retries
def delayed(attempts, delay_before_retry_sec):
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

def get_attrs(obj):
    attrs = set(obj.__dict__)
    for cls in obj.__class__.__mro__:
        attrs.update(cls.__dict__)
    return sorted(attrs)