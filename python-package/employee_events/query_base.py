# Import dependencies
from .sql_execution import QueryMixin


# Define QueryBase class
class QueryBase(QueryMixin):

    # class attribute
    name = ""

    # Return names
    def names(self):

        return []

    # Event counts dataframe
    def event_counts(self, id):

        if id is None:
            id = 1

        query = f"""
        SELECT 
            event_date,
            SUM(positive_events) as positive_events,
            SUM(negative_events) as negative_events
        FROM employee_events
        WHERE {self.name}_id = {id}
        GROUP BY event_date
        ORDER BY event_date
        """

        return self.pandas_query(query)

    # Notes dataframe
    def notes(self, id):

        if id is None:
            id = 1

        query = f"""
        SELECT 
            note_date,
            note
        FROM notes
        WHERE {self.name}_id = {id}
        ORDER BY note_date
        """

        return self.pandas_query(query)