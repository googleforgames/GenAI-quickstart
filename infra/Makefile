CUR_DIR=$(shell pwd)
PROJECT_ID=$(shell gcloud config list --format 'value(core.project)' 2>/dev/null)

-include ../.env

authenticate:
	@gcloud auth application-default login

tf-env:
	@sh ${CUR_DIR}/scripts/setup-tf.sh ${CUR_DIR}

kcc-env:
	@sh ${CUR_DIR}/scripts/setup-kcc.sh ${CUR_DIR} ${GSA}

policy-yaml:
	@sh ${CUR_DIR}/scripts/org-policy.sh ${PROJECT_ID}

policy: policy-yaml
	@gcloud org-policies set-policy ${CUR_DIR}/scripts/.tmp/requireOsLogin.yaml
	@gcloud org-policies set-policy ${CUR_DIR}/scripts/.tmp/shieldedVm.yaml
	@gcloud org-policies set-policy ${CUR_DIR}/scripts/.tmp/vmCanIpForward.yaml
	@gcloud org-policies set-policy ${CUR_DIR}/scripts/.tmp/vmExternalIpAccess.yaml
	@gcloud org-policies set-policy ${CUR_DIR}/scripts/.tmp/restrictVpcPeering.yaml
	@gcloud org-policies set-policy ${CUR_DIR}/scripts/.tmp/trustedImageProjects.yaml

policy-apply: policy
	@rm -rf $(CUR_DIR)/scripts/.tmp
