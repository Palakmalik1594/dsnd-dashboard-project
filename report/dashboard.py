from fasthtml.common import *
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import QueryBase, Employee, Team

# import the load_model function from the utils.py file
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):

    # Overwrite the build_component method
    def build_component(self, entity_id, model):

        # Set label attribute
        self.label = model.name.title()

        # Return parent output
        return super().build_component(entity_id, model)

    # Overwrite component_data method
    def component_data(self, entity_id, model):

        return model.names()


# Create a subclass of base_components/BaseComponent
# called `Header`
class Header(BaseComponent):

    # Overwrite build_component method
    def build_component(self, entity_id, model):

        return H1(f"{model.name.title()} Performance Dashboard")


# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):

    # Overwrite visualization method
    def visualization(self, asset_id, model):

        # Get event count data
        data = model.event_counts(asset_id)

        # Fill nulls
        data = data.fillna(0)

        # Set index
        data = data.set_index('event_date')

        # Sort index
        data = data.sort_index()

        # Convert to cumulative counts
        data = data.cumsum()

        # Rename columns
        data.columns = ['Positive', 'Negative']

        # Create subplot
        fig, ax = plt.subplots(figsize=(8, 5))

        # Plot data
        data.plot(ax=ax)

        # Styling
        self.set_axis_styling(
            ax,
            bordercolor='black',
            fontcolor='black'
        )

        # Labels and title
        ax.set_title('Employee Events')
        ax.set_xlabel('Date')
        ax.set_ylabel('Count')

        return fig


# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
class BarChart(MatplotlibViz):

    # Predictor class attribute
    predictor = load_model()

    # Overwrite visualization method
    def visualization(self, asset_id, model):

        # Get model input data
        data = model.model_data(asset_id)

        # Predict probabilities
        predictions = self.predictor.predict_proba(data)

        # Get second column
        predictions = predictions[:, 1]

        # Team average or employee prediction
        if model.name == "team":

            pred = predictions.mean()

        else:

            pred = predictions[0]

        # Create subplot
        fig, ax = plt.subplots(figsize=(8, 2))

        # Bar chart
        ax.barh([''], [pred])

        ax.set_xlim(0, 1)

        ax.set_title(
            'Predicted Recruitment Risk',
            fontsize=20
        )

        # Styling
        self.set_axis_styling(
            ax,
            bordercolor='black',
            fontcolor='black'
        )

        return fig


# Create a subclass of CombinedComponent
# called Visualizations
class Visualizations(CombinedComponent):

    children = [
        LineChart(),
        BarChart()
    ]

    outer_div_type = Div(cls='grid')


# Create a subclass of DataTable
# called NotesTable
class NotesTable(DataTable):

    # Overwrite component_data method
    def component_data(self, entity_id, model):

        return model.notes(entity_id)


class DashboardFilters(FormGroup):

    id = "top-filters"

    action = "/update_data"

    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),

        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]


# Create Report subclass
class Report(CombinedComponent):

    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]


# Initialize FastHTML app
app = FastHTML()

# Initialize report
report = Report()


# Root route
@app.get("/")
def home():

    return report(1, Employee())


# Employee route
@app.get("/employee/{id:str}")
def employee_dashboard(id):

    return report(id, Employee())


# Team route
@app.get("/team/{id:str}")
def team_dashboard(id):

    return report(id, Team())


# Keep below unchanged
@app.get('/update_dropdown{r}')
def update_dropdown(r):

    dropdown = DashboardFilters.children[1]

    print('PARAM', r.query_params['profile_type'])

    if r.query_params['profile_type'] == 'Team':

        return dropdown(None, Team())

    elif r.query_params['profile_type'] == 'Employee':

        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):

    from fasthtml.common import RedirectResponse

    data = await r.form()

    profile_type = data._dict['profile_type']

    id = data._dict['user-selection']

    if profile_type == 'Employee':

        return RedirectResponse(
            f"/employee/{id}",
            status_code=303
        )

    elif profile_type == 'Team':

        return RedirectResponse(
            f"/team/{id}",
            status_code=303
        )


serve()