import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake(name):
    """
    Convert camel case to snake case
    """
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

@transformer
def transform(data, *args, **kwargs):
    # Remove rows where passenger_count or trip_distance is equal to 0
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    print(f'Preprocessing: rows with zero passengers: {data["passenger_count"].isin([0]).sum()}')
    print(f'Preprocessing: rows with zero distance: {data["trip_distance"].between(0, 1e-6).sum()}')

    # Create a new column "lpep_pickup_date" by converting "lpep_pickup_datetime" to date
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    print("Original Column Names:", data.columns)

    # Rename columns from camel case to snake case
    data.columns = [camel_to_snake(col) for col in data.columns]

    print("Modified Column Names:", data.columns)

    print(data["vendor_id"].value_counts().index.unique().tolist())

    return data


@test
def test_output(output, *args):
    #Assert that passenger_count > 0
    assert output["passenger_count"].isin([0]).sum() == 0, 'There are rides with zero passengers'
    
    #Assert that trip_distance > 0
    assert output["trip_distance"].between(0, 1e-6).sum() == 0, 'There are rides with zero trip distance'
    
    # Assert that the "vendor_id" column is present
    assert "vendor_id" in output.columns, 'The "vendor_id" column is missing'

    # Assert that all values in the "vendor_id" column are among the existing values
    assert all(output["vendor_id"].isin(output["vendor_id"].unique())), 'Not all values in "vendor_id" are among the existing values'