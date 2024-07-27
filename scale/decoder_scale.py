import struct
import pandas as pd
import os


def byte_to_int(byte_str):
    """
    Converts a 4-byte string to an integer, handling two's complement for negative values.

    :param byte_str: 4-byte string to convert.
    :return: Integer representation of the byte string.
    """

    # Convert the byte string to an unsigned integer
    unsigned_int = int.from_bytes(byte_str, byteorder='big', signed=False)

    # Check if the integer is negative (using 2's complement)
    if unsigned_int >= 2 ** 31:
        return unsigned_int - 2 ** 32
    else:
        return unsigned_int


def extract_scale_to_df(input_path, header_size=0x200, footer_size=0):
    """
    Extracts binary data from a file to a DataFrame.

    :param input_path: Path to the binary file.
    :param header_size: Size of the header in bytes.
    :param footer_size: Size of the footer in bytes.
    :return: DataFrame containing the extracted data.
    """
    # Initialize columns
    columns = [[] for _ in
               range(19)]  # Assuming 19 columns based on the provided data

    with open(input_path, 'rb') as f:
        # Skip the header
        f.seek(header_size)

        # Calculate the size of the body (excluding header and footer)
        file_size = os.path.getsize(input_path)
        body_size = file_size - header_size - footer_size

        # Read the body
        bytes_read = 0

        while bytes_read < body_size:

            chunk = f.read(78)

            # Ignore the first 2 padding bytes [48 48]
            chunk = chunk[2:]

            # Get first column as float round to 4 digit
            float_val = struct.unpack('<f', chunk[:4])[0]
            columns[0].append(f"{float_val:.4f}")

            # Extract the rest of the chunk as integers, downscale by 20
            for i in range(1, 19):
                int_val = byte_to_int(chunk[i * 4:(i + 1) * 4]) // 20
                columns[i].append(int_val)

            bytes_read += 78

    # Create DataFrame
    

    # Define the column names
    # Time (min),190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360
    column_names = ['Time (min)', 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360]

    # Create DataFrame using dictionary comprehension
    df = pd.DataFrame({name: columns[i] for i, name in enumerate(column_names)})
    print(df)
    return df


def main(input_path=None, header_size=0x200, footer_size=0):
    """
    Extracts binary data from a file to a DataFrame and saves it to a CSV file.

    :param input_path: Path to the binary file.
    :param header_size: Size of the header in bytes.
    :param footer_size: Size of the footer in bytes.
    """
    if input_path is None:
        input_path = input('Enter the path to the binary file: ')

    # Extract the binary data to a DataFrame
    df = extract_scale_to_df(input_path, header_size, footer_size)
    # Save the DataFrame to a CSV file
    df.to_csv(input_path + '.csv', index=False)


if __name__ == '__main__':
    main()
