locals {
  #  Common tags to be assigned to all resources
  default_tags = {
    Owner    = "<%=username%>"
    Group = "<%=groupName%>"
    Management_Tool = "Terraform"
    Management_Platform = "Morpheus"
  }
  
  subnet_options = {
    cidrMask = "<%=customOptions.cidrMask%>"
    subnetCount = "<%=customOptions.subnetCount%>"
  }
  vpc_options = {
    region = "<%=customOptions.awsRegion%>"
    aws_account = "<%=customOptions.awsAccount%>"
  }
}