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
def func1(x, arg, kwarg1=0, kwargs2=1):
  # Do something with 'x'
  return x

@register_in_pipeline
def func2(x, arg1, arg2, kwarg=-1):
  # Do something with 'x'
  return x

# Step2: instantiate the Pipeline class
pl = Pipeline()
pl.FUNCTIONS_PIPELINE # contains 'func1' and 'func2' as callables

pl = Pipeline( pipeline = [
                           ("func1", 1, {kwarg1 = 0, kwarg2 = 1}),       # First call
                           ("func2", 1, 2, {kwarg = -1})                 # Second call
                          ]
                          
# Step3: Apply pipeline
new_x = pl(x)
```

Useful features: save and load pipeline from JSON
```python
# Save pipeline
pl.asJSON("path/to/my/pipeline.json")

# Load pipeline
pl.fromJSON("path/to/my/pipeline.json")
```

### `MonitorValues`
Useful to create a table in an easy way. 

```python
from itertools import zip_longest
from monitor_values import MonitorValues

# Instantiate MonitorValues with the desired variables to monitor as strings in a list or tuple
mv = MonitorValues(['x','y','z'])

# What happens if variables to be monitored does not exists yet? 'None' will be assing
mv()

for x,y,z in zip_longest(range(3),range(4),range(5)): 
  # Call the instance class to monitor the values
  mv()
  
# Results
mv.get_values() # List with namedtuples of all monitored values
mv.get_values_asdf() # Same before as Pandas DataFrame

#                  timestamp    x    y  z
#0  Mon Nov 16 13:37:32 2020  NaN  NaN  NaN    # 'NaN' -> 'None' in mv.get_values()
#1  Mon Nov 16 13:37:32 2020  0.0  0.0  0
#2  Mon Nov 16 13:37:32 2020  1.0  1.0  1
#3  Mon Nov 16 13:37:32 2020  2.0  2.0  2
#4  Mon Nov 16 13:37:32 2020  NaN  3.0  3
#5  Mon Nov 16 13:37:32 2020  NaN  NaN  4 

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

# 1. Generate train, test, val sets
ds(train_size = 0.8) #  -> test_size = val_size = 0.1
# > Generating train, validation and test sets...
# > Datasets successfully generated. See 'datasets' attribute.
# > {'train': {1: 41, 0: 39}, 'val': {0: 5, 1: 5}, 'test': {0: 6, 1: 4}}

# See results
ds.datasets

# 2. Generate train, val, test sets balanced_on some variable
sex = ["M"]*20 + ["F"]*80
ds(train_size = 0.8,  balanced_on = sex)
# > Generating train, validation and test sets...
# > Datasets successfully generated. See 'datasets' attribute.
# > {'train': {1: 40, 0: 40}, 'val': {0: 4, 1: 6}, 'test': {0: 6, 1: 4}}

# Distribution of variable 'sex' in datasets generated
ds._get_summary_var(sex)
# > {'train': {'F': 64, 'M': 16}, 'val': {'F': 8, 'M': 2}, 'test': {'F': 8, 'M': 2}}
```

Extra (in progress)
```python
# 2. Generate train, val, test sets exclusive_on some variable
ds(train_size = 0.8, exclusive_on = sex)
```
`exclusive_on` should be use with variables like ID. Example, Patient-ID, RUT, DNI, or something that you consider that cannot belong to more than one set.
