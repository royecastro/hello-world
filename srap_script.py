import os

base_dir = 'campaign_queries'
subdirectories_to_process = {
    'pet_food': ['nexgard.sql'],
    'toys': ['christmas.sql']
}

# Collect all errors during processing
error_log = []

for sub_dir, sql_files in subdirectories_to_process.items():
    try:
        subdir_path = os.path.join(base_dir, sub_dir)

        if not os.path.exists(subdir_path) or not os.path.isdir(subdir_path):
            raise FileNotFoundError(f"Subdirectory {subdir_path} does not exist or is not a directory.")

        for sql_file in sql_files:
            try:
                query_file = os.path.join(subdir_path, sql_file)

                if not os.path.exists(query_file) or not os.path.isfile(query_file):
                    raise FileNotFoundError(f"SQL file {query_file} does not exist or is not a file.")

                query_name = os.path.splitext(sql_file)[0]

                with open(query_file, 'r') as f:
                    query = f.read()

                print(f"Creating table {query_name}")
                table_id = f"{PROJECT}.{DATASET}.{query_name}"
                BQ.easy_query(query, destination=table_id)
                print('\tTable successfully uploaded')

            except Exception as file_error:
                error_log.append(
                    f"[{sub_dir}/{query_name}] Failed processing SQL file '{query_file}': {file_error}"
                )
                continue

    except Exception as dir_error:
        error_log.append(
            f"[{sub_dir}] Failed processing directory '{subdir_path}': {dir_error}"
        )
        continue

# Report and raise error if any issues occurred
if error_log:
    print("\nErrors encountered:")
    for error in error_log:
        print(error)

    # Raise exception to trigger pipeline/email notifications
    raise RuntimeError(
        "One or more errors occurred during SQL processing:\n" +
        "\n".join(error_log)
    )
else:
    print("\nAll files processed successfully.")
