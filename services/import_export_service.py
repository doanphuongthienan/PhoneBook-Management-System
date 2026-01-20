class ImportExportService:

    def import_contacts(self, file_path) -> bool:
        if self.duplicate_check():
            pass

    def duplicate_check(self) -> bool:
        pass

    def export_contacts(self, file_path, format_type) -> bool:
        pass
