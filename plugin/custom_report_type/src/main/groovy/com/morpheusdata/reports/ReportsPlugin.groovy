package com.morpheusdata.reports

import com.morpheusdata.core.Plugin

/**
 * Example Custom Reports Plugin
 */
class ReportsPlugin extends Plugin {

	@Override
	void initialize() {
		CustomReportProvider customReportProvider = new CustomReportProvider(this, morpheus)
		this.pluginProviders.put(customReportProvider.code, customReportProvider)
		this.setName("Patching Report")
		this.setDescription("A custom report plugin for running reports to check patching results")
		
	}

	@Override
	void onDestroy() {
	}
}