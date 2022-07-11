import pathlib
from typing import Literal

import numpy as np
import pandas as pd


class ReadFile:
    def __init__(self) -> None:
        self._storedFiles = {".xlsx": {}, ".csv": {}}

    # unfinished
    def setStoredData(
        self,
        data: pd.DataFrame | list[pd.DataFrame],
        fileType=".xlsx",
        filePath: str = "",
        index: int = -1,
    ) -> bool:
        fileData = self.getStoredData(fileType=fileType, filePath=filePath)
        if fileData:
            if index >= 0 and index < len(fileData):
                fileData[index] = data
            else:
                fileData = data
            # self._storedFiles
            return True
        return False

    def getStoredFiles(self, fileType: str = None) -> dict[str, dict[str, pd.DataFrame | None]]:
        storedFiles = self._storedFiles
        if fileType in storedFiles:
            return storedFiles[fileType]
        return storedFiles

    def getStoredData(
        self, fileType: str = "", filePath: str = "", index: int = -1
    ) -> pd.DataFrame | dict[str, pd.DataFrame | None] | Literal[False] | None:
        fileInfo = self.getStoredFiles()
        match (fileType.lower()):  # match schneller als if
            case ".xlsx":
                fileInfo = fileInfo[".xlsx"]
            case ".csv":
                fileInfo = fileInfo[".csv"]
            case _:
                if (
                    fileType in fileInfo
                ):  # gleiche funktionalität (match), allerdings weniger schnell
                    fileInfo = fileInfo[fileType]
        if filePath in fileInfo:
            fileInfo = fileInfo[filePath]
            if index > 0 and index < len(fileInfo):
                fileInfo = fileInfo[index]
            return fileInfo
        return False

    def addFileToList(self, path: str = "", data: pd.DataFrame = pd.DataFrame) -> bool:
        fileType = pathlib.Path(path).suffix
        files = self.getStoredFiles()
        if fileType in files:
            files[fileType][path] = data
            self.setStoredData(fileType=fileType, filePath=path, data=data)
            return True
        print("Datentyp nicht vorhanden")
        return False

    def getDataByIndex(self, fileIndex: int | str, **options):
        files = self.getStoredFiles()
        fileIndex = self.getNameByIndex(fileIndex, files)
        if files is not []:
            return self.getDataByPath(files[fileIndex], options)

    # options: xlsx = sheet | csv = header, names
    @classmethod
    def getDataByPath(cls, path: str, **options) -> object:
        method = cls.getExtractMethod(path=path)
        if method is not None:
            return method(path, options)
        return None

    @classmethod
    def getExtractMethod(cls, fileType: str = "", path: str = ""):  # path: str, fileType: str):
        method = None
        if path != "":
            fileType = cls.getPathSuffix(path)
        match (fileType):
            case ".xlsx" | ".xls":
                method = cls.extractExcel
            case ".csv":
                method = cls.extractCsv
            case _:
                print(f"fileType ({fileType}) unknown")
        return method

    @staticmethod
    def getPathSuffix(path: str) -> str:
        try:
            return pathlib.Path(path).suffix
        except Exception:
            return ""

    @staticmethod
    def getIndexNameByIndex(index: int | str, haystack: dict) -> str:
        if index in haystack:
            return index
        for idx, strIdx in haystack:
            if idx == index:
                return strIdx
        print(f"Index ({index}) wurde nicht gefunden")
        return f"{index}"

    @staticmethod
    def extractExcel(path: str, sheet: str | list[int | str]):
        fileData = pd.DataFrame()  # create empty dataframe
        try:
            fileData = pd.read_excel(
                pd.ExcelFile(path),
                sheet_name=[sheet[0]],
                dtype={"Name": str, "pkt": int},
            )
        except Exception:
            print("Falscher Pfad oder sheet Name!")
        else:
            print("Excel Erfolgreich eingelesen.")
        return fileData

    @staticmethod
    def extractCsv(path: str, header: int | list[int] = None, names: str | list[str] = None):
        fileData = pd.DataFrame()  # create empty dataframe
        try:
            fileData = pd.read_csv(
                pd.ExcelFile(path),
                header=header,
                names=names,
                dtype={"Name": str, "pkt": int},
            )
        except Exception:
            print("Falscher Pfad oder sheet Name!")
        else:
            print("Excel Erfolgreich eingelesen.")
        return fileData

    def __str__(self) -> str:
        s = ""
        files = self.getStoredFiles()
        for fileType in files:
            for idx, path in enumerate(files[fileType]):
                s += f"{idx}: {files[fileType][path]}"
        return s
