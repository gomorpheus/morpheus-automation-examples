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

	@Override
	String getCode() {
		'custom-report-patching'
	}

	@Override
	String getName() {
		'Patching Results Summary'
	}

	 ServiceResponse validateOptions(Map opts) {
		 return ServiceResponse.success()
	 }


	@Override
	HTMLResponse renderTemplate(ReportResult reportResult, Map<String, List<ReportResultRow>> reportRowsBySection) {
		ViewModel<String> model = new ViewModel<String>()
		model.object = reportRowsBySection
		getRenderer().renderTemplate("hbs/patchingReport", model)
	}

	/**
	 * Allows various sources used in the template to be loaded
	 * @return
	 */
	@Override
	ContentSecurityPolicy getContentSecurityPolicy() {
		def csp = new ContentSecurityPolicy()
		csp.scriptSrc = '*.jsdelivr.net'
		csp.frameSrc = '*.digitalocean.com'
		csp.imgSrc = '*.wikimedia.org'
		csp.styleSrc = 'https: *.bootstrapcdn.com'
		csp
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
			if(reportResult.configMap?.phrase) {
				String phraseMatch = "${reportResult.configMap?.phrase}%"
				results = new Sql(dbConnection).rows("SELECT id, server_name, date_created, last_updated, next_run, result, os, env from patching WHERE server_name LIKE ${phraseMatch} order by date_created asc;")
			} else {
				results = new Sql(dbConnection).rows("SELECT id, server_name, date_created, last_updated, next_run, result, os, env from patching order by date_created asc;")
			}
	    // Close the database connection
		} finally {
			morpheus.report.releaseDatabaseConnection(dbConnection)
		}
		log.info("Results: ${results}")
		Observable<GroovyRowResult> observable = Observable.fromIterable(results) as Observable<GroovyRowResult>
		observable.map{ resultRow ->
			log.info("Mapping resultRow ${resultRow}")
			Map<String,Object> data = [id: resultRow.id.toString(), server_name: resultRow.server_name.toString(), date_created: resultRow.date_created.toString(), last_updated: resultRow.last_updated.toString(), next_run: resultRow.next_run.toString(), result: resultRow.result.toString(), os: resultRow.os.toString(), environment: resultRow.env.toString() ]
			ReportResultRow resultRowRecord = new ReportResultRow(section: ReportResultRow.SECTION_MAIN, displayOrder: displayOrder++, dataMap: data)
			log.info("resultRowRecord: ${resultRowRecord.dump()}")
			totalItems++
			//if (resultRow.result.startsWith('success')) {
			//	successResults++
			//}
			//if (resultRow.result.startsWith('failed')) {
			//	failedResults++
			//}
			//if (resultRow.item_key.startsWith('secret')) {
			//	secretResults++
			//}
			//if (resultRow.item_key.startsWith('uuid')) {
			//	uuidResults++
			//}
			//if (resultRow.item_key.startsWith('key')) {
			//	keyResults++
			//}
			//if (resultRow.item_key.startsWith('random')) {
		//		randomResults++
			//}
			return resultRowRecord
		}.buffer(50).doOnComplete {
			morpheus.report.updateReportResultStatus(reportResult,ReportResult.Status.ready).blockingGet();
		}.doOnError { Throwable t ->
			morpheus.report.updateReportResultStatus(reportResult,ReportResult.Status.failed).blockingGet();
		}.subscribe {resultRows ->
			morpheus.report.appendResultRows(reportResult,resultRows).blockingGet()
		}
		//Map<String,Object> data = [total_items: totalItems, success: successResults, failed: failedResults]
		Map<String,Object> data = [total_items: totalItems]
		ReportResultRow resultRowRecord = new ReportResultRow(section: ReportResultRow.SECTION_HEADER, displayOrder: displayOrder++, dataMap: data)
        morpheus.report.appendResultRows(reportResult,[resultRowRecord]).blockingGet()
	}

	// https://developer.morpheusdata.com/api/com/morpheusdata/core/ReportProvider.html#method.summary
	// The description associated with the custom report
	 @Override
	 String getDescription() {
		 return "Patching History"
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

	// https://developer.morpheusdata.com/api/com/morpheusdata/model/OptionType.html
	 @Override
	 List<OptionType> getOptionTypes() {
		 [new OptionType(code: 'status-report-search', name: 'Search', fieldName: 'phrase', fieldContext: 'config', fieldLabel: 'Search by servername', displayOrder: 0)]
	 }
 }