# Run Tasks by Tag

# Description
The purpose of this script is to execute a task against multiple instances simultaneously if a tag name and value match the search criteria.

This task can be run hardcoded or as part of a workflow.

# Usage

This script will work drawn from a repo or entered as local content

## Create an Option Type

This example will use a manual option type.  

Set `NAME`

Set `FIELD NAME` to something with no spaces.

Set `TYPE` to `Text`

Set `LABEL` to whatever text label you want the input field to have.

Make sure `REQUIRED` is checked.

## Define a new python task

Set `Name`

In `COMMAND ARGUMENTS` add three arguments separated by a space.  
- The first is the `task id` you want to be executed on each instance.  
- The second is the `tag name` you want to search by.  
- The third is the `field name` of the option type you pass to the task.

```
eg: 39 patchwindowtag patchoption
```
- This would execute task 39 by searching the patchwindowtag`tag on all instances.

In `ADDITIONAL PACKAGES` add `requests`

Set `EXECUTE TARGET` to `Local`

## Define a new Operational Workflow

Set `NAME`

Set `Tasks` to include your created task.

Set `Option Types` to include your created Option Type.

## Running the Workflow

When you execute this workflow, you will need to input the tag value you will search on.  

If the tag name in your python task was `update_window` and you input `sun1200` in the workflow this task would search all your visible instances for the `update_window` tag.  If the value of that tag was `sun1200` it would execute the `task id` you input in the python task against each instance that matched.