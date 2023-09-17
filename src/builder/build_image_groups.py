import os
from pprint import pprint
from argparse import ArgumentParser

from json_to_dirs import ValidationError, validate_json, parse_json, make_item_groups
from process_item import make_image_file_group, log_item

def main(input_path:str, output_dir:str):
    finish_line_log:str = '-------------------------------------------------------------------------------------------------------------------------------------'
    print(f"input_path = {input_path}")
    print('READING INPUT...')
    words_data:dict = parse_json(input_path)
    print(f"input_data = ")
    pprint(words_data)
    print(finish_line_log)


    print('VALIDATING INPUT...')
    data_validate_result: [ValidationError | None] = validate_json(words_data, 3, lambda item: all(key in item for key in ['word', 'hint']))
    if data_validate_result:
        print(data_validate_result.what)
        if isinstance(data_validate_result.err_data, list):
            for err_item in data_validate_result.err_data:
                print(err_item)
        else:
            print(data_validate_result.err_data)
        return
    
    print(finish_line_log)
    

    print('PROCESSING ITEM...')
    # make_item_groups(output_dir, words_data, log_item)
    make_item_groups(output_dir, words_data, make_image_file_group)
    print(finish_line_log)

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    pkg_dir:str = os.path.join(os.getcwd(), '..', '..')
    default_input_path:str = os.path.join(pkg_dir, 'tests', 'sample_0.json')
    default_output_path:str = os.path.join(pkg_dir, 'out')
    arg_parser.add_argument('input', type=str, help='Input JSON path')
    arg_parser.add_argument('output', type=str, help='Output dir')
    args = arg_parser.parse_args()
    input_path:str = default_input_path if args.input == 'default' else args.input
    output_dir:str = default_output_path if args.output == 'default' else args.output
    main(input_path, output_dir)