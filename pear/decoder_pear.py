import struct
import pandas as pd
import os


def extract_pear_to_df(input_path, header_size=0x140, footer_size=0x1e0):
    """
    Extracts binary data from a file to a DataFrame.

    :param input_path: Path to the binary file.
    :param header_size: Size of the header in bytes.
    :param footer_size: Size of the footer in bytes.
    :return: DataFrame containing the extracted data.
    """
    col0 = []
    col1 = []

    with open(input_path, 'rb') as f:
        # Skip the header
        f.seek(header_size)

        # Calculate the size of the body (excluding header and footer)
        file_size = os.path.getsize(input_path)
        body_size = file_size - header_size - footer_size

        # Read the body
        bytes_read = 0
        while bytes_read < body_size:
            # Read 8 bytes (2 columns of 4 bytes each)
            chunk = f.read(8)
            if len(chunk) < 8:
                break

            # Extract values from the specified columns
            col0_val = struct.unpack('<I', chunk[0:4])[0]
            col1_val = struct.unpack('<I', chunk[4:8])[0]

            col0.append(col0_val)
            col1.append(col1_val)

            bytes_read += 8

    # Create DataFrame
    df = pd.DataFrame({'Time (ms)': col0, 'Intensity': col1})
    return df


def main(input_path=None, header_size=0x140, footer_size=0x1e0):
    """
    Extracts binary data from a file to a DataFrame and saves it to a CSV file.

    :param input_path: Path to the binary file.
    :param header_size: Size of the header in bytes.
    :param footer_size: Size of the footer in bytes.
    """
    if input_path is None:
        input_path = input('Enter the path to the binary file: ')

    # Extract the binary data to a DataFrame
    df = extract_pear_to_df(input_path, header_size, footer_size)
    # Save the DataFrame to a CSV file
    df.to_csv(input_path + '.csv', index=True)


if __name__ == '__main__':
    main()
