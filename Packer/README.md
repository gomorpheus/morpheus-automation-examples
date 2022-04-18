# CentOS Images

CentOS 7 and 8 images are available here: http://morpheus-image-examples.s3-website-us-west-1.amazonaws.com/

Among other featurees, these images include:

- Network Manager Enabled
- SELinux set to Permissive mode
- First 4 NICs renamed to eth0-3 for VMWare through udev rules
- Older versions are pinned to vault repositories, meaning they will receive no security updates.
  - These are meant for organizations with supplementary patching strategies.
- Root password disabled, login using your Morpheus User Settings credentials or credentials supplied in your Virtual Image definition.

## Packer Examples

These examples should work on Linux, MacOS, and WSL in Windows.  Copy the and remove `.dist` from the `pkrvars` files to `.hcl` and modify the variables inside for your environment.  The important vars are:
```
vm_network # The name of the network to attach the template to while building
remote_datastore # The name of the datastore to use
esx_host # IP address of the esx host that vCenter will deploy to
remote_host # IP of vCenter
remote_username # Username on vCenter
remote_password # Password on vCenter
```


Install the latest version of packer and run using the following in the directory with all the hcl files:
```
packer build -on-error=ask .
```