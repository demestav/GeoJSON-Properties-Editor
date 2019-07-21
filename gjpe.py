import argparse
import copy
import csv
import json
import pathlib

# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("geojson_file", help="The GeoJSON file")
parser.add_argument(
    "--prefix", help="Set the file prefix", nargs=1, type=str, default="gjpe"
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-s", "--split", help="Just split the file", action="store_true")
group.add_argument("-j", "--join", help="Just join the files", action="store_true")
parser.add_argument(
    "-k",
    "--keep",
    help="Do not delete project files after joining (option ignored for split",
    action="store_true",
)
args = parser.parse_args()

# Setup file paths and remove possible parents in path
file_prefix = args.prefix
prop_fname_only = pathlib.Path(f"{file_prefix}_properties.csv").name
feat_fname_only = pathlib.Path(f"{file_prefix}_features.csv").name
final_fname_only = pathlib.Path(f"{file_prefix}_final.csv").name

prop_path = pathlib.Path(prop_fname_only)
feat_path = pathlib.Path(feat_fname_only)
final_path = pathlib.Path(final_fname_only)

# Read the GeoJSON file into memory
orig_file_path = pathlib.Path(args.geojson_file)
try:
    with open(orig_file_path, "r") as f:
        raw_data = f.read()
except FileNotFoundError as e:
    raise (e)
data = json.loads(raw_data)

# Splitting process
if args.split:
    # Make sure that project files do not exist (to prevent data loss)
    try:
        prop_path.touch(exist_ok=False)
        feat_path.touch(exist_ok=False)
    except FileExistsError as e:
        raise (e)

    all_properties = list()
    all_keys = ["split_id"]
    features_copy_with_id = dict()

    # Get the properties of each feature
    feature_index = 0
    for feature in data["features"]:
        # Keep an indexed copy of the properties
        properties_copy = copy.deepcopy(feature["properties"])
        properties_copy["split_id"] = feature_index
        all_properties.append(properties_copy)

        # Create a collective list for all propertes keys
        for key in feature["properties"].keys():
            if key not in all_keys:
                all_keys.append(key)

        # Keep an indexed copy of the feature
        feature_copy = copy.deepcopy(feature)
        features_copy_with_id[feature_index] = feature_copy

        feature_index += 1

    # Write results to files
    with open(feat_path, "w", encoding="utf8") as feat_file:
        feat_data = json.dumps(features_copy_with_id, ensure_ascii=False)
        feat_file.write(feat_data)

    with open(prop_path, "w") as prop_file:
        dict_writer = csv.DictWriter(prop_file, all_keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_properties)

# Joining process
if args.join:
    # Read the features and properties
    try:
        with open(feat_path, "r") as feat_file:
            feat_data = json.loads(feat_file.read())
    except FileNotFoundError as e:
        raise (e)

    try:
        with open(prop_path, "r") as prop_file:
            csv_reader = csv.DictReader(prop_file)
            all_properties = [dict(x) for x in csv_reader]
    except FileNotFoundError as e:
        raise (e)

    # Make sure that project file does not exist (to prevent data loss)
    try:
        final_path.touch(exist_ok=False)
    except FileExistsError as e:
        raise (e)

    final_geojson = copy.deepcopy(data)
    final_geojson["features"] = list()

    for prop in all_properties:
        split_id = prop["split_id"]
        final_prop = copy.deepcopy(prop)
        final_feature = copy.deepcopy(feat_data[split_id])
        final_prop.pop("split_id")

        # Join properties and features based on index
        final_feature["properties"] = final_prop
        final_geojson["features"].append(final_feature)

    with open(final_path, "w", encoding="utf8") as final_file:
        final_data = json.dumps(final_geojson, ensure_ascii=False)
        final_file.write(final_data)

    # Remove the project files
    if not args.keep:
        prop_path.unlink()
        feat_path.unlink()
