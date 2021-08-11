import requests

if __name__ == "__main__":
    main()

#Evaluate the OS type and version and get the job name
def main():
    jobid=getJobId()
    workflowid=getJobWorkflowId(jobid)
    targets=getJobTargets(jobid)
    jobstatus=updateJob(jobid,targets,workflowid)
    print(jobstatus)

#Get the jobID
def getJobId(jobname):
    print("got the job id")

#Get the existing workflow/task from the job
def getJobWorkflowId(jobid):
    print("Workflow id is")

#Get the existing instances/server from the job
def getJobTargets(jobid):
    print("Current list of instances/servers")

#Update the job with new instance/server as targets combined with the existing instances/servers attached to the job
def updateJob(jobid,targets,workflowid):
    print("Job updated")
