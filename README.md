# Python DL Tools
Useful tools to work with DL problems in python. 

### `Pipeline`
Create a pipeline for preprocessing and/or augmentation.
- Use the decorator `@register_in_pipeline` to include a function in pipeline
- Use the `Pipeline` class to create a pipeline

```python
from pipeline import register_in_pipeline # decorator to make available a function to use with Pipeline class
from pipeline import Pipeline

# Step1: register functions to use with the Pipeline class
@register_in_pipeline
def func1(x, arg1, kwarg1=0, kwargs2=1):
  # Do something with 'x'
  return x

@register_in_pipeline
def func2(x, arg1, arg2, kwarg3=-1):
  # Do something with 'x'
  return x

# Step2: instantiate the Pipeline class
pl = Pipeline()
pl.FUNCTIONS_PIPELINE # contains 'func1' and 'func2' as callables

pl = Pipeline( pipeline = [
                           ("func1", 1, {kwarg1 = 0, kwarg2 = 1, kwarg3 = -1}),       # First call
                           ("func2", 1, 2, {kwarg1 = 0, kwarg2 = 1, kwarg3 = -1})     # Second call
                          ]
```

### `MonitorValues`

```python
from monitor_values import MonitorValues

# Instantiate MonitorValues with the desired variables to monitor as strings in a list or tuple
mv = MonitorValues(['x','y','z'])

for x,y,z in zip(range(3),range(4),range(5)): 
  # Call the class to monitor the values
  mv()
  
# Results
mv.get_values() # List with namedtuples of all monitored values
mv.get_values_asdf() # Same before as Pandas DataFrame
mv.to_excel("path/to/save.xlsx") # Save as excel
mv.to_csv("path/to/save.csv") # Save as csv
```

### `DataSelector`
Get train, val and test sets. 
- Balanced on some variable 
- Exlusive on some variable

```python
from data_selector import DataSelector

# Initialize data selector with labels
ds = DataSelector(id_labels = range(100), labels = [0]*50 + [1]*50)

# Generate train, test, val sets
ds(train_size = 0.8) #  -> test_size = val_size = 0.1
# > Generating train, validation and test sets...
# > Datasets successfully generated. See 'datasets' attribute.
# > {'train': {1: 41, 0: 39}, 'val': {0: 5, 1: 5}, 'test': {0: 6, 1: 4}}

# See results
ds.datasets
```
