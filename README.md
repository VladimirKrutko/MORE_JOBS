# MORE_JOBS

### Project structure

```bash
├── airflow_module -> code to load data into db using apache airflow \n
│   ├── dags -> dags definition
│   └── dags_code -> dag task realization
├── scripting 
│   ├── loader -> code for working with db
│   │   ├── models -> This folder contains models for working with db
│   ├── shop_modules -> contain code for site parsing and crawling for specific shops
│   ├── site_configurations -> contains json files with shop configuration
│   └── sys -> system script to run project
```
### Shop script description:

sys directory:<br>
* **aws_variables.py** - contains variables for working with aws services<br>
* **init_aws_services.py** - initialize aws services for specific shop<br>
* **send_first_url_to_crawling.py** - send start shop url into crawler queue to start shop crawling
* **site_data.py** - contains class that specify shop specification
* **start_placement_loading.py** - script to start process parsed data from placement pages
* **start_site_crawler.py** - start crawler for shop (page and placement modules)
* **sys_functions.py** - script contains 'helper' function
<br>
<br>





