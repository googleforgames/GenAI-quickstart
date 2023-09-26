#!/bin/sh

mkdir ./scripts/.tmp

cat > ./scripts/.tmp/requireOsLogin.yaml << ENDOFFILE
name: projects/$1/policies/compute.requireOsLogin
spec:
  rules:
  - enforce: false
ENDOFFILE

cat > ./scripts/.tmp/shieldedVm.yaml << ENDOFFILE
name: projects/$1/policies/compute.requireShieldedVm
spec:
  rules:
  - enforce: false
ENDOFFILE

cat > ./scripts/.tmp/vmCanIpForward.yaml << ENDOFFILE
name: projects/$1/policies/compute.vmCanIpForward
spec:
  rules:
  - allowAll: true
ENDOFFILE

cat > ./scripts/.tmp/vmExternalIpAccess.yaml << ENDOFFILE
name: projects/$1/policies/compute.vmExternalIpAccess
spec:
  rules:
  - allowAll: true
ENDOFFILE

cat > ./scripts/.tmp/restrictVpcPeering.yaml << ENDOFFILE
name: projects/$1/policies/compute.restrictVpcPeering
spec:
  rules:
  - allowAll: true
ENDOFFILE

# Sets compute.trustedImageProjects to Google-managed default
cat > ./scripts/.tmp/trustedImageProjects.yaml << ENDOFFILE
name: projects/$1/policies/compute.trustedImageProjects
spec:
  reset: true
ENDOFFILE

# rm -rf ./scripts/.tmp
