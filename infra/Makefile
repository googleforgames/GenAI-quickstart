# Copyright 2023 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
