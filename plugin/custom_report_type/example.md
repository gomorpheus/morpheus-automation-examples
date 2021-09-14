# Developing Morpheus Plugins

[Using the Sample](#using_the_sample_morpheus_custom_report_plugin)

## Using the sample Morpheus custom report plugin
The sample custom report plugin is an example of how the Morpheus plugin framework can be used to create a custom report based upon data stored in the Morpheus database.

**Sample Plugin Overview**

The sample plugin generates a summary or overview report for Cypher items within the Morpheus platform. 

![](_images/morpheus_sample_report_results.png)

* Query the cypher_item table from the MySQL morpheus database
* Count the total number of cypher items
* Count the different cypher item types (secret, tfvars, uuid, etc.)

### Building the sample plugin

Now that we know what the sample plugin does we'll walk through how to build the plugin. The sample plugin is built using the gradle build tool.

**Prerequisites**

Before building the sample plugin you must meet the following system requirements:

* Gradle 6.5 or later
* Java 8 or Java 11
* Git

**Build the plugin**

1. Clone the sample plugin repository

   ```bash
   git clone https://github.com/martezr/morpheus-example-reports-plugin.git
   ```

2. Change the directory to the sample plugin directory

   ```bash
   cd morpheus-example-reports-plugin
   ```

3. Build the sample plugin

   ```bash
   gradle shadowJar
   ```

   The build process should take a few seconds to complete.

   ```bash
   Starting a Gradle Daemon (subsequent builds will be faster)
   > Task :assetCompile
   > Task :compileJava NO-SOURCE
   > Task :compileGroovy
   > Task :processResources
   > Task :classes
   > Task :configureRelocationShadowJar
   > Task :shadowJar
   
   Deprecated Gradle features were used in this build, making it incompatible with Gradle 7.0.
   Use '--warning-mode all' to show the individual deprecation warnings.
   See https://docs.gradle.org/6.8.2/userguide/command_line_interface.html#sec:command_line_warnings
   
   BUILD SUCCESSFUL in 22s
   5 actionable tasks: 5 executed
   ```

   The plugin JAR file can be found in the build/libs directory

### Upload the plugin
Before we can use the plugin, we need to upload the plugin to our Morpheus installation. The plugin can be installed by navigating to the **plugins** section (Administration > Integrations > Plugins) in the Morpheus UI.

![](_images/morpheus_plugin_upload.png)

### Generating a report

Now that the plugin has been installed we are ready to generate a report using the custom report plugin. Locate the **CYPHER SUMMARY** report in the **Reports** subsection of the **Operations** section in the Moprheus UI. Click **RUN NOW** to the right of the **CYPHER SUMMARY** report to generate a new report.

![](_images/morpheus_reports.png)

Once the report has been generated the report status will change to **Ready** and the report can be viewed by clicking on the blue name link underneath the **FILTERS** column.

![](/Users/martezreed/mopho-demo-plugin/_images/morpheus_report_results.png)

The report will show the breakdown of Cypher items by type as well as a basic table of the items sorted by alphabetical order.

![](_images/morpheus_sample_report_results.png)

We have now successfully walked through the steps to build and use the Morpheus custom report sample plugin.

## Creating a Morpheus custom report plugin

In the previous section we walked through how to use the custom report sample plugin and now we'll go through creating the plugin from scratch to understand the custom report plugin development process.

#### Accessing the Morpheus Database

The MySQL database listens on the host's loopback address for a single node AIO installation by default. This means that we have to connect to the database using the MySQL client locally or use a feature like SSH proxying with MySQL Workbench.

**Morpheus Database Credentials**

Before we connect to the database we'll need the credentials for accessing the database. During the installation process of Morpheus a secrets file is created on the file system with the credentials for the MySQL database.

```bash
cat /etc/morpheus/morpheus-secrets.json
```


```bash
{
  "mysql": {
    "root_password": "389dd03291033se42c5404d5d",
    "morpheus_password": "a0c4c59322c898qyw2e1ca59b",
    "ops_password": "0c1d000b792432lwp413f0f546c"
  },
  "rabbitmq": {
    "morpheus_password": "03868913jasdfebb1",
    "queue_user_password": "2c590a02284186ce",
    "cookie": "1401B43E0103PWAA25BE"
  },
  "ui": {
    "ajp_secret": "c4a0ap91d6de6110d59100ac"
  }
}
```

Enter the **morpheus_password** when prompted for the **morpheus** user password.


```bash
/opt/morpheus/embedded/mysql/bin/mysql -u morpheus -h 127.0.0.1 -p
```

Access the **morpheus** database with the `USE moprheus` SQL statement.

```sql
USE morpheus;
```

The tables in the **morpheus** database can be listed with the `SHOW TABLES` SQL statement.

```sql
SHOW TABLES;
```

The `SHOW TABLES` command should output the list of tables in the morpheus database similar to the list displayed below. 

> *The list has been truncated for brevity purposes*

```sql
+--------------------------------------------------------------+
| Tables_in_morpheus                                           |
+--------------------------------------------------------------+
| DATABASECHANGELOG                                            |
| DATABASECHANGELOGLOCK                                        |
| access_token                                                 |
| account                                                      |
| account_invoice                                              |
| backup_integration                                           |
| build_job_execution                                          |
| campaign                                                     |
| compute_action                                               |
| cveitem                                                      |
| cypher_item                                                  |
| datastore                                                    |
| datastore_compute_zone_pool                                  |
| datastore_datastore                                          |
| deployment                                                   |
| wiki_page                                                    |
| workload_state                                               |
+--------------------------------------------------------------+
698 rows in set (0.00 sec)

```

In this example the table that we want to use is the **cypher_item** database table which contains the cypher items. Now that we have the table that we want to use we need to know what field are available in the table.

```sql
select COLUMN_NAME,DATA_TYPE from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='cypher_item';
```

The SQL query should display a list of the fields in the **cypher_items** table that we can access data from.

```
+------------------+-----------+
| COLUMN_NAME      | DATA_TYPE |
+------------------+-----------+
| id               | bigint    |
| encryption_key   | varchar   |
| item_value       | text      |
| date_created     | datetime  |
| last_updated     | datetime  |
| cypher_id        | varchar   |
| lease_timeout    | bigint    |
| last_accessed    | datetime  |
| lease_object_ref | varchar   |
| created_by       | varchar   |
| expire_date      | datetime  |
| item_key         | varchar   |
+------------------+-----------+
12 rows in set (0.00 sec)
```

Now that know the fields that are available in the table we're ready to create a SQL statement to query database for the value of the fields that we're interested in. In our example the fields that we're interested in are the item_key, last_update, last_accessed and least_timeout fields.

```sql
SELECT item_key,last_updated,last_accessed,lease_timeout from cypher_item order by item_key asc;
```

The SQL query should generate a list of entries in the table similar to that displayed below.

```
+--------------------------------+---------------------+---------------------+---------------+
| item_key                       | last_updated        | last_accessed       | lease_timeout |
+--------------------------------+---------------------+---------------------+---------------+
| password/32/passwordtest       | 2021-02-17 23:09:19 | 2021-03-08 21:06:10 |             0 |
| password/test                  | 2021-02-17 23:07:50 | 2021-03-08 21:06:07 |             0 |
| random/pltest                  | 2021-03-08 20:50:46 | 2021-03-08 21:06:15 |             0 |
| secret/demo-kube-cluster-token | 2021-05-26 16:54:10 | 2021-05-26 16:54:10 |             0 |
| secret/pechallenge             | 2021-06-01 16:34:17 | 2021-06-01 16:34:20 |             0 |
| tfvars/dev-aws-credentials     | 2021-06-03 16:55:10 | 2021-06-03 16:55:10 |             0 |
| tfvars/vspheredemo             | 2021-02-22 17:23:34 | 2021-06-03 16:53:46 |             0 |
+--------------------------------+---------------------+---------------------+---------------+
7 rows in set (0.00 sec)
```



## Developing the custom report plugin

Now that we know the table in the database and fields that we want to use for our report we're ready to start writing some code. The first thing we'll need to do is create a directory for our plugin.

```bash
mkdir example-report-plugin
```

With the directory created let's take a look at the directory structure that we'll create before we jump right into writing the code.

### File structure

| Name                        | Description                                              | Path                                                                 |
| --------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------- |
| build.gradle                | The gradle build file                                    | build.gradle                                                         |
| gradle.properties           | This file is a properties file for the Gradle build tool | gradle.properties                                                    |
| CustomReportProvider.groovy |                                                          | src/main/groovy/com/morpheusdata/reports/CustomReportProvider.groovy |
| ReportsPlugin.groovy        |                                                          | src/main/groovy/com/morpheusdata/reports/ReportsPlugin.groovy        |
| cypherReport.hbs            | This file is the UI component of the custom report       | src/mainresources/renderer/hbs/cypherReport.hbs                      |

## Create a build.gradle file

Gradle is the build tool used to build Morpheus plugins and a `build.gradle` file is required.

* group:
* version: This specifies the version number of the plugin, this is displayed in the **plugins** section in the Morpheus UI. 
* Plugin-class: In the case of our example `com.morpheusdata.reports.ReportsPlugin` is the Morpheus plugin class that should be used for a custom report plugin.

```groovy
plugins {
    id "com.bertramlabs.asset-pipeline" version "3.3.2"
    id "com.github.johnrengelman.plugin-shadow" version "2.0.3"
}

apply plugin: 'java'
apply plugin: 'groovy'
apply plugin: 'maven-publish'

group = 'com.example'
version = '1.2.2'

sourceCompatibility = '1.8'
targetCompatibility = '1.8'

ext.isReleaseVersion = !version.endsWith("SNAPSHOT")

repositories {
    mavenCentral()
}

dependencies {
    compileOnly 'com.morpheusdata:morpheus-plugin-api:0.8.0'
    compileOnly 'org.codehaus.groovy:groovy-all:2.5.6'
    compileOnly 'io.reactivex.rxjava2:rxjava:2.2.0'
    compileOnly "org.slf4j:slf4j-api:1.7.26"
    compileOnly "org.slf4j:slf4j-parent:1.7.26"
}

jar {
    manifest {
        attributes(
            'Plugin-Class': 'com.morpheusdata.reports.ReportsPlugin', //Reference to Plugin class
            'Plugin-Version': archiveVersion.get() // Get version defined in gradle
        )
    }
}

tasks.assemble.dependsOn tasks.shadowJar
```

## Create the Plugin Class

We now need to create a plugin class to handle the plugin registration process.

```groovy
package com.morpheusdata.reports

import com.morpheusdata.core.Plugin

class ReportsPlugin extends Plugin {

	@Override
	void initialize() {
		CustomReportProvider customReportProvider = new CustomReportProvider(this, morpheus)
		this.pluginProviders.put(customReportProvider.code, customReportProvider)
		this.setName("Custom Cypher Report")
		this.setDescription("A custom report plugin for cypher items")
	}

	@Override
	void onDestroy() {
	}
}
```

## Create the Report Provider Class



```groovy
package com.morpheusdata.reports

import com.morpheusdata.core.AbstractReportProvider
import com.morpheusdata.core.MorpheusContext
import com.morpheusdata.core.Plugin
import com.morpheusdata.model.OptionType
import com.morpheusdata.model.ReportResult
import com.morpheusdata.model.ReportType
import com.morpheusdata.model.ReportResultRow
import com.morpheusdata.model.ContentSecurityPolicy
import com.morpheusdata.views.HTMLResponse
import com.morpheusdata.views.ViewModel
import com.morpheusdata.response.ServiceResponse
import groovy.sql.GroovyRowResult
import groovy.sql.Sql
import groovy.util.logging.Slf4j
import io.reactivex.Observable;
import java.util.Date

import java.sql.Connection

@Slf4j
class CustomReportProvider extends AbstractReportProvider {
	Plugin plugin
	MorpheusContext morpheusContext

	CustomReportProvider(Plugin plugin, MorpheusContext context) {
		this.plugin = plugin
		this.morpheusContext = context
	}

	@Override
	MorpheusContext getMorpheus() {
		morpheusContext
	}

	@Override
	Plugin getPlugin() {
		plugin
	}

  // Define the Morpheus code associated with the plugin
	@Override
	String getCode() {
		'custom-report-cypher'
	}

  // Define the name of the report displayed on the reports page
	@Override
	String getName() {
		'Cypher Summary'
	}

	 ServiceResponse validateOptions(Map opts) {
		 return ServiceResponse.success()
	 }

	@Override
	HTMLResponse renderTemplate(ReportResult reportResult, Map<String, List<ReportResultRow>> reportRowsBySection) {
		ViewModel<String> model = new ViewModel<String>()
		model.object = reportRowsBySection
		getRenderer().renderTemplate("hbs/instanceReport", model)
	}
 
	void process(ReportResult reportResult) {
		// Update the status of the report (generating) - https://developer.morpheusdata.com/api/com/morpheusdata/model/ReportResult.Status.html
		morpheus.report.updateReportResultStatus(reportResult,ReportResult.Status.generating).blockingGet();
		Long displayOrder = 0
		List<GroovyRowResult> results = []
		Connection dbConnection
		Long passwordResults = 0
		Long tfvarsResults = 0
		Long secretResults = 0
		Long uuidResults = 0
		Long keyResults = 0
		Long randomResults = 0
		Long totalItems = 0

		try {
			// Create a read-only database connection
			dbConnection = morpheus.report.getReadOnlyDatabaseConnection().blockingGet()
			// Evaluate if a search filter or phrase has been defined
				results = new Sql(dbConnection).rows("SELECT item_key,last_updated,last_accessed,lease_timeout from cypher_item order by item_key asc;")
	    // Close the database connection
		} finally {
			morpheus.report.releaseDatabaseConnection(dbConnection)
		}
		log.info("Results: ${results}")
		Observable<GroovyRowResult> observable = Observable.fromIterable(results) as Observable<GroovyRowResult>
		observable.map{ resultRow ->
			log.info("Mapping resultRow ${resultRow}")
			Map<String,Object> data = [key: resultRow.item_key, last_updated: resultRow.last_updated.toString(), last_accessed: resultRow.last_accessed.toString(), lease_timeout: resultRow.lease_timeout ]
			ReportResultRow resultRowRecord = new ReportResultRow(section: ReportResultRow.SECTION_MAIN, displayOrder: displayOrder++, dataMap: data)
			log.info("resultRowRecord: ${resultRowRecord.dump()}")
			totalItems++
      // Evaluate if the cypher item starts with password
			if (resultRow.item_key.startsWith('password')) {
				passwordResults++
			}
      // Evaluate if the cypher item starts with tfvars
			if (resultRow.item_key.startsWith('tfvars')) {
				tfvarsResults++
			}
      // Evaluate if the cypher item starts with secret
			if (resultRow.item_key.startsWith('secret')) {
				secretResults++
			}
      // Evaluate if the cypher item starts with uuid
			if (resultRow.item_key.startsWith('uuid')) {
				uuidResults++
			}
      // Evaluate if the cypher item starts with key
			if (resultRow.item_key.startsWith('key')) {
				keyResults++
			}
      // Evaluate if the cypher item starts with random
			if (resultRow.item_key.startsWith('random')) {
				randomResults++
			}
			return resultRowRecord
		}.buffer(50).doOnComplete {
			morpheus.report.updateReportResultStatus(reportResult,ReportResult.Status.ready).blockingGet();
		}.doOnError { Throwable t ->
			morpheus.report.updateReportResultStatus(reportResult,ReportResult.Status.failed).blockingGet();
		}.subscribe {resultRows ->
			morpheus.report.appendResultRows(reportResult,resultRows).blockingGet()
		}
		Map<String,Object> data = [total_items: totalItems, password_items: passwordResults, tfvars_items: tfvarsResults, secret_items: secretResults, uuid_items: uuidResults, key_items: keyResults, random_items: randomResults]
		ReportResultRow resultRowRecord = new ReportResultRow(section: ReportResultRow.SECTION_HEADER, displayOrder: displayOrder++, dataMap: data)
        morpheus.report.appendResultRows(reportResult,[resultRowRecord]).blockingGet()
	}

	// https://developer.morpheusdata.com/api/com/morpheusdata/core/ReportProvider.html#method.summary
	// The description associated with the custom report
	 @Override
	 String getDescription() {
		 return "View an inventory of Cypher items"
	 }

	 // The category of the custom report
	 @Override
	 String getCategory() {
		 return 'inventory'
	 }

	 @Override
	 Boolean getOwnerOnly() {
		 return false
	 }

	 @Override
	 Boolean getMasterOnly() {
		 return true
	 }

	 @Override
	 Boolean getSupportsAllZoneTypes() {
		 return true
	 }
 }
```



## Create the report user interface



```html
<div id="hypervisor-inventory-report">
   <div class="intro-stats">
      <h2>Overview</h2>
      <div class="count-stats">
         <div class="stats-container">
            <span class="big-stat">{{ header.0.dataMap.total_items }}</span>
            <span class="stat-label">Items</span>
         </div>
         <div class="stats-container">
            <span class="big-stat">{{ header.0.dataMap.password_items }}</span>
            <div class="stat-label">Password</div>
         </div>
         <div class="stats-container">
            <span class="big-stat">{{ header.0.dataMap.tfvars_items }}</span>
            <div class="stat-label">TF Vars</div>
         </div>
         <div class="stats-container">
            <span class="big-stat">{{ header.0.dataMap.secret_items }}</span>
            <div class="stat-label">Secret</div>
         </div>
         <div class="stats-container">
            <span class="big-stat">{{ header.0.dataMap.uuid_items }}</span>
            <div class="stat-label">UUID</div>
         </div>
         <div class="stats-container">
            <span class="big-stat">{{ header.0.dataMap.key_items }}</span>
            <div class="stat-label">Key</div>
         </div>
         <div class="stats-container">
            <span class="big-stat">{{ header.0.dataMap.random_items }}</span>
            <div class="stat-label">Random</div>
         </div>
      </div>
   </div>
   <h2>Cypher Items</h2>
   <table>
      <thead>
         <th>Key</th>
         <th>Last Updated</th>
         <th>Last Accessed</th>
         <th>Lease Timeout</th>
      </thead>
      <tbody>
         {{#each main}}
         <tr>
            <td>{{dataMap.key}}</td>
            <td>{{dataMap.last_updated}}</td>
            <td>{{dataMap.last_accessed}}</td>
            <td>{{dataMap.lease_timeout}}</td>
         </tr>
         {{/each}}
      </tbody>
   </table>
</div>
```

We should now have a fully functional custom report plugin that we can build and add to our deployment of Morpheus.

## Additional Resources

The following resources provide additional information to help with the development of Morpheus plugins:

* Morpheus Plugin Docs: https://developer.morpheusdata.com/docs
* Morpheus Plugin API Docs: https://developer.morpheusdata.com/api/index.html?overview-summary.html
* Handlebars templating: https://github.com/jknack/handlebars.java
