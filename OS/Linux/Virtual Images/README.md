# CentOS Images

CentOS 7 and 8 images are available here: http://morpheus-image-examples.s3-website-us-west-1.amazonaws.com/

Among other featurees, these images include:

- Network Manager Enabled
- SELinux set to Permissive mode
- First 4 NICs renamed to eth0-3 for VMWare through udev rules
- Older versions are pinned to vault repositories, meaning they will receive no security updates.
  - These are meant for organizations with supplementary patching strategies.
- Root password disabled, login using your Morpheus User Settings credentials or credentials supplied in your Virtual Image definition.
