terraform {
  required_providers {

    ### provider nutanix - infra platform
    nutanix = {
      source  = "nutanix/nutanix"
      version = "1.9.5"
    }
  }
}
