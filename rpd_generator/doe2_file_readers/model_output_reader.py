import ctypes
import os
from pathlib import Path


# noinspection PyTypeChecker
class MRTArray(ctypes.Structure):
    _fields_ = [
        ("entry_id", ctypes.c_int),
        ("return_value", ctypes.c_int),
        ("psz_report_key", ctypes.c_char * 40),
        ("psz_row_key", ctypes.c_char * 40),
    ]


NHR_DICT = None


def read_nhr_list(file_path):
    nhr_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip(" ;").split(",")
            if len(parts) >= 7:
                entry_id, _, _, _, _, _, max_values = parts[:7]
                nhr_dict[int(entry_id)] = int(max_values)
    return nhr_dict


def get_nhr_dict(nhr_list_path):
    global NHR_DICT
    if NHR_DICT is None:
        NHR_DICT = read_nhr_list(nhr_list_path)
    return NHR_DICT


"""

Get Multiple Result
-------------------
Arguments
---------
pszDOE2Dir: path to DOE-2 directory
pszFileName: path to project (do not include any extension)
iFileType: 0 for Loads results, 1 for HVAC, 2 for Utility Rate; in general first digit of NHRlist ID minus 1
pfData: sample array to store the retrieved values
iMaxValues: number of items to retrieve (NI in NHRList.txt); should always be 1 when GetSingleResult is called
iNumMRTs: Number of MultResultsType structures pointed to by the following argument. Only the first 12 will be used, 
          each one must retrieve results from the same file and the number of items retrieved for each element should be equal.
pMRTs: Pointer to an array of MultResultsType structures:
       struct MultResultsType
        {
           int  iEntryID;      // from NHRList.txt
           int  iReturnValue;  // success/failure
           char pszReportKey[ 40 ];
           char pszRowKey[    40 ];
        };
"""


# noinspection PyTypeChecker, PyCallingNonCallable
def get_multiple_results(
    d2_result_dll: str, doe2_data_dir: str, project_fname: str, request_array: list
) -> list:
    """
    Get Multiple Results from the simulation output files
    :param d2_result_dll: (string) path to user's eQUEST D2Result.dll file included with installation files
    :param doe2_data_dir: (string) path to the data directory of the appropriate version of DOE-2 (e.g. DOE-2.2 or DOE-2.3)
    :param project_fname: (string) path to project with project name NOT INCLUDING FILE EXTENSION
    :param request_array: (list) list of entry_id: (int) from NHRList.txt corresponding to the value to retrieve,
    report_key: (string) to use when RI > 0 and when value to retrieve refers to a particular BDL component,
    and row_key: (string) to use when KT > 0 and when a report has multiple row where each row provides results for a separate building component or month of the year
    :return: list of returned values from the binary simulation output files
    """
    d2_result_dll = ctypes.CDLL(d2_result_dll)
    multiple_result_dll = d2_result_dll.D2R_GetMultipleResult
    nhr_list_path = str(Path(doe2_data_dir) / "DOE23" / "NHRList.txt")
    nhr_dict = get_nhr_dict(nhr_list_path)
    doe2_data_dir = str(Path(doe2_data_dir) / "DOE23") + "\\"

    num_mrts = len(request_array)
    mrt_array = (MRTArray * num_mrts)()
    if len(request_array) > 0:
        file_type = int(str(request_array[0][0])[0]) - 1
    else:
        return []

    max_values: int = 0
    for i, value_request in enumerate(request_array):
        entry_id, report_key, row_key = value_request

        mrt_array[i].entry_id = entry_id
        mrt_array[i].psz_report_key = report_key.encode("utf-8")
        mrt_array[i].psz_row_key = row_key.encode("utf-8")

        if entry_id in nhr_dict:
            max_values += nhr_dict[entry_id]

    pf_data = (ctypes.c_float * max_values)()

    multiple_result_dll(
        ctypes.c_char_p(doe2_data_dir.encode("utf-8")),
        ctypes.c_char_p(project_fname.encode("utf-8")),
        ctypes.c_int(file_type),
        pf_data,
        ctypes.c_int(max_values),
        ctypes.c_int(num_mrts),
        mrt_array,
    )

    return [data for data in pf_data]


# noinspection PyTypeChecker,PyCallingNonCallable
def get_string_result(
    d2_result_dll: str,
    doe2_dir: str,
    project_fname: str,
    entry_id: int,
    report_key: str = "",
    row_key: str = "",
) -> str:
    """
    Get single result from the simulation output files expected to be a string
    ------------------
    Arguments
    ---------
    :param d2_result_dll: (string) path to user's eQUEST D2Result.dll file included with installation files
    :param doe2_dir: (string) path to DOE-2 directory
    :param project_fname: (string) path to project with project name NOT INCLUDING FILE EXTENSION
    :param entry_id: (int) id from NHRList.txt corresponding to the value to retrieve
    :param report_key: (string) to use when RI > 0 and when value to retrieve refers to a particular BDL component
    :param row_key: (string) to use when KT > 0 and when a report has multiple row where each row provides results for a separate building component or month of the year

    :return: value from binary simulation output files
    """

    if not os.path.exists(d2_result_dll):
        raise FileNotFoundError(f"D2Result.dll not found at {d2_result_dll}")

    # Load DLL
    d2_result_dll = ctypes.CDLL(d2_result_dll)
    doe2_dir = str(Path(doe2_dir) / "DOE23") + "\\"

    single_result_dll = d2_result_dll.D2R_GetSingleResult
    single_result_dll.argtypes = [
        ctypes.c_char_p,  # pszDOE2Dir
        ctypes.c_char_p,  # pszFileName
        ctypes.c_int,  # iEntryID
        ctypes.POINTER(ctypes.c_char),  # pfData
        ctypes.c_int,  # iMaxValues
        ctypes.c_char * 40,  # pszReportKey
        ctypes.c_char * 40,  # pszRowKey
    ]
    single_result_dll.restype = ctypes.c_long

    pf_data = ctypes.create_string_buffer(256)
    report_key_arr = (ctypes.c_char * 40)(*report_key.encode("utf-8"))
    row_key_arr = (ctypes.c_char * 40)(*row_key.encode("utf-8"))

    # Call the function
    single_result_dll(
        doe2_dir.encode("utf-8"),
        project_fname.encode("utf-8"),
        entry_id,
        pf_data,
        1,
        report_key_arr,
        row_key_arr,
    )

    # Return the string from the buffer
    return pf_data.value.decode("utf-8").strip()
