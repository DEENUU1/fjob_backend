class ReportService:
    def __init__(self, repository):
        self._repository = repository

    def create(self, data):
        return self._repository.create(data)
