# CSV to DynamoDB

Transfer data from a CSV file to a DynamoDB table. It also supports a mode for deleting items.

## Installation

Install dependencies using [Poetry](https://python-poetry.org/):

```bash
poetry install
```

## Usage

```bash
poetry run csv-to-dynamodb \
  --csv-file <CSV_FILE_PATH> \
  [--csv-delimiter <CSV_DELIMITER>] \
  --dynamodb-table-name <DYNAMODB_TABLE_NAME> \
  [--delete-mode] \
  [--attribute-types '{"attribute1": "string", "attribute2": "number"}'] \
  [--ignore-duplicates] \
  [--ignore-conversion-errors] \
  [--aws-access-key <AWS_ACCESS_KEY>] \
  [--aws-secret-key <AWS_SECRET_KEY>] \
  [--aws-session-token <AWS_SESSION_TOKEN>] \
  [--aws-region <AWS_REGION>]
```

### Options
- `--csv-file`: Path to the CSV file.
- `--csv-delimiter`: Delimiter used in the CSV file (default: `,`).
- `--dynamodb-table-name`: Target DynamoDB table name.
- `--delete-mode`: Deletes items in DynamoDB instead of inserting them.
- `--attribute-types`: JSON string mapping attributes to their types. Supported types are `string`, `number`, and `boolean`. For example: `{"age": "number", "is_active": "boolean"}` (optional).
- `--ignore-duplicates`: Skips duplicate items based on primary key.
- `--ignore-conversion-errors`: Ignore conversion errors and skip items with errors.
- `--aws-access-key`: AWS Access Key ID (optional).
- `--aws-secret-key`: AWS Secret Access Key (optional).
- `--aws-session-token`: AWS Session Token (optional).
- `--aws-region`: AWS Region (optional).