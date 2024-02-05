# Small (unit) tests directory

Please add appropriate Python unit tests in this directory.
If you need your buildkite CI build to pass and there are no actual tests please uncomment everything in the test_very_little.py

## Update template files 
If your repository is just created with a template https://github.com/alianza-dev/data-shared-streaming-project-template make sure you update files in this directory as described below:

* __foo_bar_transformer_lambda_tests_data__ - _replace `foo_bar` with actual entity name_ 
  * __expected_results__
    * __test1_output.json__ - _replace `"data": {"SOMETESTDATA": 1234567890 }"` with actual data produced by transformer lambda after processing test data from __test1_sns_message_decoded.json___
    * __test2_output.json__ - _replace `"data": {"SOMETESTDATA": 1234567890 }"` with actual data produced by transformer lambda after processing test data from __test2_sns_message_decoded.json___
    * __test3_output.json__ - _there should be the same data as in __test1_sns_message_decoded.json___
  * __input__
    * __test1_sns_message_decoded.json__ - _add 1 sample message. Sample message can be found here https://github.com/alianza-dev/arch-sns-topic-registry/tree/master/topic or recorded from appropriate SNS topic._ 
    * __test2_sns_message_decoded.json__ - _add 2 sample messages_  
* __snapshotter_tests_data__ - _replace all instances of `test_project` and `foo_bar` in the file with actual project name and entity name in all files inside this directory_ 
  * __expected_results__
    * __final_table_data.json__ - _update columns, types, and projection_sql in the file so that they correspond to actual table_
  * __input__
    * __athena_query_results_max_date.json__ - _no changes are required_ 
    * __athena_query_results_select_keys.json__ - _specify columns and types that correspond to actual table_ 
    * __athena_query_start.json__ - _no changes are required_ 
    * __athena_query_status_select_keys.json__ - _no changes are required_ 
    * __test_fetch_stream_tables.json__ - _specify columns and types that correspond to actual table_
* __test_daily_snapshotter_lambda.py__ - _Uncomment everything. Replace all instances of `test_project` and `foo_bar` in the file with actual project name and entity name (for example, `switch_help` and `sip_trunk`). Update `all_cols` variable, specify all table columns. Update `delete_cols` variable, normally it should be `", _delete.col, _delete.type"` if there is a delete column in a table if not specify empty string. Specify `final_query_template` variable, it should be a copy of table.projection_sql variable from lambdas/daily_snapshotter_lambda.py but with actual values instead of variables like `{key_list_a}`, `{self.stream_database}.{table.name}`, etc. Strings `{{start_date}}` and `{{end_date}}` should be updated to `{start_date}` and `{end_date}`._
* __test_foo_bar_transformer_lambda.py__ - _Uncomment everything. Replace all instances of `FooBar` and `foo_bar` in the file with actual entity name (for example, `SipTrunk` and `sip_trunk`)._
