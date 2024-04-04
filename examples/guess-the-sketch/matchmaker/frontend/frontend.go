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
	"net/http"
	"os"

	"github.com/google/uuid"
	"github.com/googollee/go-socket.io"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"open-match.dev/open-match/pkg/pb"
)

const (
	// Default value in the Helm Open Match installation
	// https://github.com/googleforgames/open-match/blob/4eb2ff5e62e445fd068a40504c4e1a4eae83877b/install/helm/open-match/values-production.yaml#L59-L65
	defaultFrontendAddress = "open-match-frontend.open-match.svc.cluster.local:50504"
)

var localAddr string

func main() {
	server := socketio.NewServer(nil)
	server.OnConnect("/", func(s socketio.Conn) error {
		localAddr = s.LocalAddr().String()
		return nil
	})

	server.OnEvent("/", "startGame", func(s socketio.Conn, msg string) {
		fmt.Println("handling startGame event")
		matchmake(s)
	})

	server.OnError("/", func(s socketio.Conn, e error) {
		fmt.Println("error:", e)
	})

	server.OnDisconnect("/", func(s socketio.Conn, reason string) {
		fmt.Println("closed", reason)
	})

	go server.Serve()
	defer server.Close()

	http.Handle("/socket.io/", server)
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("/app/static/"))))

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/" {
			log.Println("Serving index page.")
			http.ServeFile(w, r, "/app/static/index.html")
		} else {
			log.Println("404 on", r.URL.Path)
			http.NotFound(w, r)
		}
	})

	log.Println("Starting server")
	log.Fatal(http.ListenAndServe(":8001", nil))
}

func matchmake(s socketio.Conn) {

	// TODO: Do we need context.WithCancel? "cannot use s.Context() (value of type interface{}) as context.Context
	// value in argument to context.WithCancel: interface{} does not implement context.Context (missing method Deadline)"
	// ctx, cancel := context.WithCancel(ws.Context())
	// defer cancel()
	assignments := make(chan *pb.Assignment)
	errs := make(chan error)

	// Using context.Background() as s.Context() does not implement context.Contextk
	go streamAssignments(context.Background(), assignments, errs)

	for {
		select {
		case err := <-errs:
			log.Println("Error getting assignment:", err)
			s.Emit("MatchMakeResponse", MatchMakeResponse{Err: err}, localAddr)
			return
		case assigment := <-assignments:
			log.Println("assigment.Connection:", assigment.Connection)
			s.Emit("MatchMakeResponse", MatchMakeResponse{Connection: assigment.Connection}, uuid.NewString(), localAddr)
		}
	}
}

func streamAssignments(ctx context.Context, assignments chan *pb.Assignment, errs chan error) {
	conn, err := connectFrontendServer()
	if err != nil {
		errs <- err
	}
	defer conn.Close()
	fe := pb.NewFrontendServiceClient(conn)

	var ticketId string
	crReq := &pb.CreateTicketRequest{
		Ticket: &pb.Ticket{},
	}

	resp, err := fe.CreateTicket(ctx, crReq)
	if err != nil {
		errs <- fmt.Errorf("error creating open match ticket: %w", err)
		return
	}
	ticketId = resp.Id

	defer func() {
		_, err = fe.DeleteTicket(context.Background(), &pb.DeleteTicketRequest{TicketId: ticketId})
		if err != nil {
			log.Println("Error deleting ticket", ticketId, ":", err)
		}
	}()

	waReq := &pb.WatchAssignmentsRequest{
		TicketId: ticketId,
	}

	stream, err := fe.WatchAssignments(ctx, waReq)
	if err != nil {
		errs <- fmt.Errorf("error getting assignment stream: %w", err)
		return
	}
	for {
		resp, err := stream.Recv()
		if err != nil {
			errs <- fmt.Errorf("error streaming assignment: %w", err)
			return
		}
		assignments <- resp.Assignment
	}
}

func connectFrontendServer() (*grpc.ClientConn, error) {
	frontendAddr := os.Getenv("FRONTEND_ADDR")
	if frontendAddr == "" {
		frontendAddr = defaultFrontendAddress
	}
	conn, err := grpc.Dial(frontendAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, fmt.Errorf("error dialing open match: %w", err)
	}
	return conn, nil
}

type MatchMakeResponse struct {
	Connection string `json:"connection,omitempty"`
	Err        error  `json:"err,omitempty"`
}
