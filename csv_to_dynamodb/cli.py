import click
import boto3
import csv
import json
import charset_normalizer

from csv_to_dynamodb.utils import convert_attribute


@click.command()
@click.option(
    '--csv-file',
    type=click.Path(exists=True),
    required=True, 
    help='Path to the CSV file')
@click.option(
    '--csv-delimiter',
    default=',',
    help='CSV delimiter')
@click.option(
    '--dynamodb-table-name',
    required=True, 
    help='DynamoDB table name')
@click.option(
    '--delete-mode',
    is_flag=True,
    help='Enable delete mode')
@click.option(
    '--attribute-types',
    required=False,
    help='JSON string mapping attributes to their types, e.g., '
         '{"age": "number", "is_active": "boolean"}')
@click.option(
    '--ignore-duplicates',
    is_flag=True,
    help='Ignore duplicate items based on primary key')
@click.option(
    '--ignore-conversion-errors',
    is_flag=True,
    help='Ignore conversion errors and skip items with errors')
@click.option(
    '--aws-access-key',
    required=False,
    help='AWS Access Key ID')
@click.option(
    '--aws-secret-key',
    required=False, 
    help='AWS Secret Access Key')
@click.option(
    '--aws-session-token',
    required=False, 
    help='AWS Session Token')
@click.option(
    '--aws-region',
    required=False, 
    help='AWS Region')
def main(
        csv_file,
        csv_delimiter,
        dynamodb_table_name,
        delete_mode,
        attribute_types,
        ignore_duplicates,
        ignore_conversion_errors,
        aws_access_key,
        aws_secret_key,
        aws_session_token,
        aws_region
    ):
    dynamodb = boto3.resource('dynamodb',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=aws_session_token,
        region_name=aws_region)
    table = dynamodb.Table(dynamodb_table_name)
    key_schema = table.key_schema

    attribute_types = json.loads(attribute_types) \
                      if attribute_types else {}
    
    processed_keys = set()

    rows_processed = 0

    with open(
        csv_file, 'r', 
        encoding=charset_normalizer \
                    .from_path(csv_file) \
                    .best() \
                    .encoding
        ) as file:
        reader = csv.DictReader(file, delimiter=csv_delimiter)
        with table.batch_writer() as batch:
            for row in reader:
                keys = {k['AttributeName']: row[k['AttributeName']] 
                        for k in key_schema}

                try:
                    for k, v in row.items():
                        row[k] = convert_attribute(
                                    v, attribute_types.get(k, 'string'))
                except ValueError as e:
                    if ignore_conversion_errors:
                        print(f'Error converting attribute {k} to type '
                              f'{attribute_types.get(k, "string")}. '
                              f'{str(e)}. Skipping item: {keys}')
                        continue
                    else:
                        raise
                    
                if ignore_duplicates or delete_mode:
                    key_repr = json.dumps(keys, sort_keys=True)
                    if key_repr in processed_keys:
                        print(f'Skipping duplicate item: {keys}')
                        continue
                    processed_keys.add(key_repr)

                if delete_mode:
                    batch.delete_item(Key=keys)
                else:
                    batch.put_item(Item=row)

                rows_processed += 1
                if rows_processed % 100 == 0:
                    print(f'{rows_processed} rows processed')
                    
    print(f'Finished: {rows_processed} rows processed and '
          f'{'deleted' if delete_mode else 'inserted'} '
          f'into DynamoDB table {dynamodb_table_name}')    


if __name__ == '__main__':
    main()