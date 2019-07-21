# GeoJSON Properties Editor Assistant
This is a tool to assist in editing the properties of a GeoJSON formatted file. At the moment it supports only *collection of Features* GeoJSON object as defined in [RCF7946](https://tools.ietf.org/html/rfc7946#section-2). The tool will convert the **properties** of the each feature in the collection to CSV format and output them to a file. After editing the properties with your CSV editor, the tool will create the GeoJSON file with the edited properties.


## Usage
There are two steps involved, *split* and *join*. Split is the first part of the process which splits the GeoJSON file to two separate files, *properties* and *features*. Essentially it **converts the properties to a CSV file** which can then be processed with your tool of choice. The *features* is a JSON file which will be used in the *join* process to reconstruct the GeoJSON file.

### Split
To split a GeoJSON file run:

```
python3 [FILE] --split
```

This will generate 2 files, **gjpe_properties.csv** and **gjpe_features.json**.

> Note that you can change the prefix of the output files (the **gjpe** part, using `--prefix PREFIX`).

### Editing the CSV
Open and edit the **properties.csv** file. Rows can be removed which will cause the corresponding feature not to be included the the final GeoJSON file. New properties can be added by adding new columns. It is important not to edit the

### Join
To join the **gjpe_properties.csv** and **gjpe_features.json** files run:

```
python3 [FILE] --join
```

This will generate a single file **gjpe_final.geojson** which will contain the resulting GeoJSON collection of features.

> Use the `--prefix PREFIX`` to change the prefix of the file.

The **gjpe_properties.csv** and **gjpe_features.json** files will be deleted. To keep the files you can pass the `--keep` argument.

## Notes
There are several features that can improve both the functionality and usability of this tool. I will list them here, for future reference.

- Improve the structure of the project
- Make the errors verbose
- Output a result status at the end (e.g. "... features joined, ... features removed")
- Introduce an argument which will act as an edit hook. It will call the editor of choice to edit the CSV. This will enable the tool be called just once; it will split, call the CSV editor and then join the file

Any contributions are of course welcome!

### Author
Demetris Stavrou

