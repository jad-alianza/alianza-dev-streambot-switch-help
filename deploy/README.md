# Deployment

## Update template files 
If your repository is just created with a template https://github.com/alianza-dev/data-shared-streaming-project-template make sure you update files in this directory as described below:

* __ansible__
  * __vars__
    * __env_type__
      * __b2.yml__ - _this configuration file extends configuration form __ansible/vars/main.yml__.  Specify entity(ies) that will be precessed by your app. Replace `fooBar` with actual entity name (for example, `sipTrunk`). Specify actual awsAccount number and SNS topicArn that your deliveryStream will be subscribed to. Make sure topicArn for __Beta__ environment is specified. For d2, b2, q2, make sure awsAccount for lab environments is specified_
      * __d2.yml__ - _similar to previous but for d2 env (use appropriate __Lab__ awsAccount and topicArn for __Dev__ environment)_
      * __p2.yml__ - _similar to previous but for p2 env (use appropriate __Prod__ awsAccount and topicArn for __Prod__ environment)_
      * __q2.yml__ - _similar to previous but for q2 env (use appropriate __LAB__ awsAccount and topicArn for __QA__ environment)_
    * __cloudFormation.yml__ - _no updates are required_
    * __main.yml__ - _common for all environments(d2,q2,b2,p2) entity configuration. Replace `fooBar` and `foo_bar` with actual entity name (for example, `sipTrunk` and `sip_trunk`). You may also specify additional filtering parameters to process only specific messages from SNS topic, for example: `key: 'objectType'`, `vals: 'SIPTRUNK_V3'` or remove those parameters to process all messages from SNS topic. If your app processes multiple entities you need to specify all entities in the `entityRoster:` dictionary_
  * __ansible.cfg__ - _no updates are required_
  * __deploy.yml__ - _no updates are required since the following env. variables from `.core.env` are referenced in the file: `APP_NAME_FULL` and `APP_NAME_SHORT`. Make sure all environment variables in the .core.env file have values set_
  * __requirements.yml__ - _no updates are required_
* __cloudFormation__
  * __core.CF.j2.yml__ - _Replace all instances of `FooBar`, `fooBar`, and `foo_bar` in the file with actual entity name (for example, `SipTrunk`, `sipTrunk`, and `sip_trunk`). Specify all columns in the `GlueTableParquetFooBar` section. If your app processes multiple entities you need to have `GlueTableParquetFooBar` with appropriate columns for each entity. Also for each entity there should be the following line added after line #21: `{% set ecFooBar = c.ent|selectattr('keyName','eq','fooBar')|first %}`._
  * __monitoring.CF.j2.yml__ - _no updates are required_
  * __parent.CF.j2.yml__ - _no updates are required_
* __README.md__ - _no updates are required_
* __run.sh__ - _this script is triggered by the `.buildkite/scripts/deploy.sh` file and it executes the ansible command. It does not need to be updated._ 
