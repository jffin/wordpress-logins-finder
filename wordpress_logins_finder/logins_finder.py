#!/usr/bin/env python

"""
Entrypoint to script.
The main goal of the script is to gather possible open WordPress API's endpoints
that expose user details.
"""
import argparse
import asyncio
import json
import logging
from time import time
from typing import NamedTuple, List, Union, Dict

from utils.constants import Config, targets_to_check, Types
from utils.logger_formater import OneLineExceptionFormatter
from wordpress_logins_finder.utils.request_manager import probe_target_schema, RequestManager


class RunConfig(NamedTuple):
    """
    Run Config for script args
    """
    domain: str
    verbose: bool = Config.DEFAULT_DEBUGGING
    output: str = Config.RESULT_FILE_NAME


def define_config_from_cmd(parsed_args: 'argparse.Namespace') -> RunConfig:
    """
    parsing config from args
    :param parsed_args: argparse.Namespace
    :return: RunConfig
    """
    return RunConfig(
        domain=parsed_args.domain,
        verbose=parsed_args.verbose,
        output=parsed_args.output,
    )


def cli() -> argparse.Namespace:
    """
    here we define args to run the script with
    :return: argparse.Namespace
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='scan list of urls')
    # Add the arguments to the parser
    parser.add_argument('-d', '--domain', type=str, required=True, help='Target domain')
    parser.add_argument('-v', '--verbose', action='store_true', default=Config.DEFAULT_DEBUGGING,
                        required=False, help='Verbose debug messages')
    parser.add_argument('-o', '--output', type=str, default=Config.RESULT_FILE_NAME,
                        required=False, help='Output file name')

    return parser.parse_args()


def write_results_to_file(results: Types.ASYNCIO_GATHER) -> None:
    """
    Method to save results in json into a file
    :param results:
    """
    with open(Config.RESULT_FILE_NAME, 'w') as file:
        file.write(json.dumps(results))
    logging.log(logging.DEBUG, f'Wrote results to file with name: {Config.RESULT_FILE_NAME}')


async def main() -> None:
    """
    Entrypoint to run the program
    """
    args: argparse.Namespace = cli()
    run_config: RunConfig = define_config_from_cmd(args)

    OneLineExceptionFormatter.logger_initialisation(run_config.verbose)
    logging.log(logging.DEBUG, 'Main Started')

    schema: str = await probe_target_schema(run_config.domain)
    logging.log(logging.DEBUG, f'Target Schema: {schema}')
    target: str = f'{schema}://{run_config.domain}'
    logging.log(logging.DEBUG, f'Target: {target}')

    possible_urls: List[str] = targets_to_check(target)
    logging.log(logging.DEBUG, f'Possible Targets: {possible_urls}')

    results: Types.ASYNCIO_GATHER = await RequestManager.create_make_requests(possible_urls)
    results: List[Dict[str, Union[str, int]]] = list(filter(None, results))

    write_results_to_file(results)


if __name__ == '__main__':
    try:
        start_time = time()
        asyncio.run(main(), debug=Config.DEFAULT_DEBUGGING)
        logging.log(logging.DEBUG, f'Time consumption: {time() - start_time: 0.3f}s')
    except Exception as error:
        logging.exception(f'Failed with: {error}')
