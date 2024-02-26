class SalaryService:
    """
    Service class for handling operations related to Salary entities.

    Methods:
    - __init__(self, repository): Constructor to initialize the service with a specified repository.
    - return_min_max_salary(self): Return the minimum and maximum salary from the repository.

    Attributes:
    - _repository: The repository used for CRUD operations on Salary entities.
    """

    def __init__(self, repository):
        """
        Constructor to initialize the service with a specified repository.

        Parameters:
        - repository: The repository for CRUD operations on Salary entities.
        """
        self._repository = repository

    def return_min_max_salary(self):
        """
        Return the minimum and maximum salary from the repository.

        Returns:
        - Dictionary containing "min" and "max" keys with corresponding salary values.
        """
        salaries = self._repository.get_all()

        min_salary = min(salary.salary_from for salary in salaries)
        max_salary = max(salary.salary_to for salary in salaries)

        return {
            "min": min_salary,
            "max": max_salary
        }
