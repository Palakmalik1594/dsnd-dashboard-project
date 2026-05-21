# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies needed for sql execution
from .sql_execution import query


# Define Employee subclass
class Employee(QueryBase):

    # class attribute
    name = "employee"

    # Return all employee names + ids
    @query
    def names(self):

        return """
        SELECT 
            first_name || ' ' || last_name AS full_name,
            employee_id
        FROM employee
        """

    # Return single employee name
    @query
    def username(self, id):

        return f"""
        SELECT
            first_name || ' ' || last_name AS full_name
        FROM employee
        WHERE employee_id = {id}
        """

    # Return dataframe for ML model
    def model_data(self, id):

        if id is None:
            id = 1

        query_string = f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """

        return self.pandas_query(query_string)