// Copyright 2023 Google LLC All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
package rest

import (
    "fmt"
    "net/http"
    "bytes"
)

func PostJSON(url string, jsonData []byte) (*http.Response, error) {
    
    req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
    if err != nil {
        return nil, err
    }
    req.Header.Set("Content-Type", "application/json")

    // Send the HTTP request and get the response
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        fmt.Println("Error at postJSON", err)
        return nil, err
    }

    return resp, nil
}
