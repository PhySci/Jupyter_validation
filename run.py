import papermill as pm
import os
import json


def main(inp_folder, out_folder, rep_file):
    report = list()

    file_list = get_file_paths(input_folder)
    for file in file_list:
        input_pth = os.path.join(inp_folder, file)
        output_pth = os.path.join(out_folder, file)
        msg = execute_notebook(input_pth, output_pth)
        msg.update({"File name": file})
        report.append(msg)

    save_report(report, rep_file)


def execute_notebook(input_file, output_file):
    msg = {"Status": "Success"}
    try:
        pm.execute_notebook(input_file, output_file)
    except pm.exceptions.PapermillExecutionError as err:
        msg = {"Status": "Error",
               "Error type": err.ename,
               "Cell number": err.cell_index,
               "Error message": err.evalue}
    return msg


def get_file_paths(input_dir: str) -> list:
    files = os.listdir(input_dir)
    return [f for f in files if f.endswith(".ipynb")]


def save_report(data: list, output_file: str):
    with open(output_file, "w") as fid:
        json.dump(data, fid)


if __name__ == "__main__":

    input_folder = os.path.join(os.path.dirname(__file__), "input")
    output_folder = os.path.join(os.path.dirname(__file__), "output")
    report_file = "report.json"
    main(input_folder, output_folder, report_file)
