from fileReader import ReadFile


class Program:
    def __init__(self) -> None:
        self.reader = ReadFile()
        self.ranking = None

    def run(self) -> bool:
        self.reader.addFileToList(
            r"C:\Users\etienne\Desktop\VorbereitungsWoche\Projekte\data\testData.xlsx"
        )
        print(self.reader)
        self.reader.getDataByPath(
            r"C:\Users\etienne\Desktop\VorbereitungsWoche\Projekte\data\testData.xlsx",
            sheet=["Tabelle1"],
        )
        print(self.reader)


excelReadProg = Program()
excelReadProg.run()
