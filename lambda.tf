resource "aws_lambda_function" "fetch_data" {
  filename         = "./lambda_function.zip"
  function_name    = "FetchDataFunction"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("./lambda_function.zip")
}

resource "aws_lambda_function" "data_preprocessing" {
  filename         = "./data_preprocessing.py.zip"
  function_name    = "DataPreprocessingFunction"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("./data_preprocessing.py.zip")
}
