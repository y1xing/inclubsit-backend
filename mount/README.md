# CodeGen for dummy data
This allows us to quickly initialise data to the tables.

# Requirements
- MySQL
- A `ClubsData - ClubsInfo.csv` file exported from Google Sheets.
> [!NOTE]
> If using a Docker container for MySQL, mount this directory into the container to access the `initialise.sql` script.

# Usage
## SQL Generation
```bash
python codegen.py
```
This outputs a `output.txt` file which contains the data for insertion. 

## SQL script
```sql
source <path_to_initalise.sql>
```