// Copyright 2024 Google LLC
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

package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"google.golang.org/protobuf/types/known/anypb"

	allocationv1 "agones.dev/agones/pkg/apis/allocation/v1"
	"agones.dev/agones/pkg/client/clientset/versioned"
	pb2 "github.com/googleforgames/open-match2/v2/pkg/pb"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"

	"matchmaker/omclient"

	_ "k8s.io/client-go/plugin/pkg/client/auth/gcp"
)

type Client struct {
	AgonesClientset versioned.Interface
	OmClient        *omclient.RestfulOMGrpcClient
}

func main() {
	log.Println("Starting Director")

	for range time.Tick(time.Second) {
		var r Client
		r.AgonesClientset = createAgonesClient()
		r.OmClient = omclient.CreateOMClient()

		if err := r.run(); err != nil {
			log.Println("Error running director:", err.Error())
		}
	}
}

func createAgonesClient() *versioned.Clientset {
	config, err := rest.InClusterConfig()
	if err != nil {
		panic(err.Error())
	}
	agonesClient, err := versioned.NewForConfig(config)
	if err != nil {
		panic(err.Error())
	}
	return agonesClient
}

// Customize the backend.FetchMatches request, the default one will return all tickets in the statestore
func createOMFetchMatchesRequest() *pb2.MmfRequest {
	config, err := rest.InClusterConfig()
	if err != nil {
		fmt.Printf("failed to get K8s config: %v\n", err)
		return &pb2.MmfRequest{}
	}

	client, err := kubernetes.NewForConfig(config)
	if err != nil {
		fmt.Printf("failed to create K8s client: %v\n", err)
		return &pb2.MmfRequest{}
	}

	service, err := client.CoreV1().Services("genai").Get(context.Background(), "guess-the-sketch-mmf", metav1.GetOptions{})
	if err != nil {
		fmt.Printf("Failed to get service: %v\n", err)
		return &pb2.MmfRequest{}
	}
	if len(service.Status.LoadBalancer.Ingress) <= 0 {
		fmt.Println("No external IP found (LoadBalancer might be still provisioning)")
		return &pb2.MmfRequest{}
	}
	ingress := service.Status.LoadBalancer.Ingress[0]
	return &pb2.MmfRequest{
		// om-function:50502 -> the internal hostname & port number of the MMF service in our Kubernetes cluster
		Mmfs: []*pb2.MatchmakingFunctionSpec{
			{
				Host: "http://" + ingress.IP,
				Port: 50502,
				Type: pb2.MatchmakingFunctionSpec_GRPC,
			},
		},
		Profile: &pb2.Profile{
			Name:       "1v1",
			Pools:      map[string]*pb2.Pool{"all": {Name: "everyone"}},
			Extensions: map[string]*anypb.Any{},
		},
	}
}

func createAgonesGameServerAllocation() *allocationv1.GameServerAllocation {
	return &allocationv1.GameServerAllocation{}
}

func createOMAssignTicketRequest(match *pb2.Match, gsa *allocationv1.GameServerAllocation) *pb2.CreateAssignmentsRequest {
	tids := []*pb2.Ticket{}
	for _, r := range match.Rosters {
		tids = append(tids, r.Tickets...)
	}

	return &pb2.CreateAssignmentsRequest{
		AssignmentRoster: &pb2.Roster{
			Name: "My_Assignment_Roster_Name",
			Assignment: &pb2.Assignment{
				Connection: fmt.Sprintf("%s:%d", gsa.Status.Address, gsa.Status.Ports[0].Port),
			},
			Tickets: tids,
		},
	}
}

func (r Client) run() error {
	invocationResultChan := make(chan *pb2.StreamedMmfResponse)

	fmt.Println("Director: start InvokeMatchmakingFunctions in another thread")

	go r.OmClient.InvokeMatchmakingFunctions(context.Background(), createOMFetchMatchesRequest(), invocationResultChan)

	agonesClient := r.AgonesClientset

	totalMatches := 0
	// Read the FetchMatches response. Each loop fetches an available game match that satisfies the match profiles.
	fmt.Println("Director: waiting for invocationResultChan to have a resp")
	for resp := range invocationResultChan {

		fmt.Println("got something from the invocationResultChan: ", resp)

		ctx := context.Background()

		fmt.Println("Allocating a game server")

		gsa, err := agonesClient.AllocationV1().GameServerAllocations("default").Create(ctx, createAgonesGameServerAllocation(), metav1.CreateOptions{})
		if err != nil {
			return fmt.Errorf("error requesting allocation: %w", err)
		}
		// TODO: This drops matches, instead of properly allocating them.  Tickets will only return to
		// the general pool after (iirc) one minute.  We should either tell OM that an assignment isn't
		// coming, or retry for a little while.
		if gsa.Status.State != allocationv1.GameServerAllocationAllocated {
			log.Printf("failed to allocate game server.\n")
			continue
		}

		fmt.Println("The game server is allocated, assigning tickets")

		if _, err = r.OmClient.CreateAssignments(createOMAssignTicketRequest(resp.GetMatch(), gsa)); err != nil {
			// Corner case where we allocated a game server for players who left the queue after some waiting time.
			// Note that we may still leak some game servers when tickets got assigned but players left the queue before game frontend announced the assignments.
			if err = agonesClient.AgonesV1().GameServers("default").Delete(ctx, gsa.Status.GameServerName, metav1.DeleteOptions{}); err != nil {
				return fmt.Errorf("error assigning tickets: %w", err)
			}
		}

		totalMatches++
	}

	log.Printf("Created and assigned %d matches", totalMatches)

	return nil
}
