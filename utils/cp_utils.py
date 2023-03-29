"""
This collection of functions runs CellProfiler and will rename the .sqlite outputted to any specified name if running an analysis pipeline.
"""

import os
import pathlib


def rename_sqlite_file(sqlite_dir_path: pathlib.Path, name: str, hardcode_sqlite_name: str):
    """Rename the .sqlite file to be {method}.sqlite as to differentiate between the files

    Args:
        sqlite_dir_path (pathlib.Path): path to CellProfiler_output directory
        name (str): new name for the SQLite file
        hardcode_sqlite_name (str): hardcoded name of the returned SQLite file from CellProfiler to change
    """
    try:
        # CellProfiler requires a name to be set in to pipeline, so regardless of plate or method, all sqlite files name are hardcoded
        sqlite_file_path = pathlib.Path(f"{sqlite_dir_path}/{hardcode_sqlite_name}.sqlite")

        new_file_name = str(sqlite_file_path).replace(
            sqlite_file_path.name, f"{name}.sqlite"
        )

        # change the file name in the directory
        pathlib.Path(sqlite_file_path).rename(pathlib.Path(new_file_name))
        print(f"The file is renamed to {pathlib.Path(new_file_name).name}!")

    except FileNotFoundError as e:
        print(
            f"The {hardcode_sqlite_name}.sqlite file is not found in directory. Either the pipeline wasn't ran properly or the file is already renamed.\n"
            f"{e}"
        )


def run_cellprofiler(
    path_to_pipeline: str,
    path_to_output: str,
    path_to_loaddata: str,
    sqlite_name: str = None,
    hardcode_sqlite_name: str = None, 
    analysis_run: bool = False,
):
    """Run CellProfiler on data using LoadData CSV. It can be used for both a illumination correction pipeline and analysis pipeline.

    Args:
        path_to_pipeline (str): path to the CellProfiler .cppipe file with the segmentation and feature measurement modules
        path_to_output (str): path to the output folder
        path_to_loaddata (str): path to the LoadData CSV to load in the images and IC functions
        sqlite_name (str, optional): string with name for SQLite file for an analysis pipeline (default is None)
        analysis_run (bool, optional): will use functions to complete an analysis pipeline (default is False)
    """
    # run CellProfiler on a plate that has not been analyzed yet
    command = f"cellprofiler -c -r -p {path_to_pipeline} -o {path_to_output} --data-file {path_to_loaddata}"
    os.system(command)

    if analysis_run:
        # runs through any files that are in the output path
        if any(
            files.name.startswith(sqlite_name)
            for files in pathlib.Path(path_to_output).iterdir()
        ):
            raise NameError(f'The file {sqlite_name}.sqlite has already been renamed! This means it was probably already analyzed.')

        # run CellProfiler on a plate that has not been analyzed yet
        command = f"cellprofiler -c -r -p {path_to_pipeline} -o {path_to_output} --data-file {path_to_loaddata}"
        os.system(command)

        # rename the outputted .sqlite file to the
        rename_sqlite_file(sqlite_dir_path=pathlib.Path(path_to_output), name=sqlite_name, hardcode_sqlite_name=hardcode_sqlite_name)