from datetime import datetime
import json
import pandas as pd


def read_csv(file):
    # reads csv file and returns Pandas dataframe
    return pd.read_csv(file)


class RunTracker:
    """
    This class will be responsible for tracking model runs. It calculates the desired metadata based on a model's
    inputs, outputs, and other run-specific features, before uploading them to Ersilia's Splunk dashboard.

    NOTE: Currently, the Splunk connection is not set up. For now, we will print tracking results to the console.
    """

    def __init__(self):
        self.time_start = None

    # function to be called before model is run
    def start_tracking(self):
        self.time_start = datetime.now()

    def sample_df(self, df, num_rows, num_cols):
        """
        Returns a sample of the dataframe, with the specified number of rows and columns.
        """
        return df.sample(num_rows, axis=0).sample(num_cols, axis=1)

    def stats(self, result):
        dat = read_csv(result)

        # drop first two columns (key, input)
        dat = dat.drop(["key", "input"], axis=1)

        # calculate and print statistics
        for column in dat:
            print("Mean %s: %s" % (column, dat[column].mean()))
            if len(dat[column].mode()) == 1:
                print("Mode %s: %s" % (column, dat[column].mode()))
            else:
                print("No mode")
            print("Min %s: %s" % (column, dat[column].min()))
            print("Max %s: %s" % (column, dat[column].max()))
            print("Standard deviation %s: %s" % (column, dat[column].std()))

    def get_file_sizes(self, input_df, output_df):
        input_size = input_df.memory_usage(deep=True).sum() / 1024
        output_size = output_df.memory_usage(deep=True).sum() / 1024

        input_avg_row_size = input_size / len(input_df)
        output_avg_row_size = output_size / len(output_df)

        print("Average Input Row Size (KB):", input_avg_row_size)
        print("Average Output Row Size (KB):", output_avg_row_size)

    def track(self, input, result, meta):
        """
        Tracks the results after a model run.
        """
        input_dataframe = read_csv(input)
        result_dataframe = read_csv(result)

        print("Run input file:", input)
        print(input_dataframe)

        print("Run output file:", result)
        print(result_dataframe)

        print("Model metadata:", meta)

        model_id = meta["metadata"].get("Identifier", "Unknown")
        print("Model ID:", model_id)

        time = datetime.now() - self.time_start
        print("Time taken:", time)

        self.stats(result)

        self.get_file_sizes(input_dataframe, result_dataframe)

    def log_to_console(self, data):
        print(f"\n{json.dumps(data)}\n")

    def read_json(self, result):
        data = json.load(result)
        self.log_to_console(result)
        return data
