#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import xml.etree.ElementTree as ET
import sys
import os
from pathlib import Path
import subprocess
import sys
import logging
import itertools
from functools import partial
from dataclasses import dataclass, field

from yaml import load, dump
from lxml import etree as ET

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
# Log
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("BUILD")
logger.setLevel(logging.DEBUG)
# build methods
def callCommand(command, *args):
    commands = [command] + list(args)
    for command in commands:
        logger.debug(command)
        subprocess.run(command, shell=True)


def writeQrc(resources, qrc_path):
    qrc_file = Path(qrc_path)
    def addResource(resource_path):
        resource_path = Path(resource_path)
        if resource_path.is_file():
            newFile = ET.SubElement(qresource, "file")
            newFile.text = str(resource_path.relative_to(qrc_file.parent).as_posix())
            return newFile
        elif resource_path.is_dir():
            return [addResource(f) for f in resource_path.rglob("*") if f.is_file()]

    RCC = ET.Element("RCC")
    qresource = ET.SubElement(RCC, "qresource")
    qresource.set("prefix", "/")
    for resource in resources:
        addResource(resource)
    qrc = ET.tostring(RCC, pretty_print=True)
    qrc_file.write_bytes(qrc)


def buildQrc(src, dest, compression=3):
    callCommand(
        f"pyside2-rcc -o {Path(dest).resolve().as_posix()} -g python -compress {compression} {Path(src).resolve().as_posix()}"
    )


def buildApp(
    name,
    src,
    path="",
    icon="",
    onefile=True,
    clean=True,
    exclude_modules=[],
    hidden_imports=[],
    datas={},
    binaries={},
    dist="./dist",
    work="./build",
    use_upx=False,
):
    buildCommands = []
    if onefile:
        buildCommands.append("--onefile")
    if clean:
        buildCommands.append("--clean")
    if not use_upx:
        buildCommands.append(f"--noupx")
    if dist:
        buildCommands.append(f"--distpath {dist.format(**os.environ)}")
    if work:
        buildCommands.append(f"--workpath {work.format(**os.environ)}")
    if exclude_modules:
        for mod in exclude_modules:
            buildCommands.append(f"--exclude-module {mod}")
    if hidden_imports:
        for mod in hidden_imports:
            buildCommands.append(f"--hidden-import {mod}")
    if datas:
        for data in datas:
            buildCommands.append(f"--add-data {data.format(**os.environ)}")
    if binaries:
        for binary in binaries:
            buildCommands.append(f"--add-binary {binary.format(**os.environ)}")
    if path:
        buildCommands.append(f"-p {path.format(**os.environ)}")
    if icon:
        buildCommands.append(f"-i {icon.format(**os.environ)}")

    buildCommands.append(f"-n {name}")
    buildCommands.append(src.format(**os.environ))
    callCommand(" ".join(["python -O -m PyInstaller"]+buildCommands))


def processDict(input_dict):
    if hasattr(input_dict, "__iter__") and hasattr(input_dict, "items"):
        input_dict = {
            key.lower(): processDict(value) for key, value in input_dict.items()
        }
    return input_dict


# build classes
@dataclass
class BuildStep:
    buildsteps: list = field(default_factory=list)

    def addMulti(self, build_command, build_args=[], build_keywords={}, build_group=""):
        self.buildsteps = itertools.chain(
            self.buildsteps,
            (
                (
                    f"{build_group}: {build_command.__name__}:: {arg}, {build_keywords}".lstrip(),
                    partial(build_command, arg, **build_keywords),
                )
                for arg in build_args
            ),
        )

    def addSingle(
        self, build_command, build_args=[], build_keywords={}, build_group=""
    ):
        self.buildsteps = itertools.chain(
            self.buildsteps,
            [
                (
                    f"{build_group}: {build_command.__name__}:: {build_args}, {build_keywords}".lstrip(),
                    partial(build_command, *build_args, **build_keywords),
                )
            ],
        )

    def build(self):
        for buildstep in self.buildsteps:
            msg, buildresult = buildstep
            print(msg)
            try:
                buildresult()
            except Exception:
                raise


class Build:
    def __init__(self, config_filename="pyproject.yml"):
        # Get config
        self.config_file = Path(".") / config_filename
        if not self.config_file.exists():
            sys.exit("Could not find build config!")
        self.project_config = processDict(load(self.config_file.open(), Loader=Loader))

    def run(self, run_app=False, build_production=False):
        projectname = self.project_config.get("name")
        mainentrysrc = self.project_config.get("src")
        if not projectname or not mainentrysrc:
            logger.error(
                "Must Specify Project Name: 'Name' and Main Entry point: 'Src'"
            )
            sys.exit()
        qtresources = self.project_config.get("qtresources")
        prebuild_commands = self.project_config.get("precommands") or {}
        postbuild_commands = self.project_config.get("postcommands") or {}
        build_configs = self.project_config.get("build") or {}
        environments = self.project_config.get("environments") or {}
        run_cmds = self.project_config.get("runcommands","")
        buildsteps = BuildStep()
        # set environments variable
        os.environ["APPNAME"] = projectname
        for envname, value in environments.items():
            os.environ[envname] = str(Path(value.format(**os.environ)).resolve())
        # build qt Resources
        if qtresources:
            qrc = qtresources.get("src")
            py_qrc = qtresources.get("dest")
            qt_resources = qtresources.get("resources")

            if all([qrc, py_qrc, qt_resources]):
                buildsteps.addSingle(
                    writeQrc, build_args=[qt_resources, qrc], build_group="Build Qt RC"
                )
                buildsteps.addSingle(
                    buildQrc, build_args=[qrc, py_qrc], build_group="Build Qt RC"
                )

        # build distribution
        if build_production and build_configs:

            buildkws = dict(
                name=projectname,
                src=mainentrysrc,
                path=build_configs.get("path"),
                icon=build_configs.get("icon"),
                onefile=build_configs.get("onefile"),
                clean=build_configs.get("clean"),
                exclude_modules=build_configs.get("excludemodules"),
                hidden_imports=build_configs.get("hiddenimports"),
                datas=build_configs.get("datas"),
                binaries=build_configs.get("binaries"),
                dist=build_configs.get("dist"),
                work=build_configs.get("work"),
                use_upx=build_configs.get("upx"),
            )
            # run precommands
            for commands in prebuild_commands:
                buildsteps.addSingle(
                    callCommand, build_args=[commands], build_group="Build Distribution"
                )
            # run build
            buildsteps.addSingle(
                buildApp, build_keywords=buildkws, build_group="Build Distribution"
            )
            # run postcommands
            for commands in postbuild_commands:
                buildsteps.addSingle(
                    callCommand, build_args=[commands], build_group="Build Distribution"
                )
        if run_app:
            if build_production:
                buildsteps.addSingle(
                    callCommand,
                    [
                        str(Path("{distpath}/{appname}/{appname}.exe").resolve()).format(
                            appname=projectname,
                            distpath=build_configs.get("dist", "dist"),
                        )
                    ],
                    build_group="Run Distribution",
                )
            else:
                buildsteps.addSingle(
                    callCommand,
                    [" ".join([f"python {Path(mainentrysrc).resolve().as_posix()}", run_cmds])],
                    build_group="Run Live",
                )

        # Build
        buildsteps.build()

    def _run(self):
        pass

    @classmethod
    def run_build(cls, config_filename="pyproject.yml"):
        logger.debug(config_filename)
        cls(config_filename).run()


if __name__ == "__main__":
    from fire import Fire

    Fire(Build)
