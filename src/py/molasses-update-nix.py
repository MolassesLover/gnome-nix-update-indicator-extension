#!/usr/bin/env python

import json
import subprocess
import os
import sys

from pathlib import Path


def sanitize_arguments(arguments_list: list) -> str:
    disallowed_characters = [";", "{", "}", "(", ")", "$"]

    for argument in arguments_list:
        for character in disallowed_characters:
            if character in argument:
                raise Exception(
                    f"Found illegal character `{character}` in `{argument}`."
                )

    argument_list_string = " ".join(arguments_list)

    return argument_list_string


def main():
    configuration: dict = {
        "flake_directory": None,
        "flake_directory_parent": None,
        "flake_hostname": None,
        "flake_source": None,
        "impure": False,
        "switch": True,
    }

    home_directory: str = str(Path.home())
    config_directory: str = f"{home_directory}/.config/molasses/update-nix"
    config_path: str = f"{config_directory}/config.json"
    initialize_config: bool = False

    if not Path.exists(Path(config_directory)):
        os.makedirs(config_directory)

        initialize_config = True

    if not Path.exists(Path(config_path)):
        initialize_config = True

    if initialize_config:
        with open(config_path, "w", encoding="utf-8") as config_file:
            json.dump(configuration, config_file, indent=4)

            print(
                f":: Error: No configuration file was found, wrote a template of it to `{config_path}`."
            )

            print(
                ":: Please edit this file to your liking, before running this script again."
            )

            sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as config_file:
        config_data = config_file.read()
        configuration = json.loads(config_data)

    os.putenv("SHELL", "/bin/sh")

    additional_arguments_list: list[str] = []
    rebuild_task = None

    if configuration["impure"]:
        additional_arguments_list.append("--impure")

    if configuration["switch"]:
        rebuild_task = "switch"
    else:
        rebuild_task = "boot"

    additional_arguments = sanitize_arguments(additional_arguments_list)

    if not configuration["flake_directory"]:
        print(":: Error: 'flake_directory' option not specified.")
        sys.exit(1)
    if not configuration["flake_hostname"]:
        print(":: Error: 'flake_hostname' option not specified.")
        sys.exit(1)

    if configuration["flake_directory"] and configuration["flake_hostname"]:
        flake_directory = f"{configuration['flake_directory_parent']}/{configuration['flake_directory']}"
        flake_directory_parent = configuration["flake_directory_parent"]
        flake_hostname = configuration["flake_hostname"]
        flake_source = configuration["flake_source"]

        update_command: str = (
            f"nix flake update; sudo nixos-rebuild {rebuild_task} --upgrade --flake .#{flake_hostname} {additional_arguments}"
        )

        if not Path.exists(Path(flake_directory)):
            if not flake_source:
                raise Exception(f"Flake directory not found, and no source provided.")
            else:
                os.makedirs(flake_directory_parent)

                print(":: Cloning {flake_source} using Git")

                subprocess.run(
                    f"git clone --recursive {flake_source}",
                    cwd=flake_directory_parent,
                    shell=True,
                    check=True,
                )

        if Path.exists(Path(flake_directory)):
            subprocess.run(
                str(update_command), cwd=flake_directory, shell=True, check=True
            )
        else:
            raise Exception(
                "Flake directory not found, despite earlier creation attempt."
            )
            
if __name__ == "__main__":
    main()
