import os
import sys
from packaging import version
from pprint import pprint

actually_delete = False

if len(sys.argv) > 1:
    if sys.argv[1] == 'doit':
        print("DELETE ENABLED")
        actually_delete = True

main_directory = '/var/opt/morpheus/package-repos'
#main_subdirs = ['apt', 'yum', 'msi']

apt_directories = [
    '/var/opt/morpheus/package-repos/apt/dists/morpheus/main/binary-i386/',
    '/var/opt/morpheus/package-repos/apt/dists/morpheus/main/binary-amd64/'
]

for aptdir in apt_directories:
    debdict = {}
    # Get version max
    for filename in os.listdir(aptdir):
        if not str(filename).startswith('morpheus'):
            continue
        fnsplit = str(filename).split('_')
        name = fnsplit[0]
        pkgversion = fnsplit[1]
        if name in debdict:
            if version.parse(debdict[name]) < version.parse(pkgversion):
                debdict[fnsplit[0]] = pkgversion
        else:
            debdict[name] = pkgversion
    # Delete other versions
    for filename in os.listdir(aptdir):
        if not str(filename).startswith('morpheus'):
            continue
        fnsplit = str(filename).split('_')
        filepath = aptdir + filename
        if fnsplit[1] not in debdict[fnsplit[0]]:
            if actually_delete:
                os.remove(filepath)
                print("DELETED %s" % filepath)
            else:
                print("I WOULD DELETE %s" % filepath)
        else:
            print("LEAVING %s" % filepath)

rpmdirectories = [
    '/var/opt/morpheus/package-repos/yum/amazon/latest/x86_64/',
    '/var/opt/morpheus/package-repos/yum/amazon/2/x86_64/',
    '/var/opt/morpheus/package-repos/yum/el/6/x86_64/',
    '/var/opt/morpheus/package-repos/yum/el/6/i386/',
    '/var/opt/morpheus/package-repos/yum/el/7/x86_64/',
    '/var/opt/morpheus/package-repos/yum/el/8/x86_64/',
    '/var/opt/morpheus/package-repos/yum/sles/12/x86_64/',
    '/var/opt/morpheus/package-repos/yum/sles/15/x86_64/'
]

for rpmdir in rpmdirectories:
    rpmdict = {}
    # Get version max
    for filename in os.listdir(rpmdir):
        if not str(filename).startswith('morpheus'):
            continue
        fnsplit = str(filename).split('-')
        if str(filename).startswith('morpheus-vm-node'):
            if 'fips' in filename:
                name = 'morpheus-vm-node-fips'
                pkgversion = "%s-%s" % (fnsplit[4], fnsplit[5])
            else:
                name = 'morpheus-vm-node'
                pkgversion = "%s-%s" % (fnsplit[3], fnsplit[4])
        elif str(filename).startswith('morpheus-node'):
            if 'fips' in filename:
                name = 'morpheus-node-fips'
                pkgversion = "%s-%s" % (fnsplit[3], fnsplit[4])
            else:
                name = 'morpheus-node'
                pkgversion = "%s-%s" % (fnsplit[2], fnsplit[3])
        if name in rpmdict:
            if version.parse(rpmdict[name]) < version.parse(pkgversion):
                rpmdict[name] = pkgversion
        else:
            rpmdict[name] = pkgversion
    for filename in os.listdir(rpmdir):
        if not str(filename).startswith('morpheus'):
            continue
        fnsplit = str(filename).split('-')
        if str(filename).startswith('morpheus-vm-node'):
            if 'fips' in filename:
                name = 'morpheus-vm-node-fips'
                pkgversion = "%s-%s" % (fnsplit[4], fnsplit[5])
            else:
                name = 'morpheus-vm-node'
                pkgversion = "%s-%s" % (fnsplit[3], fnsplit[4])
        elif str(filename).startswith('morpheus-node'):
            if 'fips' in filename:
                name = 'morpheus-node-fips'
                pkgversion = "%s-%s" % (fnsplit[3], fnsplit[4])
            else:
                name = 'morpheus-node'
                pkgversion = "%s-%s" % (fnsplit[2], fnsplit[3])
        filepath = rpmdir + filename
        if pkgversion not in rpmdict[name]:
            if actually_delete:
                os.remove(filepath)
                print("DELETED %s" % filepath)
            else:
                print("I WOULD DELETE %s" % filepath)

        else:
            print("LEAVING %s" % filepath)

msidir = '/var/opt/morpheus/package-repos/msi/morpheus-agent/'

msilist = ['MorpheusAgentSetup.msi', 'MorpheusAgentSetup-4_5.msi']
msilist.append(os.readlink(msidir + 'MorpheusAgentSetup.msi'))
msilist.append(os.readlink(msidir + 'MorpheusAgentSetup-4_5.msi'))

for filename in os.listdir(msidir):
    filepath = msidir + filename
    if filename not in msilist:
        if actually_delete:
            os.remove(filepath)
            print("DELETED %s" % filepath)
        else:
            print("I WOULD DELETE %s" % filepath)
    else:
        print("LEAVING %s" % filepath)
