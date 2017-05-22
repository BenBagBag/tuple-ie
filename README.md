# Mkdocs quickstart guide 
This guide and project skeleton are meant to provide a quick intro to mkdocs and the use of the AI2 mkdocs theme. 
For more detail, refer to [the official mkdocs documentation.](http://www.mkdocs.org)
## Installation
Mkdocs is pip-installable:
```python
pip install mkdocs
```
## Configuration 
Mkdocs uses a single yaml file to configure the static site it builds from a set of user-supplied markdown files. Things like 
the site name, theme, and other properties are set there. Additionally, every page included in the build is 
declared here, with the markdown file used to generate it named.  
Here is a simple example config file:

```yaml
site_name: Generic Data explorer  # The site name will appear prominently on a site's homepage, and should reflect the dataset. 
theme: null  # If using a locally defined theme this will be set to null (or left out). The theme name if using a stock theme
theme_dir: './material_ai2_mkdoc'  # Path to the theme directory being used.
repo_url: 'https://github.com/allenai/<your repo>'   # Link to project repo, if applicable.
repo_name: '<Your Repo Name>'  # The repo name that'll be displayed.
download_url: '<Your Download URL>'  # Download link to the dataset.
extra:  # Extra parameters used by a theme.
  font:  # Custom font setting.
    text: Oxygen
    code: Oxygen

pages:   # Define site structure without hierarchy
    - home: index.md  # Home page
    # The pages below will be specific to a dataset
    # these are defined as  <page name to display>: <markdown file in the the docs directory the page will be generated from. 
    - dataset structure: structure.md  # Ideally a description of the formatting of the dataset should be provided   
    - datapoint 1 : datapoint_1.md  # A page for single portion of the dataset (the size/level of detail will depend on the dataset) 
```
For larger, complex datasets, a single level of hierarchy can be used when declaring the site structure:
```yaml
pages:   # Define site structure with hierarchy
    - home: index.md  # Home page
    - dataset structure: structure.md  # Ideally a description of the formatting of the dataset should be provided
    - category 1: 
        - datapoint 1 : datapoint_1.md  # A page for single portion of the dataset (the size/level of detail will depend on the dataset)
        - datapoint 2 : datapoint_2.md
    - category 2: 
        - datapoint 3 : datapoint_3.md  # A page for single portion of the dataset (the size/level of detail will depend on the dataset)
        - datapoint 4 : datapoint_4.md
```
This will nest single data-pages under the categories specified in a collapsible navigation menu.

## AI2 Theme
The AI2 theme is packaged with this example, and it can be set as shown in the config file above. If any modifications are needed 
to mkdoc's behaviour, it's best to implement these at the theme level if possible. As an example, if a dataset is too large
for the standard search to function effectively, it can be replaced in the theme.

## Adding documents
Mkdocs builds individual pages from markdown files present in the docs directory. How these pages are generated will 
depend on the details of the dataset being documented. Pages describing the dataset as a whole are best written by hand.
Mkdocs uses standard markdown syntax to specify headers, image links, external links, and for some limited html styling.
For larger datasets, it's best to generate most markdown from the dataset in some programmatic way.

## Build
Building the site is done by:
```bash
mkdocs build
```

## Local Development
Work in progress can be previewed locally by running:
```bash
mkdocs serve 
```
This will launch a local server and buid/rebuild the site when any changes are detected to the project files.

## Deploy
After building, the site can be deployed to AWS by... TODO

## Setting DNS redirect
TODO...
